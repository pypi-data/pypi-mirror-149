import os, sys, shutil, random, math, atexit, time
from collections import OrderedDict
import functools
from functools import reduce
from osgeo import gdal, osr, ogr
import numpy as np
import random
import multiprocessing
import multiprocessing.pool
import hazelbean as hb
import scipy
import geopandas as gpd
import warnings
import netCDF4
import logging
import pandas as pd
import pygeoprocessing.geoprocessing as pgp
from pygeoprocessing.geoprocessing import *

# Conditional imports
try:
    import geoecon as ge
except:
    ge = None

numpy = np
L = hb.get_logger('hb_rasterstats')
pgp_logger = logging.getLogger('geoprocessing')

loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

def convert_polygons_to_id_raster(input_vector_path, output_raster_path, match_raster_path,
                                  id_column_label=None, data_type=None, ndv=None, all_touched=None, compress=True):

    hb.assert_file_existence(input_vector_path)
    hb.assert_file_existence(match_raster_path)
    if not id_column_label:
        # Get the column label of the first column
        gdf = gpd.read_file(input_vector_path)
        id_column_label = gdf.columns[0]

    if not data_type:
        data_type = 1

    if not ndv:
        ndv = 255
    band_nodata_list = [ndv]

    option_list = list(hb.DEFAULT_GTIFF_CREATION_OPTIONS)
    if all_touched:
        option_list.append("ALL_TOUCHED=TRUE")

    option_list.append("ATTRIBUTE=" + str(id_column_label))
    raster_option_list = [i for i in option_list if 'ATTRIBUTE=' not in i and 'ALL_TOUCHED' not in i]
    if compress:
        option_list.append("COMPRESS=DEFLATE")
    hb.new_raster_from_base_pgp(match_raster_path, output_raster_path, data_type, band_nodata_list, gtiff_creation_options=raster_option_list)
    burn_values = [1]  # will be ignored because attribute set but still needed.

    # option_list = []


    # The callback here is useful, but rather than rewrite the funciton, we just locallay reset the PGP logger level.
    prior_level = pgp_logger.getEffectiveLevel()
    pgp_logger.setLevel(logging.INFO)
    pgp.rasterize(input_vector_path, output_raster_path, burn_values, option_list, layer_id=0)
    pgp_logger.setLevel(prior_level)


