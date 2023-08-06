#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 13:30:43 2021

@author: mike
"""
import os
import numpy as np
import pandas as pd
import orjson
import tethys_data_models as tdm
from tethysts.utils import get_object_s3, read_json_zstd, s3_client
from tethys_utils.misc import make_run_date_key, path_date_parser, write_json_zstd
from tethysts import Tethys
from botocore import exceptions as bc_exceptions
from time import sleep
import pathlib
import concurrent.futures
import copy

############################################
### Parameters



############################################
### Functions


def put_object_s3(s3, bucket, key, obj, metadata, content_type, retries=5):
    """

    """
    counter = retries
    while counter > 0:
        try:
            obj2 = s3.put_object(Bucket=bucket, Key=key, Body=obj, Metadata=metadata, ContentType=content_type)
            break
        except bc_exceptions.ConnectionClosedError as err:
            print(err)
            counter = counter - 1
            if counter == 0:
                raise err
            print('...trying again...')
            sleep(5)
        except bc_exceptions.ConnectTimeoutError as err:
            print(err)
            counter = counter - 1
            if counter == 0:
                raise err
            print('...trying again...')
            sleep(5)

    obj2.update({'key': key, 'bucket': bucket})

    return obj2


def put_file_s3(s3, bucket, key, file_path, metadata, content_type, retries=5):
    """

    """
    with open(file_path, 'rb') as f:
        obj_out = put_object_s3(s3, bucket, key, f.read(), metadata, content_type, retries=retries)

    return obj_out


def copy_object_s3(s3, source_bucket, dest_bucket, source_key, dest_key, retries=5):
    """
    Copies an object in an S3 database to another location in an S3 database. They must have the same fundemental connection_config. All metadata is copied to the new object.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy_object
    """
    source_dict = {'Bucket': source_bucket, 'Key': source_key}

    counter = retries
    while counter > 0:
        try:
            resp = s3.copy_object(Bucket=dest_bucket, Key=dest_key, CopySource=source_dict, MetadataDirective='COPY')
            break
        except bc_exceptions.ConnectionClosedError as err:
            print(err)
            counter = counter - 1
            if counter == 0:
                raise err
            print('...trying again...')
            sleep(5)
        except bc_exceptions.ConnectTimeoutError as err:
            print(err)
            counter = counter - 1
            if counter == 0:
                raise err
            print('...trying again...')
            sleep(5)

    return resp


def multi_copy_object_s3(s3, source_bucket, dest_bucket, source_dest_keys, retries=5, threads=30):
    """
    Same as the copy_object_s3 except with multi threading. The input source_dest_keys must be a list of dictionaries with keys named source_key and dest_key.
    """
    keys = copy.deepcopy(source_dest_keys)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for key in keys:
            key['s3'] = s3
            key['source_bucket'] = source_bucket
            key['dest_bucket'] = dest_bucket
            f = executor.submit(copy_object_s3, **key)
            futures.append(f)
        runs = concurrent.futures.wait(futures)

    resp_list = [r.result() for r in runs[0]]

    return resp_list


def put_interim_results_s3(s3, bucket, file_path, run_id, system_version=4, retries=5):
    """

    """
    path1 = pathlib.Path(file_path)
    ds_id, stn_id, start_date = path1.stem.split('.')[0].split('_')
    key = tdm.utils.key_patterns[system_version]['interim_results'].format(run_id=run_id, dataset_id=ds_id, station_id=stn_id, start_date=start_date)

    stats = os.stat(file_path)
    run_date = pd.Timestamp(round(stats.st_mtime), unit='s')
    run_date_key = make_run_date_key(run_date)

    _ = put_file_s3(s3, bucket, key, file_path, {'run_date': run_date_key}, 'application/zstd', retries=retries)

    return key


def list_objects_s3(s3, bucket, prefix, start_after='', delimiter='', continuation_token='', date_format=None):
    """
    Wrapper S3 function around the list_objects_v2 base function with a Pandas DataFrame output.

    Parameters
    ----------
    s3_client : boto3.client
        A boto3 client object
    bucket : str
        The S3 bucket.
    prefix : str
        Limits the response to keys that begin with the specified prefix.
    start_after : str
        The S3 key to start after.
    delimiter : str
        A delimiter is a character you use to group keys.
    continuation_token : str
        ContinuationToken indicates to S3 that the list is being continued on this bucket with a token.

    Returns
    -------
    DataFrame
    """
    if s3._endpoint.host == 'https://vault.revera.co.nz':
        js = []
        while True:
            js1 = s3.list_objects(Bucket=bucket, Prefix=prefix, Marker=start_after, Delimiter=delimiter)

            if 'Contents' in js1:
                js.extend(js1['Contents'])
                if 'NextMarker' in js1:
                    start_after = js1['NextMarker']
                else:
                    break
            else:
                break

    else:
        js = []
        while True:
            js1 = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, StartAfter=start_after, Delimiter=delimiter, ContinuationToken=continuation_token)

            if 'Contents' in js1:
                js.extend(js1['Contents'])
                if 'NextContinuationToken' in js1:
                    continuation_token = js1['NextContinuationToken']
                else:
                    break
            else:
                break

    if js:
        f_df1 = pd.DataFrame(js)[['Key', 'LastModified', 'ETag', 'Size']].copy()
        if isinstance(date_format, str):
            f_df1['KeyDate'] = pd.to_datetime(f_df1.Key.apply(lambda x: path_date_parser(x, date_format)), utc=True, errors='coerce').dt.tz_localize(None)
        f_df1['ETag'] = f_df1['ETag'].str.replace('"', '')
        f_df1['LastModified'] = pd.to_datetime(f_df1['LastModified']).dt.tz_localize(None)
    else:
        if isinstance(date_format, str):
            f_df1 = pd.DataFrame(columns=['Key', 'LastModified', 'ETag', 'Size', 'KeyDate'])
        else:
            f_df1 = pd.DataFrame(columns=['Key', 'LastModified', 'ETag', 'Size'])

    return f_df1


def list_object_versions_s3(s3_client, bucket, prefix, start_after='', delimiter=None, date_format=None):
    """
    Wrapper S3 function around the list_object_versions base function with a Pandas DataFrame output.

    Parameters
    ----------
    s3_client : boto3.client
        A boto3 client object
    bucket : str
        The S3 bucket.
    prefix : str
        Limits the response to keys that begin with the specified prefix.
    start_after : str
        The S3 key to start at.
    delimiter : str or None
        A delimiter is a character you use to group keys.

    Returns
    -------
    DataFrame
    """
    js = []
    while True:
        if isinstance(delimiter, str):
            js1 = s3_client.list_object_versions(Bucket=bucket, Prefix=prefix, KeyMarker=start_after, Delimiter=delimiter)
        else:
            js1 = s3_client.list_object_versions(Bucket=bucket, Prefix=prefix, KeyMarker=start_after)

        if 'Versions' in js1:
            js.extend(js1['Versions'])
            if 'NextKeyMarker' in js1:
                start_after = js1['NextKeyMarker']
            else:
                break
        else:
            break

    if js:
        f_df1 = pd.DataFrame(js)[['Key', 'VersionId', 'IsLatest', 'LastModified', 'ETag', 'Size']].copy()
        if isinstance(date_format, str):
            f_df1['KeyDate'] = pd.to_datetime(f_df1.Key.apply(lambda x: path_date_parser(x, date_format)), utc=True, errors='coerce').dt.tz_localize(None)
        f_df1['ETag'] = f_df1['ETag'].str.replace('"', '')
        f_df1['LastModified'] = pd.to_datetime(f_df1['LastModified']).dt.tz_localize(None)
    else:
        if isinstance(date_format, str):
            f_df1 = pd.DataFrame(columns=['Key', 'VersionId', 'IsLatest', 'LastModified', 'ETag', 'Size', 'KeyDate'])
        else:
            f_df1 = pd.DataFrame(columns=['Key', 'VersionId', 'IsLatest', 'LastModified', 'ETag', 'Size'])

    return f_df1


# def put_dataset(dataset, bucket, s3=None, connection_config=None, public_url=None, system_version=4):
#     """

