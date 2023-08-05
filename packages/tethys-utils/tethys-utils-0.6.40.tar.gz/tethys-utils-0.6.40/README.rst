tethys-utils
==================================

This git repository contains the main class Titan and supporting functions for processing data to be put into Tethys.

Improvements
------------
The functions to process gridded model data is well designed and optimized.

Creating new versions for monitoring data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The biggest issue is with the monitoring data and multiple versions (i.e. quality controlled monitoring data). The currently implementation to save a new version with all of the old results is complicated and inefficient. Since the current implementation to update the station data requires that all of the results files be present locally, all of the old results must be downloaded and re-uploaded. I have a function to be able to directly copy S3 objects, and this would seem like a more optimal option. But then I'd need to change the update stations function to...copy the old results chunks data to the new version.

Station data in results chunks not updated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Again...this is primarily a problem for monitoring data...if station data changes over time, then the newer results chunks will reflex these changes, but older chunks will not. Depending on the get_results request, some station data might be different.
