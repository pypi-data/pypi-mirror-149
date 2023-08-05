#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 13:39:58 2021

@author: mike
"""
import os
import numpy as np
import xarray as xr
import pandas as pd
import tethys_utils as tu
from tethysts.utils import s3_client, get_object_s3, read_json_zstd, read_pkl_zstd, download_results, create_public_s3_url
import tethys_data_models as tdm
from typing import List, Optional, Dict, Union
from botocore import exceptions as bc_exceptions
import requests
import uuid
from cryptography.fernet import Fernet
import pandas as pd
from pydantic import HttpUrl
import concurrent.futures
import copy
from shapely import wkb, wkt, geometry
import pathlib
import dask
import glob
from datetime import date, datetime
import multiprocessing as mp
import pyproj
import random
from time import sleep

##############################################
### Parameters

b2_dl_by_id = 'https://b2.tethys-ts.xyz/b2api/v1/b2_download_file_by_id?fileId={obj_id}'


preprocessed_dir = 'preprocessed_data'
previous_dir = 'previous_data'
final_dir = 'final_results'

preprocessed_file_str = '{ds_id}_{file_id}.nc.zst'
interim_file_str = '{ds_id}_{stn_id}_{date}.nc'

base_encoding = {'lon': {'dtype': 'int32', '_FillValue': -999999, 'scale_factor': 1e-07},
'lat': {'dtype': 'int32', '_FillValue': -999999, 'scale_factor': 1e-07},
'altitude': {'dtype': 'int32', '_FillValue': -9999, 'scale_factor': 0.001},
'time': {'_FillValue': -99999999, 'units': 'days since 1970-01-01 00:00:00'},
'height': {'dtype': 'int16', '_FillValue': -9999}}

dask.config.set(**{'array.slicing.split_large_chunks': False})

agg_stat_mapping = {'mean': 'mean', 'cumulative': 'sum', 'continuous': None, 'maximum': 'max', 'median': 'median', 'minimum': 'min', 'mode': 'mode', 'sporadic': None, 'standard_deviation': 'std', 'incremental': 'cumsum'}

tz_str = 'Etc/GMT{0:+}'

###############################################
### Helper functions



# def save_chunks(chunks_list, output_path):
#     """

#     """
#     for c in chunks_list:
#         chunk_json = tdm.dataset.ChunkID(height=int(c.height.values[0] * 1000), start_date=int(c.attrs['start_date'])).json(exclude_none=True).encode('utf-8')
#         chunk_id = blake2b(chunk_json, digest_size=12).hexdigest()
#         stn_id = str(c.station_id.values[0])
#         file_path = os.path.join(output_path, stn_id + '_' + chunk_id + '.nc.zst')

#         b = c.copy().load()

#         obj1 = tu.misc.write_pkl_zstd(b.to_netcdf(), file_path)

#         b.close()
#         del b
#         del obj1


def multi_save_dataset_stations(nc_paths, block_length, block_length_factor: int = 10, compression='zstd', remove_station_data=True, max_workers=3):
    """

    """
    if isinstance(nc_paths, str):
        nc_paths1 = glob.glob(nc_paths)
    elif isinstance(nc_paths, list):
        nc_paths1 = nc_paths

    ## Iterate through files
    if max_workers <= 1:

        nc_paths = []
        for nc_path in nc_paths1:
            new_paths0 = tu.processing.save_dataset_stations(nc_path, block_length * block_length_factor, compression=compression, remove_station_data=remove_station_data)
            nc_paths.append(new_paths0)
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
            futures = []
            for nc_path in nc_paths1:
                f = executor.submit(tu.processing.save_dataset_stations, nc_path, block_length * block_length_factor, compression=compression, remove_station_data=remove_station_data)
                futures.append(f)
            runs = concurrent.futures.wait(futures)

        new_paths = [r.result() for r in runs[0]]

    ## process output
    new_paths1 = []
    for new_path in new_paths:
        new_paths1.extend(new_path)

    new_paths1.sort()

    return new_paths1


def estimate_time_interval_accurate(data, block_length, null_grid=None, max_mb=2):
    """

    """
    ## Get the dimension data
    dims = dict(data.dims)

    ## Test requested block_length
    chunks_list = tu.processing.chunk_data(data, block_length=block_length, time_interval=None, null_grid=null_grid)

    dim_sizes = np.array([np.prod(list(c.dims.values())) for c in chunks_list])
    max_dim_index = np.argsort(dim_sizes)[-10:]
    sum_dim_objs = np.sum(dim_sizes[max_dim_index])

    sum_chunks = 0
    for i in max_dim_index:
        chunk = chunks_list[i].copy().load()
        obj_len = len(tu.misc.write_pkl_zstd(chunk.to_netcdf()))

        sum_chunks += obj_len

        chunk.close()
        del chunk

    dim_per_mb = int(sum_dim_objs/(sum_chunks * 0.000001))

    if 'geometry' in dims:
        geo_sizes = np.array([c.dims['geometry'] for c in chunks_list])
    else:
        geo_sizes = np.array([c.dims['lon'] * c.dims['lat'] for c in chunks_list])

    max_geo_size = np.max(geo_sizes)

    times_per_mb = (dim_per_mb/max_geo_size)

    ## Calc time_interval
    times1 = pd.to_datetime(data['time'].values)
    days = times1.floor('D').drop_duplicates()
    times_per_day = len(times1)/len(days)

    days_per_mb = times_per_mb/times_per_day

    days_per_chunk = int(days_per_mb * max_mb)

    ## Test final parameters
    chunks_list = tu.processing.chunk_data(data, block_length=block_length, time_interval=days_per_chunk, null_grid=null_grid)

    n_chunks = len(chunks_list)

    _ = [c.close() for c in chunks_list]
    del chunks_list

    output_dict = {'time_interval': days_per_chunk,
                   'n_geometries_per_station': max_geo_size,
                   'n_chunks': n_chunks,
                   'values_per_mb': dim_per_mb
                   }

    return output_dict


def bulk_estimate_time_interval(data, block_lengths, null_grid=None, max_mb=2):
    """

    """
    block_length_dict = {}
    for b in block_lengths:
        print(b)
        o1 = estimate_time_interval_accurate(data, b, null_grid, max_mb)
        block_length_dict[b] = o1

    return block_length_dict


def estimate_time_interval_rough(data_grid_length, time_freq, block_lengths, max_mb=2, values_per_mb=550000):
    """
    Function to roughly estimate the appropriate time intervals based on specific block lengths.

    Parameters
    ----------
    data_grid_length: float or int
        The grid resolution.
    time_freq: str
        The time resolution in pandas time freq format.
    block_lengths: list of float
        The block lengths to test. Should be equal to or greater than the data_grid_length.
    max_mb: float or int
        The max size of the results object.
    values_per_mb: int
        The number of data values in a results object per MB. Do not change unless you've done the testing to determine this value.
    """
    t1 = pd.date_range('2000-01-01', '2000-01-08', freq = time_freq)[:-1]
    val_per_day = len(t1)/7

    total_val_per_day = max_mb * values_per_mb

    res_list = []
    for bl in block_lengths:
        n_stns = int(np.ceil((bl**2)/(data_grid_length**2)))
        days_per_chunk = int(total_val_per_day/n_stns/val_per_day)
        dict1 = {'time_interval': days_per_chunk,
                 'n_geometries_per_station': n_stns}
        res_list.append(dict1)

    res_dict = {bl: res_list[i] for i, bl in enumerate(block_lengths)}

    return res_dict