#     """
#     run_date_key = make_run_date_key()

#     dataset_id = dataset['dataset_id']

#     ## Get the stations agg
#     stns_key = tdm.utils.key_patterns[system_version]['stations'].format(dataset_id=dataset_id)

#     obj1 = get_object_s3(stns_key, bucket, s3, connection_config, public_url)
#     stns = read_json_zstd(obj1)

#     ## generate stats for the dataset metadata
#     ds_stats = stats_for_dataset_metadata(stns)

#     if dataset['result_type'] == 'time_series':
#         if 'spatial_resolution' in ds_stats:
#             ds_stats.pop('spatial_resolution')

#     dataset.update(ds_stats)

#     ## Add version number
#     dataset.update({'system_version': system_version})

#     ## Check and create dataset metadata
#     ds4 = tdm.dataset.Dataset(**dataset)

#     ds5 = orjson.loads(ds4.json(exclude_none=True))

#     ## Write the object
#     ds_obj = write_json_zstd(ds5)

#     ds_key = tdm.utils.key_patterns[system_version]['dataset'].format(dataset_id=dataset_id)

#     _ = put_object_s3(s3, bucket, ds_key, ds_obj, {'run_date': run_date_key}, 'application/json')

#     return ds5


# def get_remote_dataset(bucket, s3=None, connection_config=None, public_url=None, dataset_id=None, key=None, system_version=4):
#     """