def zonal_statistics_flex(input_raster,
                          zones_vector_path,
                          zone_ids_raster_path=None,
                          id_column_label=None,
                          zones_raster_data_type=None,
                          values_raster_data_type=None,
                          zones_ndv=None,
                          values_ndv=None,
                          all_touched=None,
                          assert_projections_same=True,
                          unique_zone_ids=None,
                          output_column_prefix=None,
                          csv_output_path=None,
                          vector_output_path=None,
                          stats_to_retrieve='sums',
                          enumeration_classes=None,
                          enumeration_labels=None,
                          multiply_raster_path=None,
                          verbose=False,
                          rewrite_zone_ids_raster=True,
                          vector_columns_to_include_in_output=None,
                          vector_index_column=None,
                          max_enumerate_value=1000,
                          ):
    """

    # LEGACY FUNCTION, replaced by zonal_statistics

    :param input_raster: flexible input, but it needs to be able to be returned as a path by get_flex_as_path
    :param zones_vector_path: path to GPKG file that contains the zone definition.

    :param zone_ids_raster_path:
    If not provided, function will assume that you want the slower pygeoprocessing version that does extra features,
    for instance allowing polygons to overlap. If path given, but the path isn't a raster, it will create it from the vector.
    If path is given and it exists, it will assume it is a valid ID raster generated for the vector.

    :param id_column_label:
    Which column from the vector to write to the ID raster.

    :param zones_raster_data_type:
    :param values_raster_data_type:
    :param zones_ndv:
    :param values_ndv:
    :param all_touched: When rasterizing the vector, should it yuse the midpoint or all-touched definition of rasterization.
    :param assert_projections_same:

    :param unique_zone_ids:
    If given, will return statistics for these exact zones. Note that this is a highly-optimized object and must be
    Continuous, start at zero, and include the max value of Zones. If this is None, it will generate one
    (which calls np.unique() which can be slow).

    :param csv_output_path:
    :param vector_output_path:

    :param stats_to_retrieve: Sum, sum_count, enumeration
    If enumeration, it will interpret the value raster as having categorized data and will instead output the number of instances of
    each category for each zone. Enumeration classes below will control which of the values in the

    :param enumeration_classes:
    :param multiply_raster_path:
    :param verbose:
    :param rewrite_zone_ids_raster:
    :param max_enumerate_value:
    :return:
    """



    """ if zone_ids_raster_path is set, use it and/or create it for later processing speed-ups.

     Big caveat on unique_zone_ids: must start at 1 and be sequential by zone. Otherwise, if left None, will just test first 10000 ints. This speeds up a lot not having to have a lookup.
     """

    input_path = hb.get_flex_as_path(input_raster)
    base_raster_path_band = (input_path, 1)

    # Test that input_raster and shapefile are in the same projection. Sillyness results if not.
    if assert_projections_same:
        hb.assert_gdal_paths_in_same_projection([input_raster, zones_vector_path])
    else:
        if verbose:
            a = hb.assert_gdal_paths_in_same_projection([input_raster, zones_vector_path], return_result=True)
            if not a:
                L.critical('Ran zonal_statistics_flex but the inputs werent in identical projections.')
        else:
            pass

  # if zone_ids_raster_path is not defined, use the PGP version, which doesn't use a rasterized approach.
    if not zone_ids_raster_path and rewrite_zone_ids_raster is False:
        to_return = pgp.zonal_statistics(
            base_raster_path_band, zones_vector_path,
            aggregate_layer_name=None, ignore_nodata=True,
            polygons_might_overlap=True, working_dir=None)
        if csv_output_path is not None:
            hb.python_object_to_csv(to_return, csv_output_path)
        return to_return

    # if zone_ids_raster_path is defined, then we are using a rasterized approach.
    # NOTE that by construction, this type of zonal statistics cannot handle overlapping polygons (each polygon is just represented by its id int value in the raster).
    else:
        if zones_ndv is None:
            zones_ndv = -9999

    if values_ndv is None:
        values_ndv = hb.get_raster_info_hb(input_raster)['nodata'][0]

    # Double check in case get_Raster fails
    if values_ndv is None:
        values_ndv = -9999.0
    # if zone_ids_raster_path is not set, make it a temporary file
    if zone_ids_raster_path is None:
        zone_ids_raster_path = 'zone_ids_' + hb.random_string() + '.tif'

    # if zone_ids_raster_path is given, use it to speed up processing (creating it first if it doesnt exist)
    if not hb.path_exists(zone_ids_raster_path) and rewrite_zone_ids_raster is not False:
        # Calculate the id raster and save it
        if verbose:
            L.info('Creating id_raster with convert_polygons_to_id_raster')
        hb.convert_polygons_to_id_raster(zones_vector_path, zone_ids_raster_path, input_raster, id_column_label=id_column_label, data_type=zones_raster_data_type,
                                         ndv=zones_ndv, all_touched=all_touched)
    else:
        if verbose:
            L.info('Zone_ids_raster_path existed, so not creating it.')

        # hb.assert_gdal_paths_have_same_geotransform([zone_ids_raster_path, input_raster])
    if unique_zone_ids is None:

        # LEARNING POINT, If you read a GPKG, it will automatically convert the FID into the DF ID. This means the ID is not available to, e.g., merge on and has to be an index merge. One option would be to always save an FID and an ID columns, as I did in country_ids.tif
        # Additionally, this could be challenging because you can't, as below, use the columns[0] as the index on the assumption that FID would still be there in the columns.
        gdf = gpd.read_file(zones_vector_path)
        if id_column_label is None:
            id_column_label = gdf.columns[0]

        unique_zone_ids_pre = np.unique(gdf[id_column_label][gdf[id_column_label].notnull()]).astype(np.int64)

        to_append = []
        if 0 not in unique_zone_ids_pre:
            to_append.append(0)
        # if zones_ndv not in unique_zone_ids_pre:
        #     to_append.append(zones_ndv)
        unique_zone_ids = np.asarray(to_append + list(unique_zone_ids_pre))
        # unique_zone_ids = np.asarray(to_append + list(unique_zone_ids_pre) + [max(unique_zone_ids_pre) + 1])

    if verbose:
        L.info('Starting zonal_statistics_rasterized using zone_ids_raster_path at ' + str(zone_ids_raster_path))

    # Call zonal_statistics_rasterized to parse vars into cython-format and go from there.


    if stats_to_retrieve == 'sums':
        L.debug('Exporting sums.')
        L.debug('unique_zone_ids', unique_zone_ids)
        unique_ids, sums = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)


        df = pd.DataFrame(index=unique_ids, data={'sums': sums})
        df[df == 0] = np.nan
        df.dropna(inplace=True)

        if vector_columns_to_include_in_output is not None:
            gdf = gpd.read_file(zones_vector_path)
            df = df.merge(gdf[[vector_index_column] + vector_columns_to_include_in_output], how='outer', left_index=True, right_on=vector_index_column)
            df = df[[vector_index_column] + vector_columns_to_include_in_output + ['sums']]
            df = df.sort_values(by=[vector_index_column])
            if output_column_prefix is not None:
                rename_dict = {'sums': output_column_prefix + '_sums'}
                df = df.rename(columns=rename_dict)

        if csv_output_path is not None:
            df.to_csv(csv_output_path, index=None)

        if vector_output_path is not None:
            gdf = gpd.read_file(zones_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'sums_counts':
        L.debug('Exporting sums_counts.')
        unique_ids, sums, counts = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)

        df = pd.DataFrame(index=unique_ids, data={'sums': sums, 'counts': counts})
        df[df == 0] = np.nan
        df.dropna(inplace=True)

        if vector_columns_to_include_in_output is not None:
            gdf = gpd.read_file(zones_vector_path)
            df = df.merge(gdf[[vector_index_column] + vector_columns_to_include_in_output], how='outer', left_index=True, right_on=vector_index_column)
            df = df[[vector_index_column] + vector_columns_to_include_in_output + ['sums', 'counts']]
            df = df.sort_values(by=[vector_index_column])
            if output_column_prefix is not None:
                rename_dict = {'sums': output_column_prefix + '_sums', 'counts': output_column_prefix + '_counts'}
                df = df.rename(columns=rename_dict)

        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zones_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'enumeration':

        L.debug('Exporting enumeration.')

        if enumeration_classes is None:
            enumeration_classes = hb.unique_raster_values_path(input_raster)
            enumeration_classes = [int(i) for i in enumeration_classes]
            if len(enumeration_classes) > 30:
                L.warning('You are attempting to enumerate a map with more than 30 unique values. Are you sure about this? Sure as heck doesnt look like categorized data to me...')

        unique_ids, enumeration = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve,
                                                                 enumeration_classes=enumeration_classes, multiply_raster_path=multiply_raster_path,
                                                                 verbose=verbose, )
        enumeration = np.asarray(enumeration)
        df = pd.DataFrame(index=unique_ids, columns=[str(i) for i in enumeration_classes], data=enumeration)

        if vector_columns_to_include_in_output is not None:
            gdf = gpd.read_file(zones_vector_path)
            df = df.merge(gdf[[vector_index_column] + vector_columns_to_include_in_output], how='outer', left_index=True, right_on=vector_index_column)

            df = df[[vector_index_column] + vector_columns_to_include_in_output + [str(i) for i in enumeration_classes]]

            if output_column_prefix is not None:
                if enumeration_labels is not None:
                    rename_dict = {str(i): output_column_prefix + '_' + enumeration_labels[c] for c, i in enumerate(enumeration_classes)}
                else:
                    rename_dict = {str(i): output_column_prefix + '_class_' + str(i) for i in enumeration_classes}
                # df = df[[vector_index_column] + vector_columns_to_include_in_output + [output_column_prefix + '_class_' + str(i) for i in enumeration_classes]]
            else:
                if enumeration_labels is not None:
                    rename_dict = {str(i): enumeration_labels[c] for c, i in enumerate(enumeration_classes)}
                else:
                    rename_dict = {str(i): 'class_' + str(i) for i in enumeration_classes}
            df = df.rename(columns=rename_dict)

            df = df.sort_values(by=[vector_index_column])


        if csv_output_path is not None:
            df.to_csv(csv_output_path, index=False)

        if vector_output_path is not None:
            gdf = gpd.read_file(zones_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')
            gdf_no_geom = gdf.drop(columns='geometry')




        return df


def zonal_statistics_rasterized(zone_ids_raster_path, values_raster_path, zones_ndv=None, values_ndv=None, zone_ids_data_type=None,
                                values_data_type=None, unique_zone_ids=None, stats_to_retrieve='sums', enumeration_classes=None,
                                multiply_raster_path=None, verbose=True, max_enumerate_value=1000):
    """
    Calculate zonal statistics using a pre-generated raster ID array.

    NOTE that by construction, this type of zonal statistics cannot handle overlapping polygons (each polygon is just represented by its id int value in the raster).
    """

    if verbose:
        L.info('Starting to run zonal_statistics_rasterized using iterblocks.')

    if unique_zone_ids is None:
        if verbose:
            L.info('Load zone_ids_raster and compute unique values in it. Could be slow (and could be pregenerated for speed if desired).')

        zone_ids = hb.as_array(zone_ids_raster_path)
        unique_zone_ids = np.unique(zone_ids).astype(np.int64)
        L.warning('Generated unique_zone_ids via brute force. This could be optimized.', str(unique_zone_ids))
        zone_ids = None
    else:
        unique_zone_ids = unique_zone_ids.astype(np.int64)

    # Get dimensions of rasters for callback reporting'
    zone_ds = gdal.OpenEx(zone_ids_raster_path)
    n_cols = zone_ds.RasterYSize
    n_rows = zone_ds.RasterXSize
    n_pixels = n_cols * n_rows

    # Create new arrays to hold results.
    # NOTE THAT this creates an array as long as the MAX VALUE in unique_zone_ids, which means there could be many zero values. This
    # is intended as it increases computation speed to not have to do an additional lookup.
    aggregated_sums = np.zeros(len(unique_zone_ids), dtype=np.float64)
    aggregated_counts = np.zeros(len(unique_zone_ids), dtype=np.int64)

    last_time = time.time()
    pixels_processed = 0

    # Iterate through block_offsets
    zone_ids_raster_path_band = (zone_ids_raster_path, 1)
    aggregated_enumeration = None
    for c, block_offset in enumerate(list(hb.iterblocks(zone_ids_raster_path_band, offset_only=True))):
        sample_fraction = None # TODOO add this in to function call.
        # sample_fraction = .05
        if sample_fraction is not None:
            if random.random() < sample_fraction:
                select_block = True
            else:
                select_block = False
        else:
            select_block = True

        if select_block:
            block_offset_new_gdal_api = {
                'xoff': block_offset['xoff'],
                'yoff': block_offset['yoff'],
                'buf_ysize': block_offset['win_ysize'],
                'buf_xsize': block_offset['win_xsize'],
            }

            zones_ds = gdal.OpenEx(zone_ids_raster_path)
            values_ds = gdal.OpenEx(values_raster_path)
            # No idea why, but using **block_offset_new_gdal_api failed, so I unpack it manually here.
            try:
                zones_array = zones_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.int64)
                values_array = values_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.float64)

            except:
                L.critical('unable to load' + zone_ids_raster_path + ' ' + values_raster_path)
                pass
                # zones_array = zones_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff']).astype(np.int64)
                # values_array = values_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff']).astype(np.float64)

            if zones_array.shape != values_array.shape:
                L.critical('zones_array.shape != values_array.shape', zones_array.shape, values_array.shape)

            unique_zone_ids_np = np.asarray(unique_zone_ids, dtype=np.int64)

            if len(unique_zone_ids_np) > 1000:
                L.critical('Running zonal_statistics_flex with many unique_zone_ids: ' + str(unique_zone_ids_np))

            if stats_to_retrieve=='sums':
                sums = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv, stats_to_retrieve=stats_to_retrieve)
                aggregated_sums += sums
            elif stats_to_retrieve == 'sums_counts':
                sums, counts = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv, stats_to_retrieve=stats_to_retrieve)
                aggregated_sums += sums
                aggregated_counts += counts
            elif stats_to_retrieve == 'enumeration':
                if multiply_raster_path is not None:
                    multiply_ds = gdal.OpenEx(multiply_raster_path)
                    shape = hb.get_shape_from_dataset_path(multiply_raster_path)
                    if shape[1] == 1: # FEATURE NOTE: if you give a 1 dim array, it will be multiplied repeatedly over the vertical cols of the input_array. This is useful for when you want to multiple just the hectarage by latitude vertical strip array.

                        # If is vertical stripe, just read based on y buffer.
                        multiply_raster = multiply_ds.ReadAsArray(0, block_offset_new_gdal_api['yoff'], 1, block_offset_new_gdal_api['buf_ysize']).astype(np.float64)
                    else:
                        multiply_raster = multiply_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.float64)
                else:
                    multiply_raster = np.asarray([[1]], dtype=np.float64)
                enumeration = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                        stats_to_retrieve=stats_to_retrieve, enumeration_classes=np.asarray(enumeration_classes, dtype=np.int64), multiply_raster=np.asarray(multiply_raster, dtype=np.float64))

                if aggregated_enumeration is None:
                    aggregated_enumeration = np.copy(enumeration)
                else:
                    aggregated_enumeration += enumeration
            pixels_processed += block_offset_new_gdal_api['buf_xsize'] * block_offset_new_gdal_api['buf_ysize']

            last_time = hb.invoke_timed_callback(
                last_time, lambda: L.info('Zonal statistics rasterized on ' + str(values_raster_path) + ':', float(pixels_processed) / n_pixels * 100.0), 3)
    if stats_to_retrieve == 'sums':
        return unique_zone_ids, aggregated_sums
    elif stats_to_retrieve == 'sums_counts':
        return unique_zone_ids, aggregated_sums, aggregated_counts
    elif stats_to_retrieve == 'enumeration':

        return unique_zone_ids, aggregated_enumeration

