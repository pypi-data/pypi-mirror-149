tethys-utils
==================================

This git repository contains the main class Titan and supporting classes and functions for processing data to be put into Tethys.

Improvements
------------
Some optimizations on the querying of datasets that do not exist in the S3 remote could be improved. More specifically, the first time a dataset (or any datasets in the remote bucket) is being processed, some methods in Titan tries to find files that do not exist in the S3 remote. There are several failed attempts to access these files, then it moves on. Knowing early on that there are no existing datasets and not repeatedly querying empty files would be more nicer. Though in most cases, this is not a significant issues as this only affects the first time a dataset is saved.