#     """
#     if isinstance(dataset_id, str):
#         key = tdm.utils.key_patterns[system_version]['dataset'].format(dataset_id=dataset_id)
#     elif not isinstance(key, str):
#         raise ValueError('dataset_id must be passed or key must be passed.')

#     try:
#         obj1 = get_object_s3(key, bucket, s3, connection_config, public_url)
#         rem_ds = read_json_zstd(obj1)
#     except:
#         rem_ds = None

#     return rem_ds


def get_remote_stations(bucket, s3=None, connection_config=None, public_url=None, dataset_id=None, key=None, version_date=None, system_version=4):
    """

    """
    if isinstance(dataset_id, str):
        if isinstance(version_date, (str, pd.Timestamp)):
            vd = make_run_date_key(version_date)
            key = tdm.utils.key_patterns[system_version]['stations'].format(dataset_id=dataset_id, version_date=vd)
        else:
            key = tdm.utils.key_patterns[system_version]['latest_stations'].format(dataset_id=dataset_id)
    elif not isinstance(key, str):
        raise ValueError('dataset_id and station_id must be passed or key must be passed.')

    try:
        obj1 = get_object_s3(key, bucket, s3, connection_config, public_url)
        rem_stn = read_json_zstd(obj1)
    except:
        rem_stn = None

    return rem_stn


def get_remote_results_chunks(bucket, s3=None, connection_config=None, public_url=None, dataset_id=None, key=None, version_date=None, system_version=4):
    """

    """
    if isinstance(dataset_id, str):
        if isinstance(version_date, (str, pd.Timestamp)):
            vd = make_run_date_key(version_date)
            key = tdm.utils.key_patterns[system_version]['results_chunks'].format(dataset_id=dataset_id, version_date=vd)
        else:
            key = tdm.utils.key_patterns[system_version]['latest_results_chunks'].format(dataset_id=dataset_id)
    elif not isinstance(key, str):
        raise ValueError('dataset_id must be passed or key must be passed.')

    try:
        obj1 = get_object_s3(key, bucket, s3, connection_config, public_url)
        rem_ds = read_json_zstd(obj1)
    except:
        rem_ds = None

    return rem_ds


# def put_remote_stations(dataset_id, version_date, bucket, s3, public_url=None, system_version=4):
#     """
#     Needs to be updated to create the version specific stations and results chunks files.
#     """
#     stn_key = tdm.utils.key_patterns[system_version]['stations']
#     vd = make_run_date_key(version_date)
#     stn_prefix = stn_key.split('{station_id}')[0].format(dataset_id=dataset_id, verion_date=vd)

#     if system_version >= 4:
#         list1 = list_objects_s3(s3, bucket, stn_prefix, delimiter='/')
#     else:
#         raise ValueError('Wrong object structure version.')

#     list2 = list1[list1.Key.str.contains('station.json.zst')].copy()

#     if not list2.empty:

#         ## Get all of the result chunks from the individual stations
#         with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#             futures = []

#             for key in list2['Key'].tolist():
#                 f = executor.submit(get_remote_station, s3=s3, bucket=bucket, key=key, public_url=public_url, system_version=system_version)
#                 futures.append(f)

#             runs = concurrent.futures.wait(futures)

#         stn_list = [r.result() for r in runs[0]]

#         ## Remove the results chunks from the stations
#         rc_list = []
#         _ = [rc_list.extend(s.pop('results_chunks')) for s in stn_list]

#         ## Save files
#         # Stations
#         stns_obj = write_json_zstd(stn_list)

#         run_date_key = make_run_date_key()

#         agg_stn_key = tdm.utils.key_patterns[system_version]['stations']

#         stns_key = agg_stn_key.format(dataset_id=dataset_id, verion_date=vd)

#         _ = put_object_s3(s3, bucket, stns_key, stns_obj, {'run_date': run_date_key}, 'application/json')

#         # Results chunks
#         rc_obj = write_json_zstd(rc_list)

#         agg_rc_key = tdm.utils.key_patterns[system_version]['results_chunks']

#         rc_key = agg_rc_key.format(dataset_id=dataset_id, verion_date=vd)