def zonal_statistics_rasterized_dask(zone_ids_raster_path, values_raster_path, zones_ndv=None, values_ndv=None, zone_ids_data_type=None,
                                values_data_type=None, unique_zone_ids=None, stats_to_retrieve='sums', enumeration_classes=None,
                                multiply_raster_path=None, verbose=True, max_enumerate_value=1000):
    """
This turned out to be extrordinarily hard becasue of the implied dimensionality reduction. Gonna need to rethink it.


    """
    if verbose:
        L.info('Starting to run zonal_statistics_rasterized_dask.')

    if unique_zone_ids is None:
        if verbose:
            L.info('Load zone_ids_raster and compute unique values in it. Could be slow (and could be pregenerated for speed if desired).')

        zone_ids = hb.as_array(zone_ids_raster_path)
        unique_zone_ids = np.unique(zone_ids).astype(np.int64)
        L.warning('Generated unique_zone_ids via brute force. This could be optimized.', str(unique_zone_ids))
        zone_ids = None
    else:
        unique_zone_ids = unique_zone_ids.astype(np.int64)



    import dask
    from dask import array
    from dask.array import from_array
    from dask.distributed import Client, LocalCluster, Lock
    import rioxarray

    input_paths = [zone_ids_raster_path, values_raster_path]

    block_sizes = []
    for path in input_paths:
        if not hb.path_exists(path):
            raise NameError('dask_compute unable to find path: ' + str(path))
        block_sizes.append(hb.get_blocksize_from_path(path))

    t_b = tuple([tuple(i) for i in block_sizes])

    if len(set(t_b)) > 1:
        critical_string = 'Paths given to dask_computer were not all saved in the same blocksize. This will have dramatic performance implications.'
        critical_string += '\n' + str(input_paths)
        critical_string += '\n' + str(block_sizes)
        L.critical(critical_string)

    from dask.diagnostics import ProgressBar
    import threading

    # Use reioxarray to read with specified chunksize.
    zone_ids_da = rioxarray.open_rasterio(zone_ids_raster_path, chunks={'band': 1, 'x': 1024, 'y': 1024})
    values_da = rioxarray.open_rasterio(values_raster_path, chunks={'band': 1, 'x': 1024, 'y': 1024})
    return_da = dask.array.from_array(unique_zone_ids)



    # define the operation, which hasn't run yet.
    # subtraction = ds_scenario - ds_baseline
    def op(zone_ids_da, values_da, return_da, zones_ndv, values_ndv):
        return_list = []

        return_da = zone_ids_da - values_da
        return return_da

    # Now it actually runs.
    hb.timer('start')
    r = op(zone_ids_da, values_da, return_da, zones_ndv, values_ndv)
    r.compute()
    hb.timer('Small')
    #
    # with LocalCluster() as cluster, Client(cluster) as client:
    # # with LocalCluster() as cluster, Client(cluster) as client:
    # # with LocalCluster(n_workers=math.floor(multiprocessing.cpu_count() / 2), threads_per_worker=2, memory_limit=str(math.floor(64 / (multiprocessing.cpu_count() + 1))) + 'GB') as cluster, Client(cluster) as client:
    #
    #     L.info('Starting Local Cluster at http://localhost:8787/status')
    #
    #     xds_list = []
    #     for input_path in input_paths:
    #         # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
    #         # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
    #         xds = rioxarray.open_rasterio(input_path, chunks='auto', lock=False)
    #         xds_list.append(xds)
    #
    #     delayed_computation = op(*xds_list)
    #     delayed_computation.rio.to_raster(output_path, tiled=True, compress='DEFLATE', lock=Lock("rio", client=client))  # NOTE!!! MUCH FASTER WITH THIS. I think it's because it coordinates with the read to start the next thing asap.
    #
    # # delayed_computation.compute()
        # delayed_computation.rio.to_raster(output_path, tiled=True, compress='DEFLATE', lock=Lock("rio", client=client))  # NOTE!!! MUCH FASTER WITH THIS. I think it's because it coordinates with the read to start the next thing asap.
    #
    #
    #
    #
    #
    # # Get dimensions of rasters for callback reporting'
    # zone_ds = gdal.OpenEx(zone_ids_raster_path)
    # n_cols = zone_ds.RasterYSize
    # n_rows = zone_ds.RasterXSize
    # n_pixels = n_cols * n_rows
    #
    # # Create new arrays to hold results.
    # # NOTE THAT this creates an array as long as the MAX VALUE in unique_zone_ids, which means there could be many zero values. This
    # # is intended as it increases computation speed to not have to do an additional lookup.
    # aggregated_sums = np.zeros(len(unique_zone_ids), dtype=np.float64)
    # aggregated_counts = np.zeros(len(unique_zone_ids), dtype=np.int64)
    #
    # last_time = time.time()
    # pixels_processed = 0
    #
    # # Iterate through block_offsets
    # zone_ids_raster_path_band = (zone_ids_raster_path, 1)
    # aggregated_enumeration = None
    # for c, block_offset in enumerate(list(hb.iterblocks(zone_ids_raster_path_band, offset_only=True))):
    #     sample_fraction = None # TODOO add this in to function call.
    #     # sample_fraction = .05
    #     if sample_fraction is not None:
    #         if random.random() < sample_fraction:
    #             select_block = True
    #         else:
    #             select_block = False
    #     else:
    #         select_block = True
    #
    #     if select_block:
    #         block_offset_new_gdal_api = {
    #             'xoff': block_offset['xoff'],
    #             'yoff': block_offset['yoff'],
    #             'buf_ysize': block_offset['win_ysize'],
    #             'buf_xsize': block_offset['win_xsize'],
    #         }
    #
    #         zones_ds = gdal.OpenEx(zone_ids_raster_path)
    #         values_ds = gdal.OpenEx(values_raster_path)
    #         # No idea why, but using **block_offset_new_gdal_api failed, so I unpack it manually here.
    #         try:
    #             zones_array = zones_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.int64)
    #             values_array = values_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.float64)
    #
    #         except:
    #             L.critical('unable to load' + zone_ids_raster_path + ' ' + values_raster_path)
    #             pass
    #             # zones_array = zones_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff']).astype(np.int64)
    #             # values_array = values_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff']).astype(np.float64)
    #
    #         if zones_array.shape != values_array.shape:
    #             L.critical('zones_array.shape != values_array.shape', zones_array.shape, values_array.shape)
    #
    #         unique_zone_ids_np = np.asarray(unique_zone_ids, dtype=np.int64)
    #
    #         if len(unique_zone_ids_np) > 1000:
    #             L.critical('Running zonal_statistics_flex with many unique_zone_ids: ' + str(unique_zone_ids_np))
    #
    #         if stats_to_retrieve=='sums':
    #             sums = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv, stats_to_retrieve=stats_to_retrieve)
    #             aggregated_sums += sums
    #         elif stats_to_retrieve == 'sums_counts':
    #             sums, counts = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv, stats_to_retrieve=stats_to_retrieve)
    #             aggregated_sums += sums
    #             aggregated_counts += counts
    #         elif stats_to_retrieve == 'enumeration':
    #             if multiply_raster_path is not None:
    #                 multiply_ds = gdal.OpenEx(multiply_raster_path)
    #                 shape = hb.get_shape_from_dataset_path(multiply_raster_path)
    #                 if shape[1] == 1: # FEATURE NOTE: if you give a 1 dim array, it will be multiplied repeatedly over the vertical cols of the input_array. This is useful for when you want to multiple just the hectarage by latitude vertical strip array.
    #
    #                     # If is vertical stripe, just read based on y buffer.
    #                     multiply_raster = multiply_ds.ReadAsArray(0, block_offset_new_gdal_api['yoff'], 1, block_offset_new_gdal_api['buf_ysize']).astype(np.float64)
    #                 else:
    #                     multiply_raster = multiply_ds.ReadAsArray(block_offset_new_gdal_api['xoff'], block_offset_new_gdal_api['yoff'], block_offset_new_gdal_api['buf_xsize'], block_offset_new_gdal_api['buf_ysize']).astype(np.float64)
    #             else:
    #                 multiply_raster = np.asarray([[1]], dtype=np.float64)
    #             enumeration = hb.zonal_stats_cythonized(zones_array, values_array, unique_zone_ids_np, zones_ndv=zones_ndv, values_ndv=values_ndv,
    #                                                     stats_to_retrieve=stats_to_retrieve, enumeration_classes=np.asarray(enumeration_classes, dtype=np.int64), multiply_raster=np.asarray(multiply_raster, dtype=np.float64))
    #
    #             if aggregated_enumeration is None:
    #                 aggregated_enumeration = np.copy(enumeration)
    #             else:
    #                 aggregated_enumeration += enumeration
    #         pixels_processed += block_offset_new_gdal_api['buf_xsize'] * block_offset_new_gdal_api['buf_ysize']
    #
    #         last_time = hb.invoke_timed_callback(
    #             last_time, lambda: L.info('Zonal statistics rasterized percent complete:', float(pixels_processed) / n_pixels * 100.0), 3)
    # if stats_to_retrieve == 'sums':
    #     return unique_zone_ids, aggregated_sums
    # elif stats_to_retrieve == 'sums_counts':
    #     return unique_zone_ids, aggregated_sums, aggregated_counts
    # elif stats_to_retrieve == 'enumeration':
    #
    #     return unique_zone_ids, aggregated_enumeration