def decompress_path(glob_path, compression_type='gzip', max_workers=4, **kwargs):
    """

    """
    if isinstance(glob_path, str):
        files1 = glob.glob(glob_path)
    elif isinstance(glob_path, list):
        files1 = glob_path
    new_files = tu.data_io.decompress_files_remove(files1, max_workers=max_workers)

    return new_files


def file_format_conversion(glob_path, file_format='grib', max_workers=4, **kwargs):
    """
    Function to convert data files to netcdf files.
    """
    if isinstance(glob_path, str):
        files1 = glob.glob(glob_path)
    elif isinstance(glob_path, list):
        files1 = glob_path

    if file_format == 'grib':
        new_files = tu.data_io.convert_gribs_remove(files1, max_workers=max_workers)
    else:
        raise NotImplementedError('file_format not available.')
    # elif file_format == 'geotiff':
    #     new_files = tu.data_io.convert_geotiffs_to_nc(files1, max_workers=max_workers, **kwargs)

    return new_files


def get_obj_list(glob_path, date_format=None, freq=None, from_date=None, to_date=None, connection_config=None, bucket=None):
    """

    """
    glob_path2 = glob_path

    if isinstance(connection_config, dict) and isinstance(bucket, str):
        if glob_path2.startswith('/'):
            glob_path2 = glob_path2[1:]
        glob_path3, glob_ext = os.path.split(glob_path2)
        if not glob_path3.endswith('/'):
            glob_path3 = glob_path3 + '/'
        s3 = s3_client(connection_config)
        obj_list = tu.s3.list_objects_s3(s3, bucket, glob_path3, delimiter='/', date_format=date_format)
        obj_list1 = obj_list.rename(columns={'Key': 'path', 'Size': 'size', 'KeyDate': 'date'}).drop(['LastModified', 'ETag'], axis=1).copy()
        # obj_list1['remote_type'] = 's3'
    else:
        files1 = glob.glob(glob_path)
        sizes = [os.path.getsize(f) for f in files1]
        obj_list1 = pd.DataFrame(zip(files1, sizes), columns=['path', 'size'])
        # obj_list1['remote_type'] = 'local'

        if isinstance(date_format, str):
            dates1 = tu.misc.filter_data_paths(obj_list1.path, date_format, return_dates=True)
            obj_list1 = pd.merge(obj_list1, dates1, on='path')

    filter1 = [pathlib.Path(p).match(glob_path2) for p in obj_list1.path.values]
    obj_list2 = obj_list1.iloc[filter1]

    if isinstance(date_format, str):
        if isinstance(from_date, (str, pd.Timestamp, date, datetime)):
            obj_list2 = obj_list2[obj_list2['date'] >= pd.Timestamp(from_date)].copy()
        if isinstance(to_date, (str, pd.Timestamp, date, datetime)):
            obj_list2 = obj_list2[obj_list2['date'] < pd.Timestamp(to_date)].copy()

    if isinstance(freq, str):
        grp1 = obj_list2.groupby(pd.Grouper(key='date', freq=freq, origin='start'))

        obj_list3 = [v for k, v in grp1]
    else:
        obj_list3 = obj_list2

    return obj_list3


def copy_source_objs(source_paths, dest_path, bucket=None, connection_config=None, public_url=None, compression=None, threads=None, max_workers=None):
    """

    """
    objs = source_paths

    if isinstance(connection_config, (dict, str)) and isinstance(bucket, str):
        s3 = s3_client(connection_config, threads)

        if isinstance(max_workers, int):

            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                futures = []
                for obj in objs:
                    f = executor.submit(tu.data_io.copy_s3_file, source_path=obj, dest_path=dest_path, connection_config=connection_config, bucket=bucket, public_url=public_url, compression=compression)
                    futures.append(f)
                runs = concurrent.futures.wait(futures)

            new_paths = [r.result() for r in runs[0]]

        else:
            if threads is None:
                threads = 4

            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for obj in objs:
                    f = executor.submit(tu.data_io.copy_s3_file, source_path=obj, dest_path=dest_path, s3=s3, connection_config=connection_config, bucket=bucket, public_url=public_url, compression=compression)
                    futures.append(f)
                runs = concurrent.futures.wait(futures)

            new_paths = [r.result() for r in runs[0]]

    else:
        new_paths = []
        for obj in objs:
            path1 = tu.data_io.copy_file(source_path=obj, dest_path=dest_path, compression=compression)
            new_paths.append(path1)

    new_paths.sort()

    return new_paths