#         _ = put_object_s3(s3, bucket, rc_key, rc_obj, {'run_date': run_date_key}, 'application/json')

#         return stn_list
#     else:
#         print('There are no stations files in the database.')
#         return None


# def put_remote_agg_datasets(bucket, s3, public_url=None, threads=30, system_version=4):
#     """

#     """
#     ds_key = tdm.utils.key_patterns[system_version]['dataset']

#     ds_prefix = ds_key.split('{dataset_id}')[0]

#     if system_version == 2:
#         list1 = list_objects_s3(s3, bucket, ds_prefix)
#     elif system_version >= 3:
#         list1 = list_objects_s3(s3, bucket, ds_prefix, delimiter='/')
#     else:
#         raise ValueError('Wrong object structure version.')

#     list2 = list1[list1.Key.str.contains('dataset.json.zst')].copy()

#     if not list2.empty:

#         with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#             futures = []

#             for key in list2['Key'].tolist():
#                 f = executor.submit(get_remote_dataset, s3=s3, bucket=bucket, public_url=public_url, key=key, system_version=system_version)
#                 futures.append(f)

#             runs = concurrent.futures.wait(futures)

#         ds_list = [r.result() for r in runs[0]]

#         dss_obj = write_json_zstd(ds_list)

#         run_date_key = make_run_date_key()
#         dss_key = tdm.utils.key_patterns[system_version]['datasets']

#         _ = put_object_s3(s3, bucket, dss_key, dss_obj, {'run_date': run_date_key}, 'application/json')

#     return ds_list


# def update_versions(version_data, bucket, connection_config=None, public_url=None, system_version=4):
#     """

#     """
#     ## Check version_dict data model
#     version_dict1 = tdm.dataset.ResultVersion(**version_data).dict(exclude_none=True)

#     ## Initial set up
#     # s3 = s3_client(connection_config)

#     dataset_id = version_dict1['dataset_id']

#     ## Get the versions
#     rv_key = tdm.utils.key_patterns[system_version]['versions'].format(dataset_id=dataset_id)

#     v_obj1 = get_object_s3(rv_key, bucket, connection_config=connection_config, public_url=public_url, counter=5)

#     if v_obj1 is not None:
#         v2 = read_json_zstd(v_obj1)

#         exists = any([version_dict1['version_date'].isoformat() == v['version_date'] for v in v2])

#         if exists:
#             version_list = []
#             for v in v2:
#                 if version_dict1['version_date'].isoformat() == v['version_date']:
#                     version_list.append(version_dict1)
#                 else:
#                     version_list.append(v)
#         else:
#             version_list = v2.copy()
#             version_list.append(version_dict1)
#     else:
#         version_list = [version_dict1]

#     ## Save files
#     # run_date_key = make_run_date_key()

#     # # versions
#     # rv_obj = write_json_zstd(version_list)

#     # _ = put_object_s3(s3, bucket, rv_key, rv_obj, {'run_date': run_date_key}, 'application/json')

#     return version_list


# def update_station_s3(stn_data, bucket, connection_config, public_url=None, system_version=4):
#     """

#     """
#     ## Check version_dict data model
#     stn_dict1 = tdm.dataset.Station(**stn_data).dict(exclude_none=True)

#     ## Initial set up
#     s3 = s3_client(connection_config)

#     dataset_id = stn_dict1['dataset_id']
#     stn_id = stn_dict1['station_id']

#     ## Get the versions
#     stn_key = tdm.utils.key_patterns[system_version]['station'].format(dataset_id=dataset_id, station_id=stn_id)

#     stn_obj1 = get_object_s3(stn_key, bucket, s3=s3, public_url=public_url, counter=1)

#     if stn_obj1 is not None:
#         s2 = read_json_zstd(stn_obj1)

#         stn_list = []
#         for s in s2:
#             if stn_dict1['version_date'] == v['version_date']:
#                 version_list.append(version_dict1)
#             else:
#                 version_list.append(v)
#     else:
#         stn_dict2 = stn_dict1

#     ## Save files
#     run_date_key = make_run_date_key()

#     # versions
#     stn_obj = write_json_zstd(stn_dict2)

#     _ = put_object_s3(s3, bucket, stn_key, stn_obj, {'run_date': run_date_key}, 'application/json')

#     return stn_dict2


# def put_result(s3, bucket, results_path, system_version=4):
#     """

#     """
#     file_name = os.path.split(results_path)[1]
#     ds_id, version_date_key, stn_id, chunk_id, _, _ = file_name.split('_')