def zonal_statistics(
        input_raster_path,
        zones_vector_path,
        id_column_label=None,
        zone_ids_raster_path=None,
        stats_to_retrieve='sums',
        enumeration_classes=None,
        enumeration_labels=None,
        multiply_raster_path=None,
        output_column_prefix=None,
        csv_output_path=None,
        vector_output_path=None,
        zones_ndv = None,
        zones_raster_data_type=None,
        unique_zone_ids=None, # CAUTION on changing this one. Cython code is optimized by assuming a continuous set of integers of the right bit size that covers all value possibilities and zero and the NDV.
        assert_projections_same=False,
        values_ndv=-9999,
        max_enumerate_value=20000,
        use_pygeoprocessing_version=False,
        verbose=False,
):
    # TODOO Need to consider the case to raise an exception when someone provides a pre-generated zone_ids that doesn't cover all in zones_vector_path.

    # First just test that all files are present
    hb.path_exists(input_raster_path, verbose=verbose)
    hb.path_exists(zones_vector_path, verbose=verbose)

    # Read the vector path
    gdf = gpd.read_file(zones_vector_path)

    # If no id_column_label is given, check the GDF for unique ints and choose first
    if id_column_label is None:
        possible_ids = []
        for column_label in gdf.columns:
            dtype = gdf[column_label].dtype
            if 'int' in str(dtype):
                if len(gdf[column_label].unique()) == gdf.shape[0]:
                    possible_ids.append(column_label)
        id_column_label = possible_ids[0]

    # If the id_column is not an int, check to see if its at least unique, then generate that.
    if not 'int' in str(gdf[id_column_label].dtype):
        if len(gdf[id_column_label].unique()) == gdf.shape[0]:
            print('like this')
        raise NameError('NYI but could generate a unique ids from a unique non int.')

    # Determine if we can get away with 8bit data.

    id_min = gdf[id_column_label].min()
    id_max = gdf[id_column_label].max()

    if not zones_raster_data_type:
        if not zones_ndv:
            if id_min > 0 and id_max < 255: # notice that i'm reserving 0 and 255 for values and NDV.
                zones_ndv = 255
                zones_raster_data_type = 1
                numpy_dtype = np.uint8
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(0, 256, dtype=numpy_dtype)
            else:
                zones_ndv = -9999
                zones_raster_data_type = 5
                numpy_dtype = np.int64
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(-9999, 9999 + 1, dtype=numpy_dtype)
        else:
            if zones_ndv == 255:
                zones_raster_data_type = 1
                numpy_dtype = np.uint8
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(-9999, 9999 + 1, dtype=numpy_dtype)
            else:
                zones_raster_data_type = 5
                numpy_dtype = np.int64
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(0, 256, dtype=numpy_dtype)
    else:

        if not zones_ndv:
            if zones_raster_data_type >= 5:
                zones_ndv = -9999
                numpy_dtype = np.int64
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(0, 256, dtype=numpy_dtype)
            else:
                zones_ndv = 255
                numpy_dtype = np.uint8
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(-9999, 9999 + 1, dtype=numpy_dtype)
        else:
            if zones_raster_data_type >= 5:
                numpy_dtype = np.int64
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(0, 256, dtype=numpy_dtype)
            else:
                numpy_dtype = np.uint8
                if unique_zone_ids is None:
                    unique_zone_ids = np.arange(-9999, 9999 + 1, dtype=numpy_dtype)

    if id_max - id_min < max_enumerate_value:
        create_unique_ids_array = True
    else:
        create_unique_ids_array = False

    # Test that input_raster and shapefile are in the same projection. Sillyness results if not.
    if assert_projections_same:
        hb.assert_gdal_paths_in_same_projection([zones_vector_path, zones_vector_path])
    else:
        if verbose:
            a = hb.assert_gdal_paths_in_same_projection([input_raster_path, zones_vector_path], return_result=True)
            if not a:
                L.critical('Ran zonal_statistics_flex but the inputs werent in identical projections.')
        else:
            pass

    # if zone_ids_raster_path is not set, make it a temporary file
    if zone_ids_raster_path is None:
        zone_ids_raster_path = 'zone_ids_' + hb.random_string() + '.tif'

    # if zone_ids_raster_path is given, use it to speed up processing (creating it first if it doesnt exist)
    if not hb.path_exists(zone_ids_raster_path):
        # Calculate the id raster and save it
        if verbose:
            L.info('Creating id_raster with convert_polygons_to_id_raster')
        hb.convert_polygons_to_id_raster(zones_vector_path, zone_ids_raster_path, input_raster_path, id_column_label=id_column_label, data_type=zones_raster_data_type,
                                         ndv=zones_ndv, all_touched=True)
    else:
        if verbose:
            L.info('Zone_ids_raster_path existed, so not creating it.')

    # Append all stat output columns with this output_column_prefix so that when things are merged later on its not confusing
    if output_column_prefix is None:
        output_column_prefix = hb.file_root(input_raster_path)

    if use_pygeoprocessing_version:
        # This version is much slower so it is not advised nless you need the greater flexibility of allowing polygons to overlap.
        base_raster_path_band = (input_raster_path, 1)
        to_return = pgp.zonal_statistics(
            base_raster_path_band, zones_vector_path,
            aggregate_layer_name=id_column_label, ignore_nodata=True,
            polygons_might_overlap=True, working_dir=None)
        if csv_output_path is not None:
            hb.python_object_to_csv(to_return, csv_output_path)
        return to_return

    if verbose:
        L.info('Starting zonal_statistics_rasterized using zone_ids_raster_path at ' + str(zone_ids_raster_path))

    if stats_to_retrieve == 'sums':
        L.debug('Exporting sums.')
        L.debug('unique_zone_ids', unique_zone_ids)
        _, sums = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster_path, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)

        # Create a DF of the exhaustive, continuous ints in unique_zone_ids, which may have lots of zeros.
        df = pd.DataFrame(index=unique_zone_ids, data={output_column_prefix + '_sums': sums})

    elif stats_to_retrieve == 'sums_counts':
        L.debug('Exporting sums_counts.')
        _, sums, counts = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster_path, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)

        df = pd.DataFrame(index=unique_zone_ids, data={output_column_prefix + '_sums': sums, output_column_prefix + '_counts': counts})


    elif stats_to_retrieve == 'enumeration':

        L.debug('Exporting enumeration.')

        if enumeration_classes is None:
            enumeration_classes = hb.unique_raster_values_path(input_raster_path)
            enumeration_classes = [int(i) for i in enumeration_classes]
            if len(enumeration_classes) > 90:
                L.warning('You are attempting to enumerate a map with more than 90 unique values. Are you sure about this? Sure as heck doesnt look like categorized data to me...')

        _, enumeration = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster_path, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve,
                                                                 enumeration_classes=enumeration_classes, multiply_raster_path=multiply_raster_path,
                                                                 verbose=verbose, )
        enumeration = np.asarray(enumeration)
        if enumeration_labels is not None:
            df = pd.DataFrame(index=unique_zone_ids, columns=[output_column_prefix + '_' + enumeration_labels[c]  + '_' + str(i) for c, i in enemerate(enumeration_classes)], data=enumeration)
        else:
            df = pd.DataFrame(index=unique_zone_ids, columns=[output_column_prefix + '_class_' + str(i) for c, i in enemerate(enumeration_classes)], data=enumeration)

    # Select out just the index values that are in the gdf
    df[id_column_label] = df.index
    dfs = df.loc[gdf[id_column_label]]

    gdfo = hb.df_merge(gdf, dfs, how='outer', left_on=id_column_label, right_on=id_column_label)

    if csv_output_path is not None:
        df = gdfo[[i for i in gdfo.columns if i != 'geometry']]
        df.to_csv(csv_output_path, index=None)

    if vector_output_path is not None:
        gdfo.to_file(vector_output_path, driver='GPKG')

    return gdfo