def copy_interim_objs(source_paths, dest_path, bucket, connection_config=None, public_url=None, threads=20):
    """

    """
    s3 = s3_client(connection_config, threads)

    path1 = pathlib.Path(dest_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for source_path in source_paths:
            p_list = source_path.split('/')
            ds_id = p_list[4]
            stn_id, date, nc, z = p_list[5].split('.')

            file_name = interim_file_str.format(ds_id=ds_id, stn_id=stn_id, date=date)
            dest_path1 = str(path1.joinpath(file_name))

            f = executor.submit(tu.data_io.copy_s3_file, source_path, dest_path1, bucket, s3=s3, public_url=public_url, compression='zstd')
            futures.append(f)
        runs = concurrent.futures.wait(futures)

    new_paths = [r.result() for r in runs[0]]

    new_paths.sort()

    return new_paths


def variable_processing(nc_paths, time_name, x_name, y_name, variables, projected_coordinates=True, nc_source='normal', max_workers=4):
    """
    The variable processing function does three things:
        - select only the specific variables that should be exported,
        - restructure (transpose in xarray) the coordinates so that they are ordered by time, y, x, height,
        - remove duplicate overlapping timestamps between files.

    The restructuring of the coordinates must make sure that the time coordinate is called "time", but the x and y coordinates do not necessarily need to be modified. They just need to be in the correct order. If they are actually longitude and latitude, changing them to lon and lat will make things easier in the future.
    This process will iterate over all of the nc files rather than trying to open them and process them using Dask and xarray. They will initially be opened in Dask to determine the overlapping times only.

    Parameters
    ----------
    nc_paths : list of str or glob str
        The paths to the nc files to be processed.
    variables : list of str
        The variables that should be extracted from the nc files.
    time_index_bool : list of bool
        The boolean time index in case only one file is pulled down to be processed. Normally this should not be needed as there will be multiple files to determine the overlapping times.
    """
    if isinstance(nc_paths, str):
        nc_paths1 = glob.glob(nc_paths)
    elif isinstance(nc_paths, list):
        nc_paths1 = nc_paths

    nc_paths1.sort()

    ## Determine duplicate times
    if len(nc_paths1) > 1:
        time_index_bool = tu.processing.determine_duplicate_times(nc_paths1, time_name)
    else:
        time_index_bool = None

    ## Iterate through files
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
        futures = []
        for nc_path in nc_paths1:
            f = executor.submit(tu.processing.preprocess_data_structure, nc_path, time_name, x_name, y_name, variables, time_index_bool, projected_coordinates)
            futures.append(f)
        runs = concurrent.futures.wait(futures)

    ## process output
    new_paths = [r.result() for r in runs[0]]
    new_paths1 = []
    for new_path in new_paths:
        new_paths1.extend(new_path)

    new_paths1.sort()

    return new_paths1


def resample_to_wgs84_grids(nc_paths, proj4_crs, order=1, min_val=None, max_val=None, bbox=None, time_name='time', x_name='x', y_name='y', max_workers=4):
    """

    """
    if isinstance(nc_paths, str):
        nc_paths1 = glob.glob(nc_paths)
    elif isinstance(nc_paths, list):
        nc_paths1 = nc_paths

    xr1 = xr.open_dataset(nc_paths1[0])

    ## Get approximate grid resolution
    x1 = xr1[x_name].values
    half_x = len(x1)//2
    x = x1[half_x:(half_x+10)]

    y1 = xr1[y_name].values
    half_y = len(y1)//2
    y = y1[half_y:(half_y+10)]

    xr1.close()
    del xr1

    wgs84 = pyproj.Proj(proj='latlong', datum='WGS84')

    trans = pyproj.Transformer.from_proj(proj4_crs, wgs84)

    lon, lat = trans.transform(x, y)

    grid_res_lat = np.quantile(np.abs(np.diff(lat.T)), 0.5)
    grid_res_lon = np.quantile(np.abs(np.diff(lon.T)), 0.5)
    grid_res = round((grid_res_lon + grid_res_lat)/2, 5)

    ## Iterate through files
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
        futures = []
        for nc_path in nc_paths1:
            f = executor.submit(tu.processing.resample_to_wgs84_grid, nc_path, proj4_crs, grid_res, order, min_val, max_val, bbox)
            futures.append(f)
        runs = concurrent.futures.wait(futures)

    ## process output
    print('grid resolution/length is: ' + str(grid_res))
    new_paths = [r.result() for r in runs[0]]
    new_paths.sort()

    return new_paths


# def calc_new_parameters():
#     """

#     """
#     dates1 = tu.misc.filter_data_paths(obj_list1.path, date_format, return_dates=True)



def combine_metadata(project, dataset):
    """

    """
    datasets = []
    for d in dataset:
        d1 = copy.deepcopy(d)
        d1.update(project)
        datasets.append(d1)

    return datasets


def multi_calc_new_variables(nc_paths, datasets, version_date, func_dict):
    """

    """
    dates1 = tu.misc.filter_data_paths(nc_paths, '%Y%m%d%H%M%S', return_dates=True)
    dates1['variable'] = dates1.path.apply(lambda x: pathlib.Path(x).stem.split('_wgs84_')[0])

    ## Iterate through files
    # if max_workers <=1:
    new_paths_list = []
    for i, g in dates1.groupby('date'):
        # print(g)
        p = tu.processing.calc_new_variables(g['path'].tolist(), datasets, version_date, func_dict)
        new_paths_list.append(p)

    # elif max_workers > 1:
    #     with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
    #         futures = []
    #         for i, g in dates1.groupby('date'):
    #             # print(g)
    #             f = executor.submit(tu.processing.calc_new_variables, g['path'].tolist(), datasets, func_dict)
    #             futures.append(f)
    #         runs = concurrent.futures.wait(futures)

    #     # process output
    #     new_paths_list = [r.result() for r in runs[0]]

    new_paths1 = []
    for new_path in new_paths_list:
        new_paths1.extend(new_path)

    new_paths1.sort()

    return new_paths1


def multi_mergetime_nc_remove(source_paths, by, max_workers=3):
    """

    """
    source_paths_dict = {}
    if by == 'dataset':
        for p in source_paths:
            path1 = pathlib.Path(p)
            ds_id = path1.stem.split('_')[0]
            if ds_id in source_paths_dict:
                source_paths_dict[ds_id].append(p)
            else:
                source_paths_dict[ds_id] = [p]
    elif by == 'station':
        for p in source_paths:
            path1 = pathlib.Path(p)
            ds_id, stn_id, date = path1.stem.split('_')
            key = (ds_id, stn_id)
            if key in source_paths_dict:
                source_paths_dict[key].append(p)
            else:
                source_paths_dict[key] = [p]
    else:
        raise ValueError('by must be either dataset or station.')

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
        futures = []
        for ds_id, paths in source_paths_dict.items():
            f = executor.submit(tu.data_io.mergetime_nc_remove, paths, by)
            futures.append(f)
        runs = concurrent.futures.wait(futures)

    new_paths = [r.result() for r in runs[0]]
    new_paths.sort()

    return new_paths


###############################################
### Class


class Titan(object):
    """

    """

    def __init__(self, temp_path: pathlib.Path, add_old: bool, run_id: str = None, key: str = None, diagnostics_url: HttpUrl = None ):
        """

        """
        ## Check temp path
        os.makedirs(temp_path, exist_ok=True)

        if not os.access(temp_path, os.W_OK):
            raise OSError('{} has no write access.'.format(temp_path))

        ## Add in the additional paths
        preprocessed_path = os.path.join(temp_path, preprocessed_dir)
        previous_path = os.path.join(temp_path, previous_dir)
        # final_path = os.path.join(temp_path, final_dir)
        os.makedirs(preprocessed_path, exist_ok=True)
        os.makedirs(previous_path, exist_ok=True)
        # os.makedirs(final_path, exist_ok=True)

        self.preprocessed_path = preprocessed_path
        self.previous_path = previous_path
        # self.final_path = final_path

        self._add_old = add_old

        ## Test for the run_id and key
        need_dgn = True

        if isinstance(key, str) and (diagnostics_url is not None):
            # Attempt to read the diagnostics file
            try:
                resp = requests.get(diagnostics_url)
                f = Fernet(key)
                dgn = read_json_zstd(f.decrypt(resp.content))
                run_id = dgn['run_id']
                need_dgn = False

                _ = [setattr(self, k, v) for k, v in dgn['attributes'].items()]
                print('Diagnostics file has loaded sucessfully.')
            except:
                print('Reading diagnostics file failed. Check the URL link. If you continue, the diagnostics file will be overwritten.')

        if (not isinstance(key, str)):
            key = Fernet.generate_key().decode()
            print('A new encryption key has been generated. Keep it safe and secret:')
            print(key)

        if isinstance(run_id, str):
            if len(run_id) != 14:
                print('The run_id provided is not correct, setting a new one.')
                run_id = uuid.uuid4().hex[:14]
                print('A new run_id has been generated:')
                print(run_id)
        else:
            run_id = uuid.uuid4().hex[:14]
            print('A new run_id has been generated:')
            print(run_id)

        self.key = key
        self.run_id = run_id
        self.temp_path = temp_path
        self._results_objects_updated = []

        ## Set up diagnostics dict
        if need_dgn:
            run_date1 = tu.misc.make_run_date_key()
            dgn = {'attributes': {},
                   'run_id': run_id,
                   'run_date': run_date1,
                   'key': key
                   }

        self.diagnostics = dgn

        pass


    @staticmethod
    def process_sparse_stations_from_df(stns, precision=7):
        """
        Function that takes a stns dataframe of station data and converts it to an Xarray Dataset for Tethys. This is ultimately meant to be combined with the time series data for futher processing. If a geometry column is provided, it must be as a geojson-type dict (not a geopandas column).

        """
        stns = tu.processing.process_sparse_stations_from_df(stns, precision=precision)

        return stns


    @staticmethod
    def combine_dataset_metadata(project, dataset):
        """

        """
        datasets = []
        for d in dataset:
            d1 = copy.deepcopy(d)
            d1.update(project)
            datasets.append(d1)

        return datasets


    @staticmethod
    def combine_obs_stn_data(ts_data, stn_data, mod_date=False):
        """
        Function to take a time series DataFrame and station data (in 3 formats) and combine them into a single xr.Dataset.

        Parameters
        ----------
        ts_data: pd.DataFrame
            The DataFrame should have height and time as columns in addition to the parameter column.
        stn_data: pd.Series, pd.DataFrame, dict, xr.Dataset
            The station data that should have geometry as a column.
        mod_date: bool
            The the modified_date be added to the ts_data?

        Returns
        -------
        xr.Dataset
        """
        r1 = tu.processing.combine_obs_stn_data(ts_data, stn_data, mod_date=mod_date)

        return r1


    def resample_time_series(self, df, dataset_id, sum_closed='right', other_closed='left', discrete=False):
        """

        """
        dataset = self.datasets[dataset_id]
        freq_code = dataset['frequency_interval']
        agg_stat = dataset['aggregation_statistic']
        parameter = dataset['parameter']
        utc_offset = dataset['utc_offset']

        df1 = df.copy()

        # check columns
        cols = df1.columns

        if 'time' not in cols:
            raise ValueError('time must be a column.')
        if parameter not in cols:
            raise ValueError(parameter + ' must be a column.')

        grp = []
        if 'station_id' in cols:
            grp.append('station_id')
        if 'height' in cols:
            grp.append('height')

        vars1 = [parameter] + ['time'] + grp

        ancillary_variables = [v for v in cols if (v not in vars1)]

        # main_vars = [parameter] + ancillary_variables

        # Convert times to local TZ if necessary
        if (not freq_code in ['None', 'T', 'H', '1H']) and (utc_offset != '0H'):
            t1 = int(utc_offset.split('H')[0])
            tz1 = tz_str.format(-t1)
            df1['time'] = df1['time'].dt.tz_localize('UTC').dt.tz_convert(tz1).dt.tz_localize(None)

        ## Aggregate data if necessary
        # Parameter
        if freq_code == 'None':
            data1 = df1.drop_duplicates(subset=['time']).sort_values('time')
        else:
            agg_fun = agg_stat_mapping[agg_stat]

            if agg_fun == 'sum':
                data0 = tu.misc.grp_ts_agg(df1[vars1], grp, 'time', freq_code, agg_fun, closed=sum_closed)
            else:
                data0 = tu.misc.grp_ts_agg(df1[vars1], grp, 'time', freq_code, agg_fun, discrete, closed=other_closed)

            # Ancillary variables
            av_list = [data0]
            for av in ancillary_variables:
                if 'quality_code' == av:
                    df1['quality_code'] = pd.to_numeric(df1['quality_code'], errors='coerce', downcast='integer')
                    qual1 = tu.misc.grp_ts_agg(df1[['time'] + grp + ['quality_code']], grp, 'time', freq_code, 'min')
                    av_list.append(qual1)
                else:
                    av1 = tu.misc.grp_ts_agg(df1[['time'] + grp + [av]], grp, 'time', freq_code, 'max')
                    av_list.append(av1)

            # Put the data together
            data1 = pd.concat(av_list, axis=1).reset_index().sort_values('time')

        # Convert time back to UTC if necessary
        if (not freq_code in ['None', 'T', 'H', '1H']) and (utc_offset != '0H'):
            data1['time'] = data1['time'].dt.tz_localize(tz1).dt.tz_convert('utc').dt.tz_localize(None)

        return data1


    def status_checks(self, connection_config: tdm.base.ConnectionConfig, bucket: str, public_url: str = None, system_version: int = 4, load_diagnostics: bool = False):
        """

        """
        ## Test S3 connection
        _ = tdm.base.Remote(**{'connection_config': connection_config, 'bucket': bucket, 'version': system_version})
        s3 = s3_client(connection_config)

        # Read permissions
        try:
            _ = s3.head_bucket(Bucket=bucket)
        except Exception as err:
            response_code = err.response['Error']['Code']
            if response_code == '403':
                raise requests.exceptions.ConnectionError('403 error. The connection_config is probably wrong.')
            elif response_code == '404':
                raise requests.exceptions.ConnectionError('404 error. The bucket was not found.')

        # Write permissions
        test1 = b'write test'
        test_key = 'tethys/testing/test_write.txt'

        try:
            _ = tu.s3.put_object_s3(s3, bucket, test_key, test1, {}, '', retries=1)
        except bc_exceptions.ConnectionClosedError:
            raise ValueError('Account does not have write permissions.')

        # Public URL read test
        if isinstance(public_url, str):
            try:
                _ = tdm.base.Remote(**{'public_url': public_url, 'bucket': bucket, 'version': system_version})
                _ = get_object_s3(test_key, public_url=public_url, bucket=bucket, counter=1)
            except:
                raise ValueError('public_url does not work.')

        ## Check that the S3 version is valid
        if not system_version in tdm.key_patterns:
            raise ValueError('S3 version must be one of {}.'.format(list(tdm.key_patterns.keys())))

        ## Check if there is an existing Tethys S3 version
        # Version 3+ check
        objs1 = tu.s3.list_objects_s3(s3, bucket, 'tethys/', delimiter='/')
        if not objs1.empty:
            exist_version = int(objs1.iloc[0].Key.split('/')[1].split('.')[0][1:])
        else:
        # Version 2 check
            objs2 = tu.s3.list_objects_s3(s3, bucket, 'tethys/v2/', delimiter='/')
            if objs2.empty:
                exist_version = None
            else:
                exist_version = 2

        if isinstance(exist_version, int):
            if exist_version != system_version:
                print('The bucket already has Tethys data and is version {}. You have been warned...'.format(exist_version))

        print('All status checks passed!')

        ## Save parameters
        setattr(self, 'connection_config', connection_config)
        setattr(self, 'bucket', bucket)
        setattr(self, 'public_url', public_url)
        setattr(self, 'system_version', system_version)

        ## Loading diagnostic log if it exists
        if load_diagnostics:
            dgn_key_pattern = tdm.key_patterns[self.system_version]['diagnostics']
            dgn_key = dgn_key_pattern.format(run_id=self.run_id)

            try:
                resp = get_object_s3(dgn_key, bucket, s3, public_url=public_url, counter=0)
                f = Fernet(self.key)
                dgn = read_json_zstd(f.decrypt(resp))
                self.diagnostics = dgn
                _ = [setattr(self, k, v) for k, v in dgn['attributes'].items()]
                print('Diagnostics log found and loaded.')
            except:
                ## diagnostic log
                self.diagnostics['status_checks'] = {'pass': True}
                self.diagnostics['attributes'].update({'connection_config': connection_config, 'bucket': bucket, 'public_url': public_url, 'system_version': system_version})
        else:
            ## diagnostic log
            self.diagnostics['status_checks'] = {'pass': True}
            self.diagnostics['attributes'].update({'connection_config': connection_config, 'bucket': bucket, 'public_url': public_url, 'system_version': system_version})


    def save_diagnostics(self):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'status_checks')

        f = Fernet(self.key)
        dgn_obj = f.encrypt(tu.misc.write_json_zstd(copy.deepcopy(self.diagnostics)))

        dgn_key_pattern = tdm.key_patterns[self.system_version]['diagnostics']
        dgn_key = dgn_key_pattern.format(run_id=self.run_id)

        s3 = s3_client(self.connection_config)
        run_date1 = tu.misc.make_run_date_key()

        obj_resp = tu.s3.put_object_s3(s3, self.bucket, dgn_key, dgn_obj, {'run_date': run_date1}, 'application/json')

        self.diagnostics['diagnostic_s3_obj_id'] = obj_resp['VersionId']

        if isinstance(self.public_url, str):
            dgn_url = create_public_s3_url(self.public_url, self.bucket, dgn_key)
        else:
            dgn_url = ''

        return dgn_url


    def load_dataset_metadata(self, datasets: Union[dict, list]):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'status_checks')

        dataset_list = tu.processing.process_datasets(datasets)

        # TODO: Check for existing datasets in other S3 buckets

        ## Check if the chunking parameters are in the datasets
        for ds in dataset_list:
            if 'chunk_parameters' in ds:
                _ = tdm.dataset.ChunkParams(**ds['chunk_parameters'])
            elif ds['method'] in ['sensor_recording', 'field_activity', 'sample_analysis']:
                print('Default chunk_parameters have been set.')
                ds['chunk_parameters'] = {'block_length': 0, 'time_interval': 7300}
            else:
                raise ValueError('chunk_parameters have not been set in the dataset metadata. Please do so.')

        ## Might keep this for later...
        # chunk_params_bool_list = []
        # for ds in dataset_list:
        #     if 'chunk_parameters' in ds:
        #         _ = tdm.dataset.ChunkParams(**ds['chunk_parameters'])
        #         chunk_params_bool_list.extend([True])
        #     else:
        #         chunk_params_bool_list.extend([True])

        # if all(chunk_params_bool_list):
        #     self.diagnostics['set_chunking_parameters'] = {'pass': True}

        ## Validate dataset model
        for ds in dataset_list:
            _ = tdm.dataset.Dataset(**ds)

        ## Set attributes
        ds_dict = {ds['dataset_id']: ds for ds in dataset_list}

        setattr(self, 'dataset_list', dataset_list)
        setattr(self, 'datasets', ds_dict)

        ## diagnostic log
        self.diagnostics['load_dataset_metadata'] = {'pass': True}
        self.diagnostics['attributes'].update({'dataset_list': dataset_list, 'datasets': ds_dict})


    # def set_chunking_parameters(self, block_length, time_interval=None):
    #     """

    #     """
    #     tu.misc.diagnostic_check(self.diagnostics, 'load_dataset_metadata')

    #     chunk_params = tdm.dataset.ChunkParams(block_length=block_length, time_interval=time_interval).dict(exclude_none=True)

    #     datasets = []
    #     for ds in self.dataset_list:
    #         ds['chunk_parameters'] = chunk_params
    #         datasets.append(ds)

    #     self.load_dataset_metadata(datasets)


    def process_versions(self, version_data: dict):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'load_dataset_metadata')

        version_dict, vd_old = tu.s3.process_dataset_versions(self.dataset_list, bucket=self.bucket, connection_config=self.connection_config, public_url=self.public_url, version_data=version_data, system_version=self.system_version)
        max_version_date = max(list([d['version_date'] for d in version_dict.values()]))

        # setattr(self, 'processing_code', processing_code)
        setattr(self, 'version_dict', version_dict)
        setattr(self, 'max_version_date', max_version_date)
        setattr(self, 'old_versions', vd_old)

        ## diagnostic log
        self.diagnostics['process_versions'] = {'pass': True}
        self.diagnostics['attributes'].update({'version_dict': version_dict, 'max_version_date': max_version_date, 'old_versions': vd_old})

        return version_dict


    def save_preprocessed_results(self, data: Union[List[xr.Dataset], xr.Dataset], dataset_id: str):
        """
        Method to save preprocessed results xarray datasets to netcdf files in the temp_path. The results must have the standard dimensions, geometry caclulated, appropriate parameter names, and station data.
        """
        ## All the checks...
        tu.misc.diagnostic_check(self.diagnostics, 'load_dataset_metadata')

        dataset1 = self.datasets[dataset_id]
        result_type = dataset1['result_type']
        param = dataset1['parameter']
        data_model = tdm.dataset.result_type_dict[result_type]
        dims = set(data_model.schema()['properties'].keys())

        if isinstance(data, xr.Dataset):
            data_list = [data]
        else:
            data_list = data

        _ = [data_model(**d.dims) for d in data_list]

        for d in data_list:
            if not param in d:
                raise ValueError('The {param} valiable should be in the data if {ds_id} is the dataset_id.'.format(param=param, ds_id=dataset_id))

            d_dims = set(d[param].dims)
            if d_dims != dims:
                raise ValueError('The {param} valiable should contain the dims: {dims}.'.format(param=param, dims=dims))

        ## Save the data
        file_list = []
        for d in data_list:
            # print(str(d.ref.values[0]))

            ## Update the metadata
            d = tu.processing.add_metadata_results(d, dataset1, self.max_version_date)

            file_id = uuid.uuid4().hex[:14]
            file_path = os.path.join(self.preprocessed_path, preprocessed_file_str.format(ds_id=dataset_id, file_id=file_id))

            tu.processing.write_nc_zstd(d, file_path)

            # Read the file back in to make sure it worked...
            # _ = xr.load_dataset(read_pkl_zstd(file_path))

            file_list.append(file_path)

        return file_list


    def get_obj_list(self, glob_path, date_format=None, freq=None, from_date=None, to_date=None, source_connection_config=None, source_bucket=None, source_public_url=None):
        """

        """
        obj_list = get_obj_list(glob_path, date_format=date_format, freq=freq, from_date=from_date, to_date=to_date, connection_config=source_connection_config, bucket=source_bucket)

        # self.obj_list = obj_list.path.tolist()
        self.source_connection_config = source_connection_config
        self.source_bucket = source_bucket
        self.source_public_url = source_public_url

        ## diagnostic log
        self.diagnostics['get_obj_list'] = {'pass': True}
        self.diagnostics['attributes'].update({'source_connection_config': source_connection_config, 'source_bucket': source_bucket, 'source_public_url': source_public_url})

        return obj_list


    def copy_source_objs(self, source_paths, compression=None, threads=None, max_workers=None):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'get_obj_list')

        new_paths = copy_source_objs(source_paths, self.preprocessed_path, threads=threads, compression=compression, connection_config=self.source_connection_config, bucket=self.source_bucket, public_url=self.source_public_url, max_workers=max_workers)

        return new_paths


    # def decompress_files(self, source_paths, compression_type='gzip', max_workers=4):
    #     """

    #     """
    #     new_paths1 = decompress_path(source_paths, compression_type=compression_type, max_workers=max_workers)

    #     return new_paths1


    def file_format_conversion(self, source_paths, file_format='grib', max_workers=4, **kwargs):
        """

        """
        new_paths2 = file_format_conversion(source_paths, file_format=file_format, max_workers=max_workers, **kwargs)

        return new_paths2


    def variable_processing(self, source_paths, time_name, x_name, y_name, variables, projected_coordinates=True, nc_source='normal', max_workers=4):
        """

        """
        new_paths2 = variable_processing(source_paths, time_name, x_name, y_name, variables, projected_coordinates=projected_coordinates, max_workers=max_workers)

        return new_paths2


    def resample_to_wgs84(self, source_paths, proj4_crs, order=2, bbox=None, max_workers=4):
        """

        """
        new_paths2 = resample_to_wgs84_grids(source_paths, proj4_crs, order=order, bbox=bbox, max_workers=max_workers)

        return new_paths2


    def calc_new_variables(self, source_paths, func_dict):
        """

        """
        new_paths2 = multi_calc_new_variables(source_paths, self.dataset_list, self.max_version_date, func_dict)

        return new_paths2


    def merge_time_nc_files(self, source_paths, by, max_workers=4):
        """

        """
        # if by == 'station':
        #     tu.misc.diagnostic_check(self.diagnostics, 'copy_interim_objs')

        new_paths = multi_mergetime_nc_remove(source_paths, by=by, max_workers=max_workers)

        if by == 'station':
            ## diagnostic log
            self.diagnostics['merge_nc_files'] = {'pass': True}

        return new_paths


    def save_dataset_stations(self, source_paths, block_length, block_length_factor=10, compression='zstd', max_workers=4):
        """

        """
        new_paths = multi_save_dataset_stations(source_paths, block_length, block_length_factor=block_length_factor, compression=compression, max_workers=max_workers)

        return new_paths


    def upload_interim_results(self, source_paths, threads=10):
        """

        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            s3 = s3_client(self.connection_config, max_pool_connections=threads)
            futures = []
            for path in source_paths:
                f = executor.submit(tu.s3.put_interim_results_s3, s3, self.bucket, path, self.run_id, system_version=self.system_version)
                futures.append(f)
            runs = concurrent.futures.wait(futures)

        keys = [r.result() for r in runs[0]]

        self.interim_keys = keys

        ## Remove source files
        for path in source_paths:
            os.remove(path)

        ## diagnostic log
        # self.diagnostics['upload_interim_results'] = {'pass': True}
        # self.diagnostics['attributes'].update({'interim_keys': keys})

        return keys


    def get_interim_results_list(self, max_size_gb=0.1):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'status_checks')

        key_pattern = tdm.key_patterns[self.system_version]['interim_results'].split('{dataset_id}')[0]
        key = key_pattern.format(run_id=self.run_id)

        s3 = s3_client(self.connection_config)
        obj_list1 = tu.s3.list_objects_s3(s3, self.bucket, key)
        obj_list1 = obj_list1[['Key', 'Size']].rename(columns={'Key': 'key', 'Size': 'size'})

        obj_keys1 = obj_list1['key'].tolist()
        ds_keys2 = [k.split('/')[4] for k in obj_keys1]
        stn_keys2 = [k.split('/')[5].split('.')[0] for k in obj_keys1]

        obj_list1['dataset_id'] = ds_keys2
        obj_list1['station_id'] = stn_keys2

        # ds_sizes = obj_list1.groupby('dataset_id')['size'].sum().reset_index()
        ds_stn_sizes = obj_list1.groupby(['dataset_id', 'station_id'])['size'].sum().reset_index()
        ds_stn_sizes = ds_stn_sizes.sample(frac=1, ignore_index=True, random_state=1)

        # self.ds_sizes = ds_sizes
        # self.ds_stn_sizes = ds_stn_sizes
        # self.interim_objects = obj_list1

        max_size = max_size_gb * 1000000000

        ds_stn_sum = ds_stn_sizes['size'].sum()
        mean_size = ds_stn_sum/len(ds_stn_sizes)
        group_len = int(max_size//mean_size)
        df_len = len(ds_stn_sizes)

        grouper = np.repeat(np.arange((df_len//group_len)+1), group_len)

        grp1 = ds_stn_sizes.groupby(grouper[:df_len])
        ds_stn_groups = [v for k, v in grp1]

        interim_groups = []
        for df in ds_stn_groups:
            ig = pd.merge(df.drop('size', axis=1), obj_list1, on=['dataset_id', 'station_id'])
            interim_groups.append(ig)

        ## diagnostic log
        self.diagnostics['get_interim_results_list'] = {'pass': True}
        # self.diagnostics['attributes'].update({'interim_objects': obj_list1, 'ds_stn_sizes': ds_stn_sizes, 'ds_sizes': ds_sizes})

        return interim_groups


    def copy_interim_objs(self, source_paths, threads=20):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'get_interim_results_list')

        new_paths = copy_interim_objs(source_paths, self.preprocessed_path, threads=threads, connection_config=self.connection_config, bucket=self.bucket, public_url=self.public_url)

        ## diagnostic log
        self.diagnostics['copy_interim_objs'] = {'pass': True}

        return new_paths


    def save_new_results(self, source_paths, correct_times=False, max_workers=4):
        """

        """
        # tu.misc.diagnostic_check(self.diagnostics, 'merge_nc_files')
        tu.misc.diagnostic_check(self.diagnostics, 'process_versions')

        ## Put the big files first
        merge_list = [[p, os.path.getsize(p)] for p in list(set(source_paths))]
        merge_df = pd.DataFrame(merge_list, columns=['path', 'size'])

        source_paths1 = merge_df.sort_values('size', ascending=False).path.tolist()

        ## Iterate through files
        if max_workers <= 1:
            results_new_paths1 = []
            for source_path in source_paths1:
                ds_id = source_path.split('/')[-1].split('_')[0]
                metadata = self.datasets[ds_id]
                f = tu.processing.save_new_results(source_path, metadata, self.max_version_date, correct_times, self.system_version)
                results_new_paths1.extend(f)
        else:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                futures = []
                for source_path in source_paths1:
                    ds_id = source_path.split('/')[-1].split('_')[0]
                    metadata = self.datasets[ds_id]
                    f = executor.submit(tu.processing.save_new_results, source_path, metadata, self.max_version_date, correct_times, self.system_version)
                    futures.append(f)
                runs = concurrent.futures.wait(futures)

            ## process output
            results_new_paths1 = []
            extend = results_new_paths1.extend
            _ = [extend(r.result()) for r in runs[0]]

        results_new_paths1.sort()

        ## diagnostic log
        self.diagnostics['save_new_results'] = {'pass': True}

        return results_new_paths1


    def _determine_results_chunks_diffs(self, source_paths, remote, add_old=False):
        """

        """
        r_chunks = tu.s3.determine_results_chunks_diffs(source_paths, remote, add_old)

        self._results_chunks_diffs = r_chunks

        return r_chunks


    def update_conflicting_results(self, results_paths, threads=60, max_workers=4):
        """

        """
        tu.misc.diagnostic_check(self.diagnostics, 'save_new_results')

        ## Determine which chunks need to uploaded
        if isinstance(self.public_url, str):
            remote1 = {'bucket': self.bucket, 'public_url': self.public_url, 'version': self.system_version}
        else:
            remote1 = {'bucket': self.bucket, 'connection_config': self.connection_config, 'version': self.system_version}

        results_paths_set = set(results_paths)

        r_chunks = self._determine_results_chunks_diffs(list(results_paths_set), remote1, add_old=self._add_old)

        r_chunks1 = r_chunks[r_chunks['_merge'].isin(['conflict'])].copy()

        if not r_chunks1.empty:
            chunks = r_chunks1.to_dict('records')

            ## Download old chunks for comparisons
            remote2 = copy.deepcopy(remote1)
            _ = remote2.pop('version')
            remote2['cache'] = pathlib.Path(self.previous_path)

            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for chunk in chunks:
                    remote2['chunk'] = chunk
                    f = executor.submit(download_results, **remote2)
                    futures.append(f)
                runs = concurrent.futures.wait(futures)

            chunks1 = [r.result()['chunk'] for r in runs[0]]

            ## Update the results files
            if max_workers <= 1:
                updated_paths = []
                for chunk in chunks1:
                    ds_id = str(chunk).split('/')[-3]
                    metadata = self.datasets[ds_id]
                    p1 = tu.processing.update_compare_results(chunk, metadata, self.max_version_date, self.preprocessed_path)
                    updated_paths.append(p1)
            else:
                with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                    futures = []
                    for chunk in chunks1:
                        ds_id = str(chunk).split('/')[-3]
                        metadata = self.datasets[ds_id]
                        f = executor.submit(tu.processing.update_compare_results, chunk, metadata, self.max_version_date, self.preprocessed_path)
                        futures.append(f)
                    runs = concurrent.futures.wait(futures)

                updated_paths = [r.result() for r in runs[0]]

            ## Remove previous results
            for chunk in chunks1:
                if chunk.exists():
                    os.remove(chunk)

        else:
            updated_paths = []

        ## Combine updated paths with "new" paths
        new_data_paths = r_chunks[r_chunks['_merge'] == 'new']['file_path'].tolist()
        updated_paths.extend(new_data_paths)
        updated_paths.sort()

        ## Remove files labeled as "identical"
        ident1 = r_chunks[r_chunks['_merge'] == 'identical']

        if not ident1.empty:
            paths = ident1['file_path'].tolist()
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)

        ## diagnostic log
        self.diagnostics['update_conflicting_results'] = {'pass': True}

        return updated_paths


    def _update_results_chunks(self, results_paths, max_workers=4):
        """

        """
        ## checks
        tu.misc.diagnostic_check(self.diagnostics, 'save_new_results')

        add_old = self._add_old
        if self._add_old:
            tu.misc.diagnostic_check(self.diagnostics, 'update_conflicting_results')

        if isinstance(self.public_url, str):
            remote1 = {'bucket': self.bucket, 'public_url': self.public_url, 'version': self.system_version}
        else:
            remote1 = {'bucket': self.bucket, 'connection_config': self.connection_config, 'version': self.system_version}

        results_paths_set = set(results_paths)
        r_chunks = self._determine_results_chunks_diffs(list(results_paths_set), remote1)
        r_chunks1 = r_chunks[r_chunks['_merge'] == 'conflict']

        if not r_chunks1.empty:
            tu.misc.diagnostic_check(self.diagnostics, 'update_conflicting_results')

        ## Organise the paths
        paths_dict = {}
        for path in list(set(results_paths)):
            path1 = os.path.split(path)[1]
            ds_id, version_date1, stn_id, chunk_id, _, _ = path1.split('_')

            if ds_id in paths_dict:
                    paths_dict[ds_id].append(path)
            else:
                paths_dict[ds_id] = [path]

        ## Iterate through datasets
        futures = []

        for ds_id, stn_files in paths_dict.items():

            if ds_id in self.old_versions:
                old_versions = [v['version_date'] for v in self.old_versions[ds_id]]
            else:
                old_versions = []

            ## Get the old results chunks file
            if self.max_version_date in old_versions:
                old_rc_data = tu.s3.get_remote_results_chunks(self.bucket, s3=None, connection_config=self.connection_config, public_url=self.public_url, dataset_id=ds_id, version_date=self.max_version_date, system_version=self.system_version)
            elif add_old and (len(old_versions) > 0):
                previous_version_date = old_versions[-1]
                old_rc_data = tu.s3.get_remote_results_chunks(self.bucket, s3=None, connection_config=self.connection_config, public_url=self.public_url, dataset_id=ds_id, version_date=previous_version_date, system_version=self.system_version)
            else:
                old_rc_data = None

            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                f = executor.submit(tu.processing.update_results_chunks, stn_files, self.preprocessed_path, old_rc_data)
                futures.append(f)

        runs = concurrent.futures.wait(futures)

        rc_paths = [r.result() for r in runs[0]]

        self.results_chunks_paths = rc_paths

        ## diagnostic log
        self.diagnostics['update_results_chunks'] = {'pass': True}

        return rc_paths


    def _update_stations(self, results_paths, max_workers=4):
        """

        """
        ## Checks
        tu.misc.diagnostic_check(self.diagnostics, 'update_results_chunks')

        add_old = self._add_old

        ## Organise the paths
        paths_dict = {}
        for path in list(set(results_paths)):
            path1 = os.path.split(path)[1]
            ds_id, version_date1, stn_id, chunk_id, _, _ = path1.split('_')

            if ds_id in paths_dict:
                    paths_dict[ds_id].append(path)
            else:
                paths_dict[ds_id] = [path]

        rc_paths = self.results_chunks_paths.copy()

        rc_path_dict = {}
        for path in rc_paths:
            path1 = os.path.split(path)[1]
            ds_id = path1.split('_')[0]
            rc_path_dict[ds_id] = path

        ## Iterate through datasets
        futures = []

        for ds_id, data_paths in paths_dict.items():
            rc_path = rc_path_dict[ds_id]

            if ds_id in self.old_versions:
                old_versions = [v['version_date'] for v in self.old_versions[ds_id]]
            else:
                old_versions = []

            ## Get the old results chunks file
            if self.max_version_date in old_versions:
                old_stns_data = tu.s3.get_remote_stations(self.bucket, s3=None, connection_config=self.connection_config, public_url=self.public_url, dataset_id=ds_id, version_date=self.max_version_date, system_version=self.system_version)
            elif add_old and (len(old_versions) > 0):
                previous_version_date = old_versions[-1]
                old_stns_data = tu.s3.get_remote_stations(self.bucket, s3=None, connection_config=self.connection_config, public_url=self.public_url, dataset_id=ds_id, version_date=previous_version_date, system_version=self.system_version)
            else:
                old_stns_data = None

            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                f = executor.submit(tu.processing.update_stations, data_paths, rc_path, self.preprocessed_path, old_stns_data)
                futures.append(f)

        runs = concurrent.futures.wait(futures)

        stn_paths = [r.result() for r in runs[0]]

        self.stations_paths = stn_paths

        ## diagnostic log
        self.diagnostics['update_stations'] = {'pass': True}

        return stn_paths


    def _update_versions(self, max_workers=4):
        """

        """
        ## Checks
        tu.misc.diagnostic_check(self.diagnostics, 'update_stations')

        ## Determine what datasets are updated
        dataset_ids = []
        for d in self.results_chunks_paths:
            ds_id = os.path.split(d)[1].split('_')[0]
            dataset_ids.append(ds_id)

        ## Run versions update
        futures = []
        for dataset_id in dataset_ids:
            version_data1 = self.version_dict[dataset_id]

            ## Get the versions
            if dataset_id in self.old_versions:
                rv_key = tdm.utils.key_patterns[self.system_version]['versions'].format(dataset_id=dataset_id)

                v_obj1 = get_object_s3(rv_key, self.bucket, connection_config=self.connection_config, public_url=self.public_url)

                old_versions = read_json_zstd(v_obj1)
            else:
                old_versions = None

            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                f = executor.submit(tu.processing.update_versions, version_data1, self.preprocessed_path, old_versions)
                futures.append(f)

        runs = concurrent.futures.wait(futures)

        versions_paths = [r.result() for r in runs[0]]

        self.versions_paths = versions_paths

        ## diagnostic log
        self.diagnostics['update_versions'] = {'pass': True}

        return versions_paths


    def _update_datasets(self):
        """

        """
        ## Checks
        tu.misc.diagnostic_check(self.diagnostics, 'update_versions')

        ## Save the individual datasets
        ds_paths = []
        for stns_path in self.stations_paths:
            ds_id = os.path.split(stns_path)[1].split('_')[0]
            dataset = self.datasets[ds_id]
            ds_path = tu.processing.update_dataset(dataset, self.preprocessed_path, stns_path, self.system_version)
            ds_paths.append(ds_path)

        ## Process the agg dataset file
        # Get the old file
        dss_key = tdm.utils.key_patterns[self.system_version]['datasets']

        dss_obj = get_object_s3(dss_key, bucket=self.bucket, connection_config=self.connection_config, public_url=self.public_url, counter=2)

        if dss_obj is None:
            old_datasets = None
        else:
            old_datasets = read_json_zstd(dss_obj)

        # Process and save the new file
        dss_path = tu.processing.update_dataset_agg(ds_paths, self.preprocessed_path, old_datasets)

        ## diagnostic log
        self.diagnostics['update_datasets'] = {'pass': True}

        return ds_paths


    def update_auxiliary_objects(self, results_paths, max_workers=4):
        """

        """
        if len(results_paths) > 0:
            print('-- updating the results chunks...')
            rc_paths = self._update_results_chunks(results_paths, max_workers)

            print('-- updating the stations...')
            stns_paths = self._update_stations(results_paths, max_workers)

            print('-- updating the versions...')
            versions_paths = self._update_versions(max_workers)

            print('-- updating the datasets...')
            ds_paths = self._update_datasets()
        else:
            print('No results to update')


    def upload_final_objects(self, threads=60):
        """

        """
        ## Determine all the different files to upload
        rc_paths = glob.glob(os.path.join(self.preprocessed_path, '*results_chunks.json.zst'))

        if len(rc_paths) > 0:

            results_paths = glob.glob(os.path.join(self.preprocessed_path, '*results.nc.zst'))
            stns_paths = glob.glob(os.path.join(self.preprocessed_path, '*stations.json.zst'))
            v_paths = glob.glob(os.path.join(self.preprocessed_path, '*versions.json.zst'))
            ds_paths = glob.glob(os.path.join(self.preprocessed_path, '*dataset.json.zst'))
            dss_path = glob.glob(os.path.join(self.preprocessed_path, 'datasets.json.zst'))

            ## Checks
            tu.misc.diagnostic_check(self.diagnostics, 'update_datasets')

            ds_set = set()
            for p in results_paths:
                ds_id = os.path.split(p)[1].split('_')[0]
                ds_set.add(ds_id)

            if not (len(rc_paths) == len(stns_paths) == len(ds_paths) == len(ds_set) == len(v_paths)):
                raise ValueError('The number of auxillary files do not match up.')

            if len(dss_path) != 1:
                raise ValueError('There must be one datasets.json.zst file.')

            ## Prepare files to be uploaded
            all_paths = results_paths.copy()
            all_paths.extend(rc_paths)
            all_paths.extend(stns_paths)
            all_paths.extend(v_paths)
            all_paths.extend(ds_paths)
            all_paths.extend(dss_path)
            random.shuffle(all_paths)

            s3 = s3_client(self.connection_config, max_pool_connections=threads)

            s3_list = []
            append = s3_list.append
            for path in all_paths:
                dict1 = tu.processing.prepare_file_for_s3(path, s3, self.bucket, self.system_version)
                append(dict1)

            ## Iterate through the files
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []

                for s3_dict in s3_list:
                    f = executor.submit(tu.s3.put_file_s3, **s3_dict)
                    futures.append(f)

                runs = concurrent.futures.wait(futures)

            resp = [r.result() for r in runs[0]]

        else:
            print('There seems to be no useful files in the results path. Nothing will get uploaded and any files in the path will be removed.')
            resp = None

        ## Remove all files in the results path
        path1 = pathlib.Path(self.preprocessed_path)
        for path in path1.glob('*'):
            os.remove(path)

        return resp


    def clear_interim_results(self):
        """

        """
        prefix = tdm.utils.key_patterns[self.system_version]['interim_results'].split('{dataset_id}')[0].format(run_id=self.run_id)

        s3 = s3_client(self.connection_config)

        obj_list = tu.s3.list_object_versions_s3(s3, self.bucket, prefix)

        rem_keys = []
        for i, row in obj_list.iterrows():
            rem_keys.extend([{'Key': row['Key'], 'VersionId': row['VersionId']}])

        if len(rem_keys) > 0:
            ## Split them into 1000 key chunks
            rem_keys_chunks = np.array_split(rem_keys, int(np.ceil(len(rem_keys)/1000)))

            ## Run through and delete the objects...
            for keys in rem_keys_chunks:
                _ = s3.delete_objects(Bucket=self.bucket, Delete={'Objects': keys.tolist(), 'Quiet': True})

        print(str(len(rem_keys)) + ' objects removed')












################################
### Testing


   # def init_ray(self, num_cpus=1, include_dashboard=False, configure_logging=False, **kwargs):
    #     """

    #     """
    #     if ray.is_initialized():
    #         ray.shutdown()

    #     ray.init(num_cpus=num_cpus, include_dashboard=include_dashboard, configure_logging=configure_logging, **kwargs)

    #     @ray.remote
    #     def _load_result(dataset, result, run_date_key, other_attrs, discrete, other_closed, sum_closed, other_encoding):
    #         """

    #         """
    #         out1 = tu.processing.prepare_results_v02(dataset, result, run_date_key, sum_closed=sum_closed, other_closed=other_closed, discrete=discrete, other_attrs=other_attrs, other_encoding=other_encoding)

    #         return out1

    #     self._load_result = _load_result
    #     self._obj_refs = []


    # def shutdown_ray(self):
    #     ray.shutdown()


    # def load_results(self, results, sum_closed='right', other_closed='left', discrete=True, other_attrs=None, other_encoding=None, run_date=None):
    #     """

    #     """
    #     ## Dataset checks
    #     # ds_ids = list(results.keys())

    #     if isinstance(run_date, str):
    #         run_date_key = tu.misc.make_run_date_key(run_date)
    #     else:
    #         run_date_key = self.max_run_date_key

    #     r1 = [self._load_result.remote(self.datasets[r['dataset_id']], r['result'], run_date_key, other_attrs, discrete, other_closed, sum_closed, other_encoding) for r in results]
    #     # r2 = ray.get(r1)

    #     self._obj_refs.extend(r1)