#     key_name = tdm.utils.key_patterns[system_version]['results'].format(dataset_id=ds_id, version_date=version_date_key, station_id=stn_id, chunk_id=chunk_id)

#     run_date_key = make_run_date_key()

#     metadata = {'run_date': run_date_key}

#     _ = put_file_s3(s3, bucket, key_name, results_path, metadata, 'application/zstd', retries=5)

#     return key_name


# def put_station(s3, bucket, stn_path, system_version=4):
#     """

#     """
#     file_name = os.path.split(stn_path)[1]
#     ds_id, version_date_key, stn_id, _ = file_name.split('_')

#     key_name = tdm.utils.key_patterns[system_version]['station'].format(dataset_id=ds_id, version_date=version_date_key, station_id=stn_id)

#     run_date_key = make_run_date_key()

#     metadata = {'run_date': run_date_key}

#     _ = put_file_s3(s3, bucket, key_name, stn_path, metadata, 'application/zstd', retries=5)

#     return key_name


def delete_dataset_s3(conn_config, bucket, dataset_id, system_version=4):
    """
    Function to delete Tethys result objects including all object versions.

    Parameters
    ----------
    conn_config : dict
        A dictionary of the connection info necessary to establish an S3 connection.
    bucket : str
        The s3 bucket.
    dataset_id : str
        The specific dataset that should be removed.

    Returns
    -------
    list of keys deleted
    """
    s3 = s3_client(conn_config)

    ## Update/Remove the dataset from the master datasets file
    dss_key = tdm.utils.key_patterns[system_version]['datasets']

    dss_obj = get_object_s3(dss_key, bucket, s3)

    rem_keys = []

    if dss_obj is not None:
        dss_list = read_json_zstd(dss_obj)

        dss_list_new = []
        for dss in dss_list:
            if dss['dataset_id'] != dataset_id:
                dss_list_new.append(dss)

        if len(dss_list_new) > 0:
            content_type = 'application/json'

            run_date_key = make_run_date_key()
            metadata = {'run_date': run_date_key}

            dss_obj_new = write_json_zstd(dss_list_new)

            resp = put_object_s3(s3, bucket, dss_key, dss_obj_new, metadata, content_type)
        else:
            obj_list = list_object_versions_s3(s3, bucket, dss_key)
            obj_del = obj_list[['Key', 'VersionId']].to_dict('records')
            resp = s3.delete_objects(Bucket=bucket, Delete={'Objects': obj_del, 'Quiet': True})
            rem_keys.extend(obj_del)

        ## Remove all of the other objects
        del_results = tdm.utils.key_patterns[system_version]['results'].split('{version_date}')[0].format(dataset_id=dataset_id)
        del_versions = tdm.utils.key_patterns[system_version]['versions'].format(dataset_id=dataset_id)
        del_dataset = tdm.utils.key_patterns[system_version]['dataset'].format(dataset_id=dataset_id)

        del_list = [del_dataset, del_versions, del_results]

        for prefix in del_list:

            obj_list = list_object_versions_s3(s3, bucket, prefix)

            if not obj_list.empty:
                obj_del = obj_list[['Key', 'VersionId']].to_dict('records')

                ## Split them into 1000 key chunks
                rem_keys_chunks = np.array_split(obj_del, int(np.ceil(len(obj_del)/1000)))

                ## Run through and delete the objects...
                for keys in rem_keys_chunks:
                    resp = s3.delete_objects(Bucket=bucket, Delete={'Objects': keys.tolist(), 'Quiet': True})

                rem_keys.extend(obj_del)
    else:
        print('No dataset found with the given dataset_id.')

    return rem_keys