def zonal_statistics_merge(
        input_raster_paths,
        zones_vector_path,
        id_column_label=None,
        zone_ids_raster_path=None,
        stats_to_retrieve='sums',
        enumeration_classes=None,
        enumeration_labels=None,
        multiply_raster_path=None,
        output_column_prefix=None,
        csv_output_path=None,
        vector_output_path=None,
        zones_ndv=None,
        zones_raster_data_type=None,
        unique_zone_ids=None,  # CAUTION on changing this one. Cython code is optimized by assuming a continuous set of integers of the right bit size that covers all value possibilities and zero and the NDV.
        assert_projections_same=False,
        values_ndv=-9999,
        max_enumerate_value=20000,
        use_pygeoprocessing_version=False,
        verbose=False,
):

    # Only generate zone_ids_raster_path once then reuse.
    if zone_ids_raster_path is None:
        zone_ids_raster_path = hb.ruri(os.path.join(os.path.split(zones_vector_path)[0], 'zone_ids.tif'))

    df = None
    for input_raster_path in input_raster_paths:
        if verbose:
            L.info('Running zonal statistics on ' + str(input_raster_path) + ' (called from zonal_statistics_merge)')
        current_df = hb.zonal_statistics(
            input_raster_path,
            zones_vector_path,
            id_column_label=id_column_label,
            zone_ids_raster_path=zone_ids_raster_path,
            zones_ndv=zones_ndv,
            assert_projections_same=assert_projections_same,
            verbose=verbose,
        )

        if df is None:
            df = current_df
        else:
            df = hb.df_merge(df, current_df)
    return df

def extract_correspondence_and_categories_dicts_from_df_cols(input_df, broad_col, narrow_col):
    set_differences = hb.compare_sets(input_df[broad_col], input_df[narrow_col], return_amount='all')

    correspondence = {}
    categories = {}
    for i in set_differences['right_set']:
        categories[i] = []
    for i in set_differences['left_set']:
        correspondence[i] = input_df[input_df[broad_col] == i][narrow_col].values[0]
        categories[input_df[input_df[broad_col] == i][narrow_col].values[0]].append(i)
    return correspondence, categories



def get_vector_info_PGP_REFERENCE(vector_path, layer_index=0):
    """Get information about an OGR vector (datasource).

    Parameters:
        vector_path (str): a path to a OGR vector.
        layer_index (int): index of underlying layer to analyze.  Defaults to
            0.

    Raises:
        ValueError if `vector_path` does not exist on disk or cannot be opened
        as a gdal.OF_VECTOR.

    Returns:
        raster_properties (dictionary): a dictionary with the following
            properties stored under relevant keys.

            'projection' (string): projection of the vector in Well Known
                Text.
            'bounding_box' (list): list of floats representing the bounding
                box in projected coordinates as [minx, miny, maxx, maxy].

    """
    vector = gdal.OpenEx(vector_path, gdal.OF_VECTOR)
    if not vector:
        raise ValueError(
            "Could not open %s as a gdal.OF_VECTOR" % vector_path)
    vector_properties = {}
    layer = vector.GetLayer(iLayer=layer_index)
    # projection is same for all layers, so just use the first one
    spatial_ref = layer.GetSpatialRef()
    if spatial_ref:
        vector_sr_wkt = spatial_ref.ExportToWkt()
    else:
        vector_sr_wkt = None
    vector_properties['projection'] = vector_sr_wkt
    layer_bb = layer.GetExtent()
    layer = None
    vector = None
    # convert form [minx,maxx,miny,maxy] to [minx,miny,maxx,maxy]
    vector_properties['bounding_box'] = [layer_bb[i] for i in [0, 2, 1, 3]]
    return vector_properties