def process_dataset_versions(dataset_list, bucket, version_data, s3=None, connection_config=None, public_url=None, system_version=4):
    """
    Function to process the run date keys for all datasets for the extraction.

    Parameters
    ----------
    dataset_list : list of dict
        The list of datasets, which is the output of the process_datasets function.
    remote : dict
        Dict of a connection_config and bucket:
        conn_config : dict
            A dictionary of the connection info necessary to establish an S3 connection.
        bucket : str
            The S3 bucket.

    Returns
    -------
    run_date_dict : dict of str
    """
    remote1 = dict(s3=s3, connection_config=connection_config, public_url=public_url, bucket=bucket, version=system_version)

    ## Build the ResultVersion model
    mod_date = pd.Timestamp.today(tz='utc').tz_localize(None).round('s')

    if isinstance(version_data['version_date'], str):
        version_data['version_date'] = pd.Timestamp(version_data['version_date'])

    version_data['modified_date'] = mod_date

    version_dict = {}
    for ds in dataset_list:
        dataset_id = ds['dataset_id']
        vd = version_data.copy()
        vd['dataset_id'] = dataset_id
        version_m = tdm.dataset.ResultVersion(**vd)
        version_dict[dataset_id] = orjson.loads(version_m.json(exclude_none=True))

    ## Check to make sure that the passed version date is not earlier than existing versions
    t1 = Tethys([remote1])
    datasets = t1._datasets

    old_versions = {}

    for ds_id, vd in version_dict.items():
        if ds_id in datasets:
            new_date = pd.Timestamp(vd['version_date'])
            vd_old = t1.get_versions(ds_id)
            old_date = pd.to_datetime([pd.Timestamp(v['version_date']) for v in vd_old]).max()
            if new_date < old_date:
                raise ValueError('The new version date is prior to the max old version date. New version date: {new_date}; old max version date: {old_date}. dataset_id: {ds_id}.'.format(new_date=new_date.isoformat(), old_date=old_date.isoformat(), ds_id=ds_id))
            old_versions[ds_id] = vd_old

    return version_dict, old_versions


# def reprocess_datasets(dataset, conn_config, bucket, public_url, threads=20):
#     """

#     """
#     dataset_id = dataset['dataset_id']
#     tethys = Tethys([{'connection_config': public_url, 'bucket': bucket, 'version': 2}])

#     stns = tethys.get_stations(dataset_id, results_object_keys=True)

#     bad_stns = [s for s in stns if 'time_range' not in s]

#     prefix = tdm.utils.key_patterns[2]['results'].split('{station_id}')[0].format(dataset_id=dataset_id)

#     s3 = s3_client(conn_config)
#     keys1 = list_objects_s3(s3, bucket, prefix)
#     obj_df1 = keys1[keys1.Key.str.contains('results.nc')].copy()
#     obj_df1['station_id'] = obj_df1['Key'].apply(lambda x: x.split('/')[3])


#     def reprocess_dataset(stn):
#         """

#         """
#         stn_id = stn['station_id']
#         run_dates = tethys.get_run_dates(dataset_id, stn['station_id'])

#         for run_date in run_dates:

#         # run_date = stn['results_object_key']['run_date']
#             run_date_key = make_run_date_key(run_date)
#             mod_date_key = make_run_date_key()
#             up1 = tethys.get_results(dataset_id, stn_id, run_date=run_date, output='Dataset')

#             key_dict = {'dataset_id': dataset_id, 'station_id': stn_id, 'run_date': run_date_key}

#             new_key = tdm.utils.key_patterns[2]['results'].format(**key_dict)

#             cctx = zstd.ZstdCompressor(level=1)
#             c_obj = cctx.compress(up1.to_netcdf())

#             obj_resp = put_object_s3(s3, bucket, new_key, c_obj, {'run_date': mod_date_key}, 'application/zstd')

#             ## Process stn data
#             # print('Save station data')

#         ## Process object key infos
#         stn_obj_df1 = obj_df1[obj_df1['station_id'] == stn_id].drop(['LastModified', 'station_id'], axis=1).copy()
#         keys = stn_obj_df1['Key'].unique()
#         new_key_info = [new_key, obj_resp['ResponseMetadata']['HTTPHeaders']['etag'].replace('"', ''), len(c_obj), pd.Timestamp(run_date_key).tz_localize(None)]

#         if new_key in keys:
#             stn_obj_df1[stn_obj_df1['Key'] == new_key] = new_key_info
#         else:
#             stn_obj_df1.loc[len(stn_obj_df1)] = new_key_info

#         info1 = [S3ObjectKey(key=row['Key'], bucket=bucket, content_length=row['Size'], etag=row['ETag'], run_date=row['KeyDate']) for i, row in stn_obj_df1.iterrows()]

#         ## Final station processing and saving
#         stn_m = process_station_summ(up1, info1, mod_date=mod_date_key)

#         up_stns = put_remote_station(s3, bucket, stn_m, run_date=mod_date_key, version=2)


#     if len(bad_stns) > 0:
#         print('Updating results and stations...')
#         output = ThreadPool(threads).map(reprocess_dataset, bad_stns)

#         print('Updating aggregates...')

#         ds_stations = put_remote_agg_stations(s3, bucket, dataset_id, threads*2, version=2)
#         if ds_stations is not None:
#             ds_new = put_remote_dataset(s3, bucket, dataset, ds_stations, version=2)

#         # Aggregate all datasets for the bucket
#         ds_all = put_remote_agg_datasets(s3, bucket, threads*2, version=2)

#     else:
#         print('Nothing to update.')

#     print('Finished')