def get_raster_info_PGP_REFERENCE(raster_path):
    """Get information about a GDAL raster (dataset).

    Parameters:
       raster_path (String): a path to a GDAL raster.

    Raises:
        ValueError if `raster_path` is not a file or cannot be opened as a
        gdal.OF_RASTER.

    Returns:
        raster_properties (dictionary): a dictionary with the properties
            stored under relevant keys.

            'pixel_size' (tuple): (pixel x-size, pixel y-size) from
                geotransform.
            'mean_pixel_size' (float): the average size of the absolute value
                of each pixel size element.
            'raster_size' (tuple):  number of raster pixels in (x, y)
                direction.
            'nodata' (list): a list of the nodata values in the bands of the
                raster in the same order as increasing band index.
            'n_bands' (int): number of bands in the raster.
            'geotransform' (tuple): a 6-tuple representing the geotransform of
                (x orign, x-increase, xy-increase,
                 y origin, yx-increase, y-increase).
            'datatype' (int): An instance of an enumerated gdal.GDT_* int
                that represents the datatype of the raster.
            'projection' (string): projection of the raster in Well Known
                Text.
            'bounding_box' (list): list of floats representing the bounding
                box in projected coordinates as [minx, miny, maxx, maxy]
            'block_size' (tuple): underlying x/y raster block size for
                efficient reading.

    """
    raster = gdal.OpenEx(raster_path, gdal.OF_RASTER)
    if not raster:
        raise ValueError(
            "Could not open %s as a gdal.OF_RASTER" % raster_path)
    raster_properties = {}
    projection_wkt = raster.GetProjection()
    if not projection_wkt:
        projection_wkt = None
    raster_properties['projection'] = projection_wkt
    geo_transform = raster.GetGeoTransform()
    raster_properties['geotransform'] = geo_transform
    raster_properties['pixel_size'] = (geo_transform[1], geo_transform[5])
    raster_properties['mean_pixel_size'] = (
            (abs(geo_transform[1]) + abs(geo_transform[5])) / 2.0)
    raster_properties['raster_size'] = (
        raster.GetRasterBand(1).XSize,
        raster.GetRasterBand(1).YSize)
    raster_properties['n_bands'] = raster.RasterCount
    raster_properties['nodata'] = [
        raster.GetRasterBand(index).GetNoDataValue() for index in range(
            1, raster_properties['n_bands'] + 1)]
    # blocksize is the same for all bands, so we can just get the first
    raster_properties['block_size'] = raster.GetRasterBand(1).GetBlockSize()

    # we dont' really know how the geotransform is laid out, all we can do is
    # calculate the x and y bounds, then take the appropriate min/max
    x_bounds = [
        geo_transform[0], geo_transform[0] +
                          raster_properties['raster_size'][0] * geo_transform[1] +
                          raster_properties['raster_size'][1] * geo_transform[2]]
    y_bounds = [
        geo_transform[3], geo_transform[3] +
                          raster_properties['raster_size'][0] * geo_transform[4] +
                          raster_properties['raster_size'][1] * geo_transform[5]]

    raster_properties['bounding_box'] = [
        numpy.min(x_bounds), numpy.min(y_bounds),
        numpy.max(x_bounds), numpy.max(y_bounds)]

    # datatype is the same for the whole raster, but is associated with band
    raster_properties['datatype'] = raster.GetRasterBand(1).DataType
    raster = None
    return raster_properties
