def determine_results_chunks_diffs(source_paths, remote, add_old=False):
    """

    """
    paths1 = []
    for p in source_paths:
        ds_id, version_date1, stn_id, chunk_id, hash_id, _ = os.path.split(p)[1].split('_')
        paths1.append([p, ds_id, version_date1, stn_id, chunk_id, hash_id])

    paths2 = pd.DataFrame(paths1, columns=['file_path', 'dataset_id', 'version_date', 'station_id', 'chunk_id', 'chunk_hash'])
    paths2['version_date'] = pd.to_datetime(paths2['version_date']).dt.tz_localize(None)

    tethys = Tethys([remote])
    datasets = tethys._datasets

    diffs_list = []
    for ds_id, g in paths2.groupby('dataset_id'):
        # print(ds_id)

        if ds_id in datasets:
            # dataset = datasets[ds_id]
            # method = dataset['method']
            vd_old = tethys.get_versions(ds_id)
            vd_max = g.version_date.max()

            # Check to make sure new version data is greater or equal to old dates
            vd0 = [vd['version_date'] for vd in vd_old if pd.Timestamp(vd['version_date']) <= vd_max]

            if not vd0:
                raise ValueError('The new version date must be greater than or equal to the old version dates.')

            # Determine what version date to use
            vd1 = [vd['version_date'] for vd in vd_old if pd.Timestamp(vd['version_date']) == vd_max]

            if len(vd1) > 0:
                vd = vd1[-1]
                merge_vals = ['conflict', 'new']
            else:
                if add_old:
                    vd = vd_old[-1]['version_date']
                    merge_vals = ['conflict', 'new', 'old']
                else:
                    g['key'] = np.nan
                    g['_merge'] = 'new'
                    diffs_list.append(g)
                    continue

            # Load in the results chunks
            vd_key = make_run_date_key(vd)
            rc_key = tdm.utils.key_patterns[4]['results_chunks'].format(dataset_id=ds_id, version_date=vd_key)

            s_remote = copy.deepcopy(remote)
            _ = s_remote.pop('version')
            s_remote['obj_key'] = rc_key

            rc_obj = get_object_s3(**s_remote)
            chunks1 = read_json_zstd(rc_obj)

            chunks_df = pd.DataFrame(chunks1).drop(['version_date', 'content_length', 'height', 'chunk_day'], axis=1).rename(columns={'chunk_hash': 'original_chunk_hash'})

            # Combine to determine which chunks should be assessed
            combo1 = pd.merge(g, chunks_df, on=['dataset_id', 'station_id', 'chunk_id'], indicator=True, how='outer')
            combo1 = combo1.replace({'_merge': {'both': 'conflict', 'left_only': 'new', 'right_only': 'old'}})
            combo1 = combo1[combo1['_merge'].isin(merge_vals)].copy()
            combo1['version_date'] = vd_max

            combo1['_merge'] = combo1['_merge'].cat.set_categories(['identical', 'conflict', 'new', 'old'])
            combo1.loc[combo1['chunk_hash'] == combo1['original_chunk_hash'], '_merge'] = 'identical'

            diffs_list.append(combo1.drop(['original_chunk_hash'], axis=1))
        else:
            g['key'] = np.nan
            g['_merge'] = 'new'
            diffs_list.append(g)

    combo2 = pd.concat(diffs_list)

    return combo2


# def update_latest_stations(dataset_id, bucket, s3, public_url=None, threads=60, system_version=4):
#     """

#     """
#     ## Get the versions
#     rv_key = tdm.utils.key_patterns[system_version]['versions'].format(dataset_id=dataset_id)

#     v_obj1 = get_object_s3(rv_key, bucket, s3=s3, public_url=public_url, counter=2)

#     if v_obj1 is not None:
#         v2 = read_json_zstd(v_obj1)

#         last_version_date = max([v['version_date'] for v in v2])

#         ## Update all of the individual station objects
#         # stn_key_str = tdm.utils.key_patterns[system_version]['station']
#         # vd = make_run_date_key(version_date)
#         # stn_prefix = stn_key_str.split('{station_id}')[0].format(dataset_id=dataset_id, verion_date=vd)
#         #
#         # if system_version >= 4:
#         #     list1 = list_objects_s3(s3, bucket, stn_prefix, delimiter='/')
#         # else:
#         #     raise ValueError('Wrong object structure version.')
#         #
#         # list2 = list1[list1.Key.str.contains('station.json.zst')].copy()
#         #
#         # source_dest_keys = []
#         # for key in list2['Key'].tolist():
#         #     stn_id = key.split('/')[4].split('.')[0]
#         #     stn_key = stn_key_str.format(dataset_id=dataset_id, verion_date=vd, station_id=stn_id)
#         #     dict1 = {'source_key': key, 'dest_key': stn_key}
#         #     source_dest_keys.append(dict1)
#         #
#         # resp_list = multi_copy_object_s3(s3, bucket, bucket, source_dest_keys, retries=5, threads=threads)

#         ## Update the stations object
#         stns_key_str = tdm.utils.key_patterns[system_version]['stations']
#         vd = make_run_date_key(last_version_date)
#         stns_key = stns_key_str.format(dataset_id=dataset_id, verion_date=vd)

#         dest_key_str = tdm.utils.key_patterns[system_version]['latest_stations']
#         dest_key = dest_key_str.format(dataset_id=dataset_id)

#         stn_resp = copy_object_s3(s3, bucket, bucket, stns_key, dest_key)

#         ## Update the results_chunks object
#         rc_key_str = tdm.utils.key_patterns[system_version]['results_chunks']
#         vd = make_run_date_key(last_version_date)
#         rc_key = rc_key_str.format(dataset_id=dataset_id, verion_date=vd)

#         dest_key_str = tdm.utils.key_patterns[system_version]['latest_results_chunks']
#         dest_key = dest_key_str.format(dataset_id=dataset_id)

#         rc_resp = copy_object_s3(s3, bucket, bucket, rc_key, dest_key)

#         return True
#     else:
#         return False




# for ds in titan.dataset_list:
#     reprocess_datasets(ds['dataset_id'], conn_config, bucket, public_url, threads=20)





# for result in results[2500:]:
#     new1 = xr.load_dataset(read_pkl_zstd(result, False))
#
#     stn_id = str(new1.squeeze()['station_id'].values)
#     print('station_id: ' + stn_id)
#
#     vars1 = list(new1.variables)
#     parameter = [v for v in vars1 if 'dataset_id' in new1[v].attrs][0]
#     result_attrs = new1[parameter].attrs.copy()
#
#     ds_id = result_attrs['dataset_id']
#     mod_date_key = new1.attrs['history'].split(':')[0]
#
#     if no_comparison:
#         up1 = new1
#     else:
#         last_date_key_df = last_date1[last_date1['station_id'] == stn_id]
#         if last_date_key_df.empty:
#             last_date_key = None
#         else:
#             last_date_key = make_run_date_key(last_date_key_df['KeyDate'].iloc[0])
#
#         up1 = compare_datasets_from_s3(conn_config, bucket, new1, add_old=add_old, last_run_date_key=last_date_key, public_url=public_url)
#
#     ## Save results
#     if isinstance(up1, xr.Dataset) and (len(up1[parameter].time) > 0):
#
#         # print('Save results')
#         key_dict = {'dataset_id': ds_id, 'station_id': stn_id, 'run_date': run_date_key}
#
#         new_key = tdm.utils.key_patterns['results'].format(**key_dict)
#
#         cctx = zstd.ZstdCompressor(level=1)
#         c_obj = cctx.compress(up1.to_netcdf())
#
#         obj_resp = s3.put_object(Body=c_obj, Bucket=bucket, Key=new_key, ContentType='application/zstd', Metadata={'run_date': mod_date_key})
#
#         ## Process stn data
#         # print('Save station data')
#
#         ## Process object key infos
#         stn_obj_df1 = obj_df1[obj_df1['station_id'] == stn_id].drop(['LastModified', 'station_id'], axis=1).copy()
#         keys = stn_obj_df1['Key'].unique()
#         new_key_info = [new_key, obj_resp['ResponseMetadata']['HTTPHeaders']['etag'].replace('"', ''), len(c_obj), pd.Timestamp(run_date_key).tz_localize(None)]
#
#         if new_key in keys:
#             stn_obj_df1[stn_obj_df1['Key'] == new_key] = new_key_info
#         else:
#             stn_obj_df1.loc[len(stn_obj_df1)] = new_key_info
#
#         info1 = [S3ObjectKey(key=row['Key'], bucket=bucket, content_length=row['Size'], etag=row['ETag'], run_date=row['KeyDate']) for i, row in stn_obj_df1.iterrows()]
#
#         ## Final station processing and saving
#         stn_m = process_station_summ(ds_id, stn_id, up1, info1, mod_date=mod_date_key)
#
#         up_stns = put_remote_station(s3, bucket, stn_m, run_date=mod_date_key)
#
#     else:
#         print('No new data to update')
#
#     ## Get rid of big objects
#     new1 = None
#     up1 = None
