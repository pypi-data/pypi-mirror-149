import os, sys, warnings, logging, inspect, math, time

from osgeo import gdal, osr, ogr
import netCDF4
import netCDF4 as nc
import numpy as np
import hazelbean as hb
import time
from collections import OrderedDict
from decimal import Decimal
import multiprocessing
import geopandas as gpd
import pandas as pd
import difflib
import rioxarray

L = hb.get_logger('pyramids', logging_level='info')

mollweide_compatible_resolutions = OrderedDict()
mollweide_compatible_resolutions[10.0] = 309.2208077590933 # calculated via hb.size_of_one_arcdegree_at_equator_in_meters / (60 * 6)
mollweide_compatible_resolutions[30.0] = 309.2208077590933 * (30.0 / 10.0)
mollweide_compatible_resolutions[300.0] = 309.2208077590933 * (300.0 / 10.0)
mollweide_compatible_resolutions[900.0] = 309.2208077590933 * (900.0 / 10.0)
mollweide_compatible_resolutions[1800.0] = 309.2208077590933 * (1800.0 / 10.0)
mollweide_compatible_resolutions[3600.0] = 309.2208077590933 * (3600.0 / 10.0)
mollweide_compatible_resolutions[7200.0] = 309.2208077590933 * (7200.0 / 10.0)
mollweide_compatible_resolutions[14400.0] = 309.2208077590933 * (14400.0 / 10.0)

# Define the resolutions compatible with pyramid calculation as key = arcseconds, value = resolution in 64 bit notation, precisely defined with the right amount of significant digits.
pyramid_compatible_arcseconds = [10.0,
                                                     30.0,
                                                     300.0,
                                                     900.0,
                                                     1800.0,
                                                     3600.0,
                                                     7200.0,
                                                     14400.0,]

pyramid_compatible_resolution_to_arcseconds = OrderedDict()
pyramid_compatible_resolution_to_arcseconds[0.002777777777777778] =    10.0
pyramid_compatible_resolution_to_arcseconds[0.008333333333333333] =    30.0
pyramid_compatible_resolution_to_arcseconds[0.08333333333333333] =   300.0
pyramid_compatible_resolution_to_arcseconds[0.25] =   900.0
pyramid_compatible_resolution_to_arcseconds[0.5] =  1800.0
pyramid_compatible_resolution_to_arcseconds[1.0] =  3600.0
pyramid_compatible_resolution_to_arcseconds[2.0] =  7200.0
pyramid_compatible_resolution_to_arcseconds[4.0] = 14400.0

pyramid_compatible_resolutions = OrderedDict()
pyramid_compatible_resolutions[10.0] =    0.002777777777777778
pyramid_compatible_resolutions[30.0] =    0.008333333333333333
pyramid_compatible_resolutions[300.0] =   0.08333333333333333
pyramid_compatible_resolutions[900.0] =   0.25
pyramid_compatible_resolutions[1800.0] =  0.5
pyramid_compatible_resolutions[3600.0] =  1.0
pyramid_compatible_resolutions[7200.0] =  2.0
pyramid_compatible_resolutions[14400.0] = 4.0

# Define the bounds of what should raise an assertion that the file is close but not exactly matching one of the supported resolutions.
pyramid_compatible_resolution_bounds = OrderedDict()
pyramid_compatible_resolution_bounds[10.0] =    (0.0027777, 0.00277778)
pyramid_compatible_resolution_bounds[30.0] =    (0.0083333, 0.00833334)
pyramid_compatible_resolution_bounds[300.0] =   (0.08333, 0.08334)
pyramid_compatible_resolution_bounds[900.0] =   (0.24999, 0.25001)
pyramid_compatible_resolution_bounds[1800.0] =  (0.4999, 0.5001)
pyramid_compatible_resolution_bounds[3600.0] =  (0.999, 1.001)
pyramid_compatible_resolution_bounds[7200.0] =  (1.999, 2.001)
pyramid_compatible_resolution_bounds[14400.0] = (3.999, 4.001)

pyramid_compatable_shapes = {}
pyramid_compatable_shapes[10.0] = [129600, 64800]
pyramid_compatable_shapes[20.0] = [64800, 32400]
pyramid_compatable_shapes[30.0] = [43200, 21600]
pyramid_compatable_shapes[60.0] = [21600, 10800]
pyramid_compatable_shapes[120.0] = [10800, 5400]
pyramid_compatable_shapes[240.0] = [5400, 2700]
pyramid_compatable_shapes[300.0] = [4320, 2160]
pyramid_compatable_shapes[600.0] = [2160, 1080]
pyramid_compatable_shapes[900.0] = [1440, 720]
pyramid_compatable_shapes[1800.0] = [720, 360]
pyramid_compatable_shapes[3600.0] = [360, 180]
pyramid_compatable_shapes[7200.0] = [180, 90]
pyramid_compatable_shapes[14400.0] = [90, 45]

pyramid_compatable_shapes_to_arcseconds = {}
pyramid_compatable_shapes_to_arcseconds[(129600, 64800)] = 10.0
pyramid_compatable_shapes_to_arcseconds[(64800, 32400)] = 20.0
pyramid_compatable_shapes_to_arcseconds[(43200, 21600)] = 30.0
pyramid_compatable_shapes_to_arcseconds[(21600, 10800)] = 60.0
pyramid_compatable_shapes_to_arcseconds[(10800, 5400)] = 120.0
pyramid_compatable_shapes_to_arcseconds[(5400, 2700)] = 240.0
pyramid_compatable_shapes_to_arcseconds[(4320, 2160)] = 300.0
pyramid_compatable_shapes_to_arcseconds[(2160, 1080)] = 600.0
pyramid_compatable_shapes_to_arcseconds[(1440, 720)] = 900.0
pyramid_compatable_shapes_to_arcseconds[(720, 360)] = 1800
pyramid_compatable_shapes_to_arcseconds[(360, 180)] = 3600
pyramid_compatable_shapes_to_arcseconds[(180, 90)] = 7200
pyramid_compatable_shapes_to_arcseconds[(90, 45)] = 14400

## DEFINED IN CONFIG:
# geotransform_global_4deg = (-180.0, 4.0, 0.0, 90.0, 0.0, -4.0)
# geotransform_global_2deg = (-180.0, 2.0, 0.0, 90.0, 0.0, -2.0)
# geotransform_global_1deg = (-180.0, 1.0, 0.0, 90.0, 0.0, -1.0)
# geotransform_global_30m = (-180.0, 0.5, 0.0, 90.0, 0.0, -0.5)
# geotransform_global_15m = (-180.0, 0.25, 0.0, 90.0, 0.0, -0.25)
# geotransform_global_5m = (-180.0, 0.08333333333333333, 0.0, 90.0, 0.0, -0.08333333333333333)  # NOTE, the 0.08333333333333333 is defined very precisely as the answer a 64 bit compiled python gives from the answer 1/12 (i.e. 5 arc minutes)
# geotransform_global_30s = (-180.0, 0.008333333333333333, 0.0, 90.0, 0.0, -0.008333333333333333)  # NOTE, the 0.008333333333333333 is defined very precisely as the answer a 64 bit compiled python gives from the answer 1/120 (i.e. 30 arc seconds) Note that this has 1 more digit than 1/12 due to how floating points are stored in computers via exponents.
# geotransform_global_10s = (-180.0, 0.002777777777777778, 0.0, 90.0, 0.0, -0.002777777777777778)  # NOTE, the 0.002777777777777778 is defined very precisely

pyramid_compatible_geotransforms = OrderedDict()
pyramid_compatible_geotransforms[10.0] = (-180.0, 0.002777777777777778, 0.0, 90.0, 0.0, -0.002777777777777778)
pyramid_compatible_geotransforms[30.0] = (-180.0, 0.008333333333333333, 0.0, 90.0, 0.0, -0.008333333333333333)
pyramid_compatible_geotransforms[300.0] = (-180.0, 0.08333333333333333, 0.0, 90.0, 0.0, -0.08333333333333333)
pyramid_compatible_geotransforms[900.0] = (-180.0, 0.25, 0.0, 90.0, 0.0, -0.25)
pyramid_compatible_geotransforms[1800.0] = (-180.0, 0.5, 0.0, 90.0, 0.0, -0.5)
pyramid_compatible_geotransforms[3600.0] = (-180.0, 1.0, 0.0, 90.0, 0.0, -1.0)
pyramid_compatible_geotransforms[7200.0] = (-180.0, 2.0, 0.0, 90.0, 0.0, -2.0)
pyramid_compatible_geotransforms[14400.0] = (-180.0, 4.0, 0.0, 90.0, 0.0, -4.0)

pyramid_compatible_overview_levels = OrderedDict()
pyramid_compatible_overview_levels[10.0] = [3, 30, 90]
pyramid_compatible_overview_levels[30.0] = [10, 30]
pyramid_compatible_overview_levels[300.0] = [3]
pyramid_compatible_overview_levels[900.0] = []
pyramid_compatible_overview_levels[1800.0] = []
pyramid_compatible_overview_levels[3600.0] = []
pyramid_compatible_overview_levels[7200.0] = []
pyramid_compatible_overview_levels[14400.0] = []

pyramid_compatible_half_overview_levels = OrderedDict()
pyramid_compatible_half_overview_levels[10.0] = [2, 3, 6, 12, 24, 30, 60, 90]
pyramid_compatible_half_overview_levels[30.0] = [2, 4, 8, 10, 20, 30, 60]
pyramid_compatible_half_overview_levels[300.0] = [2, 3, 6, 12]
pyramid_compatible_half_overview_levels[900.0] = [2, 4]
pyramid_compatible_half_overview_levels[1800.0] = [2]
pyramid_compatible_half_overview_levels[3600.0] = []
pyramid_compatible_half_overview_levels[7200.0] = []
pyramid_compatible_half_overview_levels[14400.0] = []

pyramid_compatible_full_overview_levels = OrderedDict()
pyramid_compatible_full_overview_levels[10.0] = [2, 3, 2*3, 4*3, 8*3, 10*3, 20*3, 30*3, 60*3, 120*3, 240*3, 480*3, 960*3]
pyramid_compatible_full_overview_levels[30.0] = [2, 4, 8, 10, 20, 30, 60, 120, 240, 480, 960]
pyramid_compatible_full_overview_levels[300.0] = [2, 3, 6, 12, 24, 48, 96]
pyramid_compatible_full_overview_levels[900.0] = [2, 4, 8, 16, 32]
pyramid_compatible_full_overview_levels[1800.0] = [2, 4, 8, 16]
pyramid_compatible_full_overview_levels[3600.0] = [2, 4, 8]
pyramid_compatible_full_overview_levels[7200.0] = [2, 4]
pyramid_compatible_full_overview_levels[14400.0] = [2]

pyramid_ha_per_cell = {}
pyramid_ha_per_cell[10.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_10sec.tif')
pyramid_ha_per_cell[30.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_30sec.tif')
pyramid_ha_per_cell[300.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_300sec.tif')
pyramid_ha_per_cell[900.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_900sec.tif')
pyramid_ha_per_cell[1800.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_1800sec.tif')
pyramid_ha_per_cell[3600.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_3600sec.tif')
pyramid_ha_per_cell[7200.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_7200sec.tif')
pyramid_ha_per_cell[14400.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_14400sec.tif')

pyramid_ha_per_cell_column = {}
pyramid_ha_per_cell_column[10.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_10sec.tif')
pyramid_ha_per_cell_column[30.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_30sec.tif')
pyramid_ha_per_cell_column[300.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_300sec.tif')
pyramid_ha_per_cell_column[900.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_900sec.tif')
pyramid_ha_per_cell_column[1800.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_1800sec.tif')
pyramid_ha_per_cell_column[3600.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_3600sec.tif')
pyramid_ha_per_cell_column[7200.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_7200sec.tif')
pyramid_ha_per_cell_column[14400.0] = os.path.join(hb.BASE_DATA_DIR, 'pyramids', 'ha_per_cell_column_14400sec.tif')

global_esa_lulc_paths_by_year = {}
global_esa_lulc_paths_by_year[2000] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa", "full", "ESACCI-LC-L4-LCCS-Map-300m-P1Y-2000-v2.0.7.tif")
global_esa_lulc_paths_by_year[2010] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa", "full", "ESACCI-LC-L4-LCCS-Map-300m-P1Y-2010-v2.0.7.tif")
global_esa_lulc_paths_by_year[2014] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa", "full", "ESACCI-LC-L4-LCCS-Map-300m-P1Y-2014-v2.0.7.tif")
global_esa_lulc_paths_by_year[2015] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa", "full", "ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7.tif")

global_esa_seals5_lulc_paths_by_year = {}
global_esa_seals5_lulc_paths_by_year[2000] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa\simplified\lulc_esa_simplified_2000.tif")
global_esa_seals5_lulc_paths_by_year[2010] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa\simplified\lulc_esa_simplified_2010.tif")
global_esa_seals5_lulc_paths_by_year[2014] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa\simplified\lulc_esa_simplified_2014.tif")
global_esa_seals5_lulc_paths_by_year[2015] = os.path.join(hb.SEALS_BASE_DATA_DIR, "lulc_esa\simplified\lulc_esa_simplified_2015.tif")

global_bounding_box = [-180.0, -90.0, 180.0, 90.0]

def compare_sets(left_input, right_input, return_amount='partial', output_csv_path=None):
    left_set = set(left_input)
    right_set = set(right_input)

    union = left_set | right_set # union.
    intersection = left_set & right_set # intersection.
    left_difference = left_set - right_set # difference
    right_difference = right_set - left_set# difference
    symmetric_difference = left_set ^ right_set # symmetric difference



    if return_amount == 'all':
        output_dict = {}
        output_dict['left_set'] = list(left_set)
        output_dict['right_set'] = list(right_set)
        output_dict['union'] = list(union)
        output_dict['intersection'] = list(intersection)
        output_dict['left_only'] = list(left_difference)
        output_dict['right_only'] = list(right_difference)
        output_dict['symmetric_difference'] = list(symmetric_difference)

        L.info('Set 1: ' + str(len(left_set)) + ' ' + str(left_set))
        L.info('Set 2: ' + str(len(right_set)) + ' ' + str(right_set))
        L.info('union: ' + str(len(union)), union)
        L.info('intersection: ' + str(len(intersection)), intersection)
        L.info('left_only: ' + str(len(left_difference)), left_difference)
        L.info('right_only: ' + str(len(right_difference)), right_difference)
        L.info('symmetric_difference: ' + str(len(symmetric_difference)), symmetric_difference)

    elif return_amount == 'partial':
        output_dict = {}
        output_dict['intersection'] = list(intersection)
        output_dict['left_only'] = list(left_difference)
        output_dict['right_only'] = list(right_difference)

        L.info('intersection: ' + str(len(intersection)), intersection)
        L.info('left_only: ' + str(len(left_difference)), left_difference)
        L.info('right_only: ' + str(len(right_difference)), right_difference)

    longest_element = max([len(output_dict[i]) for i in output_dict.keys()])

    to_write = ','.join(list(output_dict.keys())) + '\n'
    for r in range(longest_element):
        for c in list(output_dict.keys()):
            if r < len(output_dict[c]):

                to_write += '\"' + output_dict[c][r] + '\"' + ','
            else:
                to_write += ','
        to_write += '\n'


    if output_csv_path:
        hb.write_to_file(to_write, output_csv_path)
        comparison_df = pd.read_csv(output_csv_path)
    else:
        from io import StringIO
        df_string = StringIO(to_write)

        comparison_df = pd.read_csv(df_string)
        # comparison_df = pd.read_csv(to_write)


    return output_dict


def fuzzy_merge(left_df, right_df, left_on, right_on, how='inner', cutoff=0.6):
    report = {}
    def get_closest_match(x, other, cutoff, report):
        matches = difflib.get_close_matches(x, other, n=20, cutoff=cutoff)

        if len(matches) > 0:
            if x != matches[0]:
                pass
                if x not in report:

                    report[x] = [matches[0], matches]
                    print ('   found matches for ', x, ': ', matches)
                return matches[0]
            else:
                L.debug('   found EXACT match for ', x, ': ', matches)
                report[x] = [matches[0], matches]
                return matches[0]
        else:
            L.debug('    found NO matches for ' , x)
            report[x] = ''
            return x

    left_uniques = pd.unique(left_df[left_on])
    right_uniques = pd.unique(right_df[right_on])

    right_df['original_right'] = right_df[right_on]
    right_df_copy = right_df.copy()

    print('right_df', right_df)
    print('right_dfr', right_df[right_on])

    replace_dict = {}
    for right_unique in right_uniques:
        print('right_unique', right_unique)
        possible_matches = get_closest_match(right_unique, left_uniques, cutoff, report)
        print('possible_matches', possible_matches)
        replace_dict[right_unique] = possible_matches

    print('right_df111', right_df)
    print('replace_dict', replace_dict)
    right_df[right_on].replace(replace_dict, inplace=True)
    print('right_df1112', right_df)

    # # Apply the get_closest_match for each x in right_df merge column.
    # # This is VERY unoptimized but meh for now.
    # # Save it in a new left_on column in the right_df df.
    # right_df_copy[left_on] = [get_closest_match(x, left_df[left_on], cutoff, report)
    #                      for x in right_df_copy[right_on]]


    # Return the merged output along with a report on what happened.
    return left_df.merge(right_df, on=left_on, how=how), report



def get_blocksize_from_path(input_path):
    ds = gdal.OpenEx(input_path)
    blocksize = ds.GetRasterBand(1).GetBlockSize()
    return blocksize

def get_compression_type_from_path(input_path):
    ds = gdal.OpenEx(input_path)
    image_structure = ds.GetMetadata('IMAGE_STRUCTURE')
    if "COMPRESSION" in image_structure:
        return image_structure['COMPRESSION']
    else:
        return 'Didnt detect compression.'

def rewrite_array_with_new_blocksize(input_path, output_path, desired_blocksize):
    if desired_blocksize == 'full_stripe':
        output_blocksize = [hb.get_shape_from_dataset_path(input_path)[1], 1]
        dst_options = ['TILED=NO', 'BIGTIFF=YES', 'COMPRESS=DEFLATE']  # NO tiling cause striding. They're all in a stripe!
    elif desired_blocksize == 'block_default':
        dst_options = hb.DEFAULT_GTIFF_CREATION_OPTIONS
    elif type(desired_blocksize) is list:
        if len(desired_blocksize) == 2:
            if desired_blocksize[0] > 1 and desired_blocksize[1] > 1:
                dst_options = ['TILED=YES', 'BIGTIFF=YES', 'COMPRESS=DEFLATE', 'BLOCKXSIZE=' + str(desired_blocksize[0]), 'BLOCKYSIZE=' + str(desired_blocksize[1])]
            else:
                dst_options = ['TILED=NO', 'BIGTIFF=YES', 'COMPRESS=DEFLATE', 'BLOCKXSIZE=' + str(desired_blocksize[0]), 'BLOCKYSIZE=' + str(desired_blocksize[1])]
        else:
            raise NameError('Unable to interpret inputs for ', input_path)
    else:
        raise NameError('Unable to interpret inputs for rewrite_array_with_new_blocksize on ', input_path)

    swap_filenames_at_end = False
    if input_path == output_path:
        swap_filenames_at_end = True
        output_path = hb.rsuri(output_path, 'pre_swap')


    input_blocksize = get_blocksize_from_path(input_path)
    input_compression_type = get_compression_type_from_path(input_path)

    ds = gdal.Open(input_path)
    band = ds.GetRasterBand(1)

    read_callback = hb.make_logger_callback("ReadAsArray percent complete:")
    input_array = band.ReadAsArray(callback=read_callback, callback_data=[input_path])

    data_type = hb.get_datatype_from_uri(input_path)
    geotransform = hb.get_geotransform_path(input_path)
    projection = hb.get_dataset_projection_wkt_uri(input_path)
    ndv = hb.get_ndv_from_path(input_path)



    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(output_path, input_array.shape[1], input_array.shape[0], 1, data_type, dst_options)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(projection)
    ndv = -9999.0
    dst_ds.GetRasterBand(1).SetNoDataValue(ndv)

    write_callback = hb.make_logger_callback("WriteArray percent complete:")
    dst_ds.GetRasterBand(1).WriteArray(input_array, callback=write_callback, callback_data=[output_path])

    dst_ds = None # Necessary for filename swap
    ds = None # Necessary for filename swap

    if swap_filenames_at_end:
        hb.swap_filenames(output_path, input_path)



def get_global_block_list_from_resolution(processing_block_size, raster_resolution):
    """Get list of 6-length lists that define tiles of the world, based only on coarse and fine resolutions. Returns list of lists.

    Return: [ul fine col, ul fine row, fine width, fine height, coarse col, coarse row]
    """
    n_h_blocks = int(360.0 / float(processing_block_size))
    n_v_blocks = int(180.0 / float(processing_block_size))
    n_blocks = n_h_blocks * n_v_blocks

    block_list = []
    block_size = processing_block_size / raster_resolution
    for h_b in range(n_h_blocks):

        for v_b in range(n_v_blocks):
            block_list.append([int(h_b * block_size), int(v_b * block_size), int(block_size), int(block_size), int(h_b), int(v_b)])

    return block_list

def get_global_block_list_from_resolution_and_bb(processing_block_size, raster_resolution, bb):
    """Get list of 6-length lists that define tiles that iterate over the bounding box. Note that the bounds of the BB must be a multiple of
    the coarse resolution, based only on coarse and fine resolutions. Returns list of lists.

    Return: [ul fine col, ul fine row, fine width, fine height, coarse col, coarse row]
    """
    x_min_deg = bb[0]
    y_min_deg = bb[1]
    x_max_deg = bb[2]
    y_max_deg = bb[3]

    n_h_blocks = int((x_max_deg - x_min_deg) / float(processing_block_size))
    n_v_blocks = int((y_max_deg - y_min_deg) / float(processing_block_size))
    n_blocks = n_h_blocks * n_v_blocks

    block_size = processing_block_size / raster_resolution

    left_offset_h_blocks = math.floor((180. + x_min_deg) / float(processing_block_size))
    left_offset_h_pixels = left_offset_h_blocks * block_size
    top_offset_v_blocks = math.ceil((90. + y_min_deg) / float(processing_block_size))
    top_offset_v_pixels = top_offset_v_blocks * block_size
    block_list = []
    for h_b in range(n_h_blocks):

        for v_b in range(n_v_blocks):
            block_list.append([int((h_b * block_size) + left_offset_h_pixels), int((v_b * block_size) + top_offset_v_pixels), int(block_size), int(block_size), int(h_b), int(v_b)])

    return block_list

def get_subglobal_block_list_from_resolution_and_bb(processing_block_size, raster_resolution, bb):
    """Get list of 6-length lists that define tiles that iterate over the bounding box. Note that the bounds of the BB must be a multiple of
    the coarse resolution, based only on coarse and fine resolutions. Returns list of lists.

    Return: [ul fine col, ul fine row, fine width, fine height, coarse col, coarse row]
    """
    x_min_deg = bb[0]
    y_min_deg = bb[1]
    x_max_deg = bb[2]
    y_max_deg = bb[3]

    n_h_blocks = int((x_max_deg - x_min_deg) / float(processing_block_size))
    n_v_blocks = int((y_max_deg - y_min_deg) / float(processing_block_size))
    n_blocks = n_h_blocks * n_v_blocks

    block_size = processing_block_size / raster_resolution

    # TODOO actually eliminate rather than set as zero
    left_offset_h_blocks = 0
    left_offset_h_pixels = left_offset_h_blocks * block_size
    top_offset_v_blocks = 0
    top_offset_v_pixels = top_offset_v_blocks * block_size
    block_list = []
    for h_b in range(n_h_blocks):

        for v_b in range(n_v_blocks):
            block_list.append([int((h_b * block_size) + left_offset_h_pixels), int((v_b * block_size) + top_offset_v_pixels), int(block_size), int(block_size), int(h_b), int(v_b)])

    return block_list

def determine_pyramid_resolution(input_path):
    """ Check if input_path has a resolution the is exactly equal or close to a pyramid-supported resolution.

    Return the input resolution if correct, the snapped-to resolution if close enough. Otherwise raise exception."""
    ds = gdal.OpenEx(input_path)
    if ds is None:
        raise Exception('Could not open ' + str(input_path))
    gt = ds.GetGeoTransform()
    ulx, xres, _, uly, _, yres = gt[0], gt[1], gt[2], gt[3], gt[4], gt[5]

    resolution = None
    if xres in pyramid_compatible_resolutions.keys():
        resolution = xres
    else:
        for k, v in pyramid_compatible_resolution_bounds.items():
            if v[0] < xres < v[1]:
                resolution = pyramid_compatible_resolutions[k]
                if resolution != xres:
                    L.info('Input res was ' + str(xres) + ' for ' + str(input_path) + ' but should have been ' + str(resolution) + ' to make pyramid-ready.')

    if resolution is None:

        L.warning('determine_pyramid_resolution found no suitably close resolution for ' + str(input_path) + ' with ulx, xres, uly, yres of ' + str(ulx) + ' ' + str(xres) + ' ' + str(uly) + ' ' + str(yres) + ' ')
        return None
    ds = None
    return resolution
def make_paths_list_global_pyramid(
        input_paths_list,
        output_paths_list=None,
        make_overviews=True,
        overwrite_overviews=False,
        calculate_stats=True,
        overwrite_stats=False,
        clean_temporary_files=False,
        raise_exception=False,
        make_overviews_external=True,
        set_ndv_below_value=None,
        verbose=False
):

    num_workers = max(min(multiprocessing.cpu_count() - 1, len(input_paths_list)), 1)

    if verbose:
        L.info('Creating multiprocessing worker pool of size ' + str(num_workers))
    worker_pool = multiprocessing.Pool(num_workers)  # NOTE, worker pool and results are LOCAL variabes so that they aren't pickled when we pass the project object.

    initial_test = []
    for path in input_paths_list:
        initial_test.append(hb.is_path_global_pyramid(path))
    if verbose:
        L.info('Tested input_paths list and the following were not globally pyramidal: ' + str([i for c, i in enumerate(input_paths_list) if not initial_test[c]]))

    if not all(initial_test):
        input_paths_list = [i for c, i in enumerate(input_paths_list) if not initial_test[c]]
        finished_results = []
        if output_paths_list is None:
            output_paths_list = [None for i in input_paths_list]
        parsed_iterable = [(input_paths_list[c],
                            output_paths_list[c],
                            make_overviews,
                            overwrite_overviews,
                            calculate_stats,
                            overwrite_stats,
                            clean_temporary_files,
                            raise_exception,
                            make_overviews_external,
                            set_ndv_below_value,
                            verbose)
                                for c, i in enumerate(input_paths_list)]

        if verbose:
            L.info('About to launch parallel process on the following parsed_iterable:\n' + hb.pp(parsed_iterable, return_as_string=True))
        result = worker_pool.starmap_async(make_path_global_pyramid, parsed_iterable)
        for i in result.get():
            finished_results.append(i)
        worker_pool.close()
        worker_pool.join()
    # FOR REFERENCE. here is the old apply_async approach
    # results = []
    # finished_results = []
    # num_simultaneous = 80
    # starting_c = 0
    # for w in range(num_simultaneous):
    #     for c in range(starting_c, starting_c + num_simultaneous):
    #         if c < len(input_paths_list):
    #
    #             path = input_paths_list[c]
    #
    #             if output_paths_list is not None:
    #                 output_path = output_paths_list[c]
    #             else:
    #                 output_path = None
    #             L.info('Running make_paths_list_global_pyramid in parallel for ' + path)
    #
    #
    #             result = worker_pool.apply_async(func=make_path_global_pyramid, args=(path,
    #                                                                                   output_path,
    #                                                                                   make_overviews,
    #                                                                                   overwrite_overviews,
    #                                                                                   calculate_stats,
    #                                                                                   overwrite_stats,
    #                                                                                   clean_temporary_files,
    #                                                                                   raise_exception,
    #                                                                                   make_overviews_external,
    #                                                                                   set_ndv_below_value,
    #                                                                                   verbose)
    #                                              )
    #
    #         # Note this keeps it in memory, and can hit limits.
    #         results.append(result)
    #     starting_c = starting_c + num_simultaneous
    #
    #     for i in results:
    #         finished_results.append(i.get())
    #         del i
    #         # print ('i', i, i.get())
    #         #
    #         # for j in i.get():
    #         #     if j is not None:
    #         #         finished_results.append(j)
    #
    # worker_pool.close()
    # worker_pool.join()


def resample_to_match_pyramid(input_path,
                      match_path,
                      output_path,
                      resample_method='bilinear',
                      output_data_type=None,
                      src_ndv=None,
                      ndv=None,
                      s_srs_wkt=None,
                      compress=True,
                      ensure_fits=False,
                      gtiff_creation_options=hb.DEFAULT_GTIFF_CREATION_OPTIONS,
                      calc_raster_stats=False,
                      add_overviews=False,
                      pixel_size_override=None,
                      remove_intermediate_files=False,
                      verbose=False,
                      ):

    if verbose:
        original_level = L.getEffectiveLevel()
        L.setLevel(logging.DEBUG)

    if hb.assert_paths_same_pyramid(input_path, match_path):
        L.debug('Both input and match are same pyramids already.')
        return

    # if not hb.is_path_global_pyramid(input_path):
    #     raise NameError('Non-pyramidal path given to match_path for resample_to_match_pyramid: ' + str(match_path))

    if hb.assert_gdal_paths_have_same_geotransform(input_path):
        requires_resample = False
    else:
        requires_resample = True

    if requires_resample:

        temp_resample_path = hb.temp('.tif', 'temp_resample', remove_intermediate_files, os.path.split(output_path)[0])

        hb.resample_to_match(input_path,
                             match_path,
                             output_path,
                             resample_method=resample_method,
                             output_data_type=output_data_type,
                             src_ndv=src_ndv,
                             ndv=ndv,
                             s_srs_wkt=s_srs_wkt,
                             compress=compress,
                             ensure_fits=ensure_fits,
                             gtiff_creation_options=gtiff_creation_options,
                             calc_raster_stats=calc_raster_stats,
                             add_overviews=add_overviews,
                             pixel_size_override=pixel_size_override,
                             verbose=verbose,
                             )

        # if hb.is_path_global_pyramid(temp_resample_path):
        #     L.debug('Path was pyramidal after resample. Renaming to ' + str(output_path))
        #     hb.rename_with_overwrite(temp_resample_path, output_path)
        # else:
        hb.make_path_global_pyramid(output_path)
    else:

        hb.make_path_global_pyramid(input_path, output_path=output_path)

    if verbose:
        L.setLevel(original_level)

def assert_path_global_pyramid(input_path):
    try:
        result = is_path_global_pyramid(input_path)
    except Exception as e:
        raise NameError('assert_path_global_pyramid failed on ', input_path, 'with exception', e)
    if not result:
        raise NameError('assert_path_global_pyramid failed on ', input_path)

def is_path_global_pyramid(input_path):
    """Fast method for testing if path is pyramidal."""
    to_return = True

    res = hb.determine_pyramid_resolution(input_path)

    if res is None:
        L.critical('Not pyramid because no suitable resolution was found: ' + str(input_path))
        return False

    gt = hb.get_geotransform_path(input_path)

    if not pyramid_compatible_geotransforms[pyramid_compatible_resolution_to_arcseconds[res]] == gt:
        L.critical('Not pyramid because geotransform was not pyramidal. Found ' + str(gt) + ' which was not equal to ' + str(pyramid_compatible_geotransforms[pyramid_compatible_resolution_to_arcseconds[res]]) + ' for: '  + str(input_path))
        to_return = False

    ds = gdal.OpenEx(input_path)
    image_structure = ds.GetMetadata('IMAGE_STRUCTURE')
    compression = image_structure.get('COMPRESSION', None)

    # Check if compressed (pyramidal file standards require compression)
    if str(compression).lower() not in ['deflate']:
        L.critical('Not a global pyramid because compression was not deflate: ' + str(input_path))
        to_return = False

    data_type = ds.GetRasterBand(1).DataType
    ndv = ds.GetRasterBand(1).GetNoDataValue()

    if data_type == 1:
        if ndv != 255:
            L.critical('Not pyramid because ndv was not 255 and datatype was 1: ' + str(input_path))
            to_return = False
    elif data_type < 6:
        if ndv != 9999:  # NOTE INT
            L.critical('rNot pyramid because ndv was not 9999 and datatype was of int type: ' + str(input_path))
            to_return = False
    else:
        if ndv != -9999.0:
            L.critical('Not pyramid because ndv was not -9999.0 and datatype was > 5 (i.e. is a float): ' + str(input_path))
            to_return = False

    if to_return:
        return True
    else:
        return False

def make_vector_path_global_pyramid(input_path, output_path=None, pyramid_index_columns=None, drop_columns=False,
                                    clean_temporary_files=False, verbose=False):
    """A pyramidal vector file requires that it have bb information (optionall minx, miny separate), a pyramid_id that is composed of name-id pairs of potential zones.

    pyramid_id may be large, hence also have pyramid_id which starts at 1

    If specifying pyramid_index_columns, it will smartly create an index according to the following logic:
        if the column type is int64able, it is an unnamed int pyramid_index
        if the column is not int64able, it is a named pyramid index and also generates a <name>_as_id column that is int64

    """
    if drop_columns is False:
        drop_columns = []

    if os.path.splitext(input_path)[1] != 'gpkg':
        input_is_not_gpkg = True

    try:
        if os.path.splitext(input_path)[1].lower() == 'gpkg':
            gdf = gpd.read_file(input_path, driver='GPKG')
        elif os.path.splitext(input_path)[1].lower() == 'shp':
            gdf = gpd.read_file(input_path, driver='ESRI Shapefile')
        else:
            gdf = gpd.read_file(input_path)
    except NameError as exception:
        raise NameError('Unable to read GPKG at ' + str(input_path) + ' and encountered exception: ' + str(exception))

    rewrite_necessary = False
    dissolved_gdf = None

    if 'bb' not in gdf.columns:
        if verbose:
            L.info('bb not in vector attributes so rewriting.')
        gdf['bb'] = gdf.bounds.minx.astype(str) + ',' + gdf.bounds.miny.astype(str) + ',' + gdf.bounds.maxx.astype(str) + ',' + gdf.bounds.maxy.astype(str)
        gdf['minx'] = gdf.bounds.minx.astype(float)
        gdf['miny'] = gdf.bounds.miny.astype(float)
        gdf['maxx'] = gdf.bounds.maxx.astype(float)
        gdf['maxy'] = gdf.bounds.maxy.astype(float)
        rewrite_necessary = True

    if 'pyramid_id' not in gdf.columns or pyramid_index_columns is not None:
        rewrite_necessary = True
        if verbose:
            L.info('pyramid_id not in vector so rewriting.')
        if pyramid_index_columns is None:
            raise NameError('Unable to make vector file a global pyramid because there was no preexisting pyramid_id column and no pyramid_index_columns argument was given.')

        # First sanitize names:
        rename_dict = {}
        for name in pyramid_index_columns:
            if name.lower() != name:
                rename_dict[name] = name.lower()
        # pyramid_index_columns = list(rename_dict.values())
        pyramid_index_columns = [i.lower() for i in pyramid_index_columns]
        gdf.rename(columns=rename_dict, inplace=True)

        updated_pyramid_index_columns = []
        updated_pyramid_names_columns = []
        columns_to_add_ids = []

        gdf = gdf.dropna(subset=pyramid_index_columns)

        # Iterate through the columns that will define the pyramidal structure in REVERSE because the first listed is the final sort.
        for column_name in pyramid_index_columns:
            try:
                gdf[column_name] = gdf[column_name].fillna(0).astype(np.int64)
                column_intable = True
            except Exception as e:
                L.debug('In try, came accross exception ' + str(e))
                column_intable = False


            # For intable indices, only need to rename and move them.
            if column_intable is True:
                validated_column_id =  column_name.lower() + '_pyramid_id'
                updated_pyramid_index_columns.append(validated_column_id)
                gdf.rename(columns={column_name: validated_column_id}, inplace=True)

                # Sort the by the new column id
                gdf = gdf.iloc[gdf[validated_column_id].sort_values().index.values] #.astype(np.int64)



            # But for columns that are not ints, need to add a new name after a complex sort.
            else:
                validated_column_name = column_name.lower() + '_pyramid_name'
                updated_pyramid_names_columns.append(validated_column_name)
                columns_to_add_ids.append(column_name.lower())
                validated_column_id = column_name.lower() + '_pyramid_id'
                updated_pyramid_index_columns.append(validated_column_id)

                # LEARNING POINT WTF, underscore comes between capital and lowercase letters. Sorting thus is borked. Best fix is to replace understcores with something that does sort right. WTFingF.

                unique_values = list(np.unique(gdf[column_name][gdf[column_name].notnull()]))
                ascii_fixed_unique_values = [str(i).replace('_', '%') for i in unique_values]
                unique_sorted_values = [str(i).replace('%', '_') for i in sorted(ascii_fixed_unique_values)]

                replacement_dict = {v: c + 1 for c, v in enumerate(unique_sorted_values)}

                L.info('Generated replacement dict for pyramid id on ' + str(column_name) + ': ' + str(replacement_dict))
                # gdf[validated_column_name] = gdf[column_name]
                gdf.rename(columns={column_name: validated_column_name}, inplace=True)
                gdf[validated_column_id] = gdf[validated_column_name].replace(replacement_dict).astype(np.int64)
                # Sort the by the new column id
                gdf = gdf.iloc[gdf[validated_column_id].sort_values().index.values]


        # Generate a concatenation of all pyramids in int form

        # Generate actual pyramid id
        for c, column_name in enumerate(updated_pyramid_index_columns):
            if column_name.endswith('_pyramid_id'):
                if 'pyramid_ids_concatenated' not in gdf.columns:
                    gdf['pyramid_ids_concatenated'] = gdf[column_name].map(np.int64).map(str)
                else:
                    gdf['pyramid_ids_concatenated'] = gdf['pyramid_ids_concatenated'].map(str) + '_' + gdf[column_name].map(np.int64).map(str)

                if 'pyramid_ids_multiplied' not in gdf.columns:
                    gdf['pyramid_ids_multiplied'] = gdf[column_name].map(np.int64)
                else:
                    gdf['pyramid_ids_multiplied'] = gdf['pyramid_ids_multiplied'].map(np.int64) * 1000 + gdf[column_name].map(np.int64)

        # Check to see if the resultant pyramid_ids are unique. If not, write a secondary file *_dissolved that combines these polygons to make it unique
        unique_pyramid_ids = np.unique(gdf['pyramid_ids_multiplied'])
        pyramid_ordered_ids_dict = {v: c + 1 for c, v in enumerate(list(unique_pyramid_ids))}
        gdf['pyramid_id'] = gdf['pyramid_ids_multiplied'].apply(lambda x: pyramid_ordered_ids_dict[x])
        # gdf['pyramid_id'] = gdf['pyramid_id'].apply(lambda x: pyramid_ordered_ids_dict[x])

        # Reorder to put pyramid cols first.
        drop_columns.append('dissolve_col')
        updated_pyramid_index_columns = ['pyramid_id'] + ['pyramid_ids_concatenated'] + ['pyramid_ids_multiplied'] + updated_pyramid_index_columns + updated_pyramid_names_columns
        columns_ordered = updated_pyramid_index_columns + [i for i in gdf.columns if i not in updated_pyramid_index_columns and i not in drop_columns]
        gdf = gdf[columns_ordered]

        from shapely.geometry.polygon import Polygon
        from shapely.geometry.multipolygon import MultiPolygon

        # Learning point, I encountered an error with invalid geometries. I fixed it by both converting to Multipolygons AND running feature.buffer().
        # the above worked, this is fraught if there's invalid geometry. It
        # appears there is no good way of fixing invalid geometry cause each case is different.
        try:
            gdf["geometry"] = [MultiPolygon([feature.buffer(0)]) if type(feature) == Polygon else feature.buffer(0) for feature in gdf["geometry"]]
        except:
            print ('Tried the bugger and multipolygon trick but that didnt work. Miiiiight not matter but be cautious.')

        if len(unique_pyramid_ids) < len(gdf['pyramid_id']):
            L.info('Found non-unique pyramid_id, so creating new geopackage with dissolved_gdf polygons.')

            # Add copy of column to be dissolved on cause it disappears on dissolve.
            gdf['dissolve_col'] = gdf['pyramid_id']

            # Save it as gtap_aez_dissolved
            dissolved_gdf = gdf.dissolve(by='dissolve_col')

            dissolved_gdf_path = hb.suri(output_path, 'dissolved')

            # Need to rewrite BB info cause disolving changed this.
            dissolved_gdf['bb'] = dissolved_gdf.bounds.minx.astype(str) + ',' + dissolved_gdf.bounds.miny.astype(str) + ',' + dissolved_gdf.bounds.maxx.astype(str) + ',' + dissolved_gdf.bounds.maxy.astype(str)
            dissolved_gdf['minx'] = dissolved_gdf.bounds.minx.astype(float)
            dissolved_gdf['miny'] = dissolved_gdf.bounds.miny.astype(float)
            dissolved_gdf['maxx'] = dissolved_gdf.bounds.maxx.astype(float)
            dissolved_gdf['maxy'] = dissolved_gdf.bounds.maxy.astype(float)

        gdf = gdf.sort_values('pyramid_id')
        if dissolved_gdf is not None:
            dissolved_gdf = dissolved_gdf.sort_values('pyramid_id')

        # Reorder to put pyramid cols first.
        # updated_pyramid_index_columns = ['pyramid_id', 'pyramid_ids_concatenated'] + updated_pyramid_index_columns
        columns_ordered = updated_pyramid_index_columns + [i for i in gdf.columns if i not in updated_pyramid_index_columns and i not in drop_columns]
        gdf = gdf[columns_ordered]

        if dissolved_gdf is not None:
            dissolved_gdf = dissolved_gdf[columns_ordered]


    if rewrite_necessary is True:

        # Rename files to displace old input. This has to be done before external-file operations are completed.
        displacement_path = hb.temp('.gpkg', filename_start=hb.file_root(input_path) + '_displaced_' + hb.random_string(), folder=os.path.split(input_path)[0], remove_at_exit=clean_temporary_files)
        temp_write_path = hb.temp('.gpkg', filename_start=hb.file_root(input_path) + '_temp_write_' + hb.random_string(), folder=os.path.split(input_path)[0], remove_at_exit=clean_temporary_files)

        if output_path:
            layer_name = hb.file_root(output_path)
        else:
            layer_name = hb.file_root(input_path)

        # LEARNING POINT, when importing a shapefile that had a float-style fid, which is interpretted by fiona as the SQL primary key, there was a
        # File "fiona/ogrext.pyx", line 1173, in fiona.ogrext.WritingSession.start
        # fiona.errors.SchemaError: Wrong field type for fid
        # error that arose. Solution for now was to rewrite fids as ints64.
        for current_gdf in [gdf, dissolved_gdf]:
            if current_gdf is not None:
                if 'fid' in current_gdf.columns:
                    if current_gdf['fid'].dtype != np.int64:
                        current_gdf['fid'] = current_gdf['fid'].astype(np.int64)

        # gdf = gdf.drop('dissolve_col', 1)
        # dissolved_gdf = dissolved_gdf.drop('dissolve_col', 1)
        # if 'dissolve_col' in gdf.columns:
        #     gdf = gdf.drop('dissolve_col', 1)
        if dissolved_gdf is not None:
            # LEARNING POINT, I messed up dropping dissolve_col because it was the INDEX, and thus was not in dissolved_gdf.columns
            # dissolved_gdf = dissolved_gdf[[i for i in dissolved_gdf.columns if i != 'dissolve_col']]
            dissolved_gdf.set_index('pyramid_id', inplace=True)

        # Writing logic: if no output path given, rename input path to displacement path then write on input path.
        if output_path:
            hb.create_directories(os.path.split(str(output_path))[0])

            if dissolved_gdf is not None:
                try:
                    dissolved_gdf = dissolved_gdf[[i for i in dissolved_gdf.columns if i != 'dissolve_col']]
                    dissolved_gdf.to_file(str(output_path), driver='GPKG')
                except NameError as e:
                    raise NameError('Unable to write GPKG. Encountered exception: ' + str(e))

                try:
                    gdf.to_file(hb.suri(str(output_path), 'pre_dissolve'), driver='GPKG')
                except NameError as e:
                    raise NameError('Unable to write GPKG. Encountered exception: ' + str(e))
            else:

                try:
                    gdf.to_file(str(output_path), driver='GPKG')
                except NameError as e:
                    raise NameError('Unable to write GPKG. Encountered exception: ' + str(e))

        else:
            if dissolved_gdf is not None:
                try:
                    dissolved_gdf.to_file(temp_write_path, driver='GPKG')
                except NameError as e:
                    raise NameError('Unable to write GPKG. Encountered exception: ' + str(e))

                try:
                    gdf.to_file(hb.suri(input_path, 'pre_dissolve'), driver='GPKG')
                except NameError as e:
                    raise NameError('Unable to write GPKG. Encountered exception: ' + str(e))
            else:
                try:
                    gdf.to_file(temp_write_path, driver='GPKG')
                except NameError as e:
                    raise NameError('Unable to write GPKG. Encountered exception: ' + str(e))

            if os.path.exists(temp_write_path):
                os.rename(input_path, displacement_path)
                os.rename(temp_write_path, input_path)

def resample_via_pyramid_overviews(input_path, output_resolution, output_path, force_overview_rewrite=False, overview_resampling_algorithm=None, new_ndv=None,
                                   overview_data_types=None, assert_pyramids=True, scale_array_by_resolution_change=False):
    if assert_pyramids:
        hb.assert_path_global_pyramid(input_path)
    output_shape = hb.pyramid_compatable_shapes[output_resolution]
    raster_statistics = hb.read_raster_stats(input_path)
    input_deg_resolution = hb.get_cell_size_from_path(input_path)
    input_resolution = hb.pyramid_compatible_resolution_to_arcseconds[input_deg_resolution]

    input_resolution = hb.determine_pyramid_resolution(input_path)
    input_resolution_in_arcseconds = hb.pyramid_compatible_resolution_to_arcseconds[input_resolution]
    overview_level = None
    if overview_data_types is None:
        overview_data_types = hb.get_datatype_from_uri(input_path)

    if 'overviews' in raster_statistics:
        for c, i in enumerate(raster_statistics['overviews']):
            if output_shape == i['size']:
                overview_level = c

    if overview_level is None or force_overview_rewrite:
        L.info('resample_via_pyramid_overviews triggered rewrite of overviews. overview_level', overview_level, 'force_overview_rewrite', force_overview_rewrite)

        if output_resolution not in hb.pyramid_compatible_overview_levels:
            raise NameError('resample_via_pyramid_overviews on', input_path, 'did not seem to need overviews. Is it already low res?')

        if new_ndv is not None:

            old_ndv = hb.get_ndv_from_path(input_path)
            temp_path = hb.temp()

            # START HERE, the binary data type wasn't working on this type of data because it was still in byte format and thus the average failed.
            hb.raster_calculator_af_flex(input_path, lambda x: np.where(x == old_ndv, new_ndv, x), temp_path, datatype=overview_data_types)
            hb.set_ndv_in_raster_header(input_path, new_ndv)
            hb.swap_filenames(input_path, temp_path)

        hb.add_overviews_to_path(input_path, specific_overviews_to_add=hb.pyramid_compatible_overview_levels[input_resolution_in_arcseconds],
                                 overview_resampling_algorithm=overview_resampling_algorithm, make_pyramid_compatible=True)

        # Get the specific overview_level from where they output resolution was in the dictionary.
        # NOTE the cool but confusing method by which i get the position in the resample list via the ratio of arcescond resolutions.
        # this works because overview levels are defined as multiples of the input resolution.
        overview_level =  list(hb.pyramid_compatible_overview_levels[input_resolution_in_arcseconds]).index(int(output_resolution / input_resolution_in_arcseconds))


        L.info('Rewrote overviews and set overview_level to', overview_level)
    ds = gdal.OpenEx(input_path)
    band = ds.GetRasterBand(1)
    overview_band = band.GetOverview(overview_level)
    overview_array = overview_band.ReadAsArray()

    if scale_array_by_resolution_change:
        scaler = (output_resolution / input_resolution_in_arcseconds) ** 2
        L.info('Multiplying resampled output by ', scaler, 'based on difference in resolutions. This means you are multiplying something that is in a fixed areal, like hectares, which will change when the resolution changes.')
        overview_array *= scaler

    n_rows, n_cols = overview_array.shape
    hb.save_array_as_geotiff(overview_array, output_path, input_path, n_cols=n_cols, n_rows=n_rows, geotransform_override=hb.pyramid_compatible_geotransforms[output_resolution])



    # if output_resolution in [i['size'] for i in raster_statistics['overviews']]:

def make_path_global_pyramid(
        input_path,
        output_path=None,
        make_overviews=True,
        overwrite_overviews=False,
        calculate_stats=True,
        overwrite_stats=False,
        clean_temporary_files=False,
        raise_exception=False,
        make_overviews_external=True,
        set_ndv_below_value=None,
        write_unique_values_list=False,
        overview_resample_method=None,
        verbose=False
):
    """Throw exception if input_path is not pyramid-ready. This requires that the file be global, geographic projection, and with resolution
    that is a factor/multiple of arcdegrees.

    If output_path is specified, write to that location. Otherwise, make changes in-place but saving a temporary backup file of the input.

    # LEARNING POINT: Able to access specific overview bands!
    # ovr_band = src_ds.GetRasterBand(i).GetOverview(1)

    write_unique_values_list = True makes it write to the xml stats file a comma separated list of unique values
    """

    # TODOO write_unique_values_list unimplemented but good idea for fasterstats.
    if verbose:
        L.info('Running make_path_global_pyramid on ' + str(input_path))

    resolution = hb.determine_pyramid_resolution(input_path)
    arcseconds = pyramid_compatible_resolution_to_arcseconds[resolution]

    ds = gdal.OpenEx(input_path)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    gt = ds.GetGeoTransform()

    ulx, xres, _, uly, _, yres = gt[0], gt[1], gt[2], gt[3], gt[4], gt[5]
    if verbose:
        L.info('   ulx: ' + str(ulx) + ', uly: ' + str(uly) + ', xres: ' + str(xres) + ', yres: ' + str(yres) + ', n_c: ' + str(n_c) + ', n_r: ' + str(n_r))

    if -180.001 < ulx < -179.999:
        ulx = -180.0
    if 90.001 > uly > 89.999:
        uly = 90.0

    if ulx != -180.0 or uly != 90.0:
        result_string = 'Input path not pyramid ready because UL not at -180 90 (or not close enough): ' + str(input_path)
        if raise_exception:
            raise NameError(result_string)
        else:
            L.info(result_string)
            return False
    lrx = ulx + resolution * n_c
    lry = uly + -1.0 * resolution * n_r

    if lrx != 180.0 or lry != -90.0:

        result_string = 'Input path not pyramid ready because its not the right size: ' + str(input_path) + '\n    ulx ' + str(ulx) + ', xres ' + str(xres) + ', uly ' + str(uly) + ', yres ' + str(yres) + ', lrx ' + str(lrx) + ', lry ' + str(lry)
        if raise_exception:
            raise NameError(result_string)
        else:
            L.warning(result_string)
            return False

    output_geotransform = pyramid_compatible_geotransforms[arcseconds]
    ds = None

    if output_geotransform != gt:
        L.warning('Changing geotransform of ' + str(input_path) + ' to ' + str(output_geotransform) + ' from ' + str(gt))

    hb.set_geotransform_to_tuple(input_path, output_geotransform)

    ds = gdal.OpenEx(input_path, gdal.GA_Update)
    md = ds.GetMetadata()
    image_structure = ds.GetMetadata('IMAGE_STRUCTURE')
    compression = image_structure.get('COMPRESSION', None)
    if verbose:
        L.info('Compression of ' + str(input_path) + ': ' + str(compression))

    # Consider operations that may need rewriting the underlying data
    rewrite_array = False

    # Check if compressed (pyramidal file standards require compression)
    if str(compression).lower() not in  ['deflate']:
        L.critical('rewrite_array triggered because compression was not deflate.')
        rewrite_array = True

    data_type = ds.GetRasterBand(1).DataType
    ndv = ds.GetRasterBand(1).GetNoDataValue()

    if data_type >= 6:
        options = (
            'TILED=YES',
            'BIGTIFF=YES',
            'COMPRESS=DEFLATE',
            'BLOCKXSIZE=256',
            'BLOCKYSIZE=256',
            'PREDICTOR=3',
        )
    else:
        options = hb.DEFAULT_GTIFF_CREATION_OPTIONS

    new_ndv = False
    below_ndv = False
    if verbose:
        L.info('input data_type: ' + str(data_type) + ', input ndv: ' + str(ndv))
    if data_type == 1:
        if ndv != 255:
            old_ndv = ndv
            ndv = 255
            L.critical('rewrite_array triggered because ndv was not 255 and datatype was 1.')
            rewrite_array = True
            new_ndv = True
    elif data_type < 6:
        if ndv != 9999:  # NOTE INT
            old_ndv = ndv
            ndv = 9999
            L.critical('rewrite_array triggered because ndv was not 9999 and datatype was of int type.')
            rewrite_array = True
            new_ndv = True
    else:
        if ndv != -9999.0:
            old_ndv = ndv
            ndv = -9999.0
            L.critical('rewrite_array triggered because ndv was not -9999.0 and datatype was > 5 (i.e. is a float).')
            rewrite_array = True
            new_ndv = True

    if set_ndv_below_value is not None:
        rewrite_array = True
        new_ndv = True
        old_ndv = ndv
        if data_type == 1:
            if ndv != 255:
                ndv = 255
        elif data_type < 6:
            if ndv != 9999:  # NOTE INT
                ndv = 9999
        else:
            if ndv != -9999.0:
                ndv = -9999.0

    if verbose:
        L.info('output data_type: ' + str(data_type) + ', output ndv: ' + str(ndv))

    ds.SetMetadataItem('last_processing_on', str(time.time()))

    ds = None
    if verbose:
        L.info('rewrite_array ' + str(rewrite_array))

    displacement_path = hb.temp('.tif', filename_start='displaced_by_make_path_global_pyramid_on_' + str(hb.file_root(input_path)), folder=os.path.split(input_path)[0], remove_at_exit=clean_temporary_files)
    temp_write_path = hb.temp('.tif', filename_start='temp_write_' + str(hb.file_root(input_path)), folder=os.path.split(input_path)[0], remove_at_exit=clean_temporary_files)

    if rewrite_array:
        L.info('make_path_spatially_clean triggered rewrite_array for ' + str(input_path))

        def sanitize_array(x):
            x = x.astype(hb.gdal_number_to_numpy_type[data_type])

            if new_ndv is True:
                x = np.where(np.isclose(x, old_ndv), ndv, x)
            if set_ndv_below_value is not None:
                x[x < set_ndv_below_value] = ndv
            return x

        hb.raster_calculator_af_flex(input_path, sanitize_array, temp_write_path, datatype=data_type, ndv=ndv, gtiff_creation_options=options)


    # Rename files to displace old input. This has to be done before external-file operations are completed.
    if output_path:
        if rewrite_array:
            hb.create_directories(os.path.split(output_path)[0])
            os.rename(temp_write_path, output_path)
            processed_path = output_path
        else:
            processed_path = input_path
    else:
        if os.path.exists(temp_write_path):
            os.rename(input_path, displacement_path)
            os.rename(temp_write_path, input_path)
        processed_path = input_path

    # Do metadata and compression tasks
    if make_overviews_external:
        ds = gdal.OpenEx(processed_path)
    else:
        ds = gdal.OpenEx(processed_path, gdal.GA_Update)

    # make_rat = False  # Arcaic form from ESRI, KEPT FOR REFERENCE ONLY
    # if make_rat:
    #     rat = gdal.RasterAttributeTable()
    #
    #     attr_dict = {0: 0, 1: 11, 2: 22}
    #     column_name = 'values'
    #
    #     rat.SetRowCount(len(attr_dict))
    #
    #     # create columns
    #     rat.CreateColumn('Value', gdal.GFT_Integer, gdal.GFU_MinMax)
    #     rat.CreateColumn(column_name, gdal.GFT_String, gdal.GFU_Name)
    #
    #     row_count = 0
    #     for key in sorted(attr_dict.keys()):
    #         rat.SetValueAsInt(row_count, 0, int(key))
    #         rat.SetValueAsString(row_count, 1, attr_dict[key])
    #         row_count += 1
    #
    #     ds.GetRasterBand(1).SetDefaultRAT(rat)

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    # gdal.SetConfigOption('USE_RRD', 'YES')  # FORCE EXTERNAL ,possibly as ovr? # USE_RRD is outdated (saves x.aux file). If you want external, just make sure you open the DS in read only.

    if overview_resample_method is None:
        if data_type <= 5:
            overview_resample_method = 'mode'
        else:
            overview_resample_method = 'average'

    #TODOO FEATURE IDEA, have multiple types of overviews, mean, min, max, nearest for extremely quick reference to statistics at different scales.
    if make_overviews or overwrite_overviews:
        if not os.path.exists(processed_path + '.ovr') or overwrite_overviews:
            if verbose:
                L.info('Starting to make overviews for ' + str(processed_path))

            band = ds.GetRasterBand(1)
            callback = hb.make_logger_callback("Creation of overviews in hb.spatial_utils.make_path_global_pyramid() %.1f%% complete %s for%s")

            ds.BuildOverviews(overview_resample_method, pyramid_compatible_overview_levels[arcseconds], callback, [input_path])  # Based on commonly used data shapes

    if calculate_stats or overwrite_stats:
        if not os.path.exists(processed_path + '.aux.xml') or overwrite_overviews:
            if verbose:
                L.info('Starting to calculate stats for ' + str(processed_path))
            ds.GetRasterBand(1).ComputeStatistics(False)  # False here means approx NOT okay
            ds.GetRasterBand(1).GetHistogram(approx_ok=0)
    ds = None
    return True

def make_dir_global_pyramid(input_dir, output_path=None, make_overviews=True, calculate_stats=True, clean_temporary_files=False,
                            resolution=None, raise_exception=False, make_overviews_external=True, verbose=True):
    """Throw exception if input_path is not pyramid-ready. This requires that the file be global, geographic projection, and with resolution
    that is a factor/multiple of arcdegrees.

    If output_path is specified, write to that location. Otherwise, make changes in-place but saving a temporary backup file of the input.

    # LEARNING POINT
    # ovr_band = src_ds.GetRasterBand(i).GetOverview(1)
    """
    L.critical('A bit outdated because doesnt use parallel approach found in make_paths_list_global_pyramid')
    for file_path in hb.list_filtered_paths_nonrecursively(input_dir, include_extensions='.tif'):
        hb.make_path_global_pyramid(file_path, output_path=output_path, make_overviews=make_overviews, calculate_stats=calculate_stats, clean_temporary_files=clean_temporary_files,
                                    raise_exception=raise_exception, make_overviews_external=make_overviews_external, verbose=verbose)


def make_path_spatially_clean(input_path,
                              output_path=None,
                              make_overviews=True,
                              overwrite_overviews=False,
                              calculate_stats=True,
                              overwrite_stats=False,
                              clean_temporary_files=False,
                              resolution=None,
                              raise_exception=False,
                              make_overviews_external=True,
                              set_ndv_below_value=None,
                              compression_method='deflate',
                              verbose=True):
    L.critical('DEPRECATED because hasnt been updated with newest things from make_path_global_pyramid.')

    """Similar to make_path_global_pyramid, except doesnt change anything that would alter the data.
    Specifically, it only changes (optionally) compression, overviews, and NDV (based on observed data_type."""
    ds = gdal.OpenEx(input_path, gdal.GA_Update)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    output_geotransform = ds.GetGeoTransform()
    # TODO This is outdated compared to advances made in make_path_global_pyramid.
    md = ds.GetMetadata()
    image_structure = ds.GetMetadata('IMAGE_STRUCTURE')
    compression = image_structure.get('COMPRESSION', None)

    # Consider operations that may need rewriting the underlying data
    rewrite_array = False

    # Check if compressed (pyramidal file standards require compression)
    if str(compression).lower() != compression_method.lower():
        rewrite_array = True

    L.info('Running make_path_spatially_clean on ' + str(input_path))
    data_type = ds.GetRasterBand(1).DataType
    ndv = ds.GetRasterBand(1).GetNoDataValue()
    ds.SetMetadataItem('last_processing_on', str(time.time()))
    # ds = None

    if data_type >= 6:
        options = (
            'BIGTIFF=YES',
            'COMPRESS=' + str(compression_method).upper(),
            'BLOCKXSIZE=256',
            'BLOCKYSIZE=256',
            'TILED=YES',
            # 'PREDICTOR=3', #
        )
    else:
        options = hb.DEFAULT_GTIFF_CREATION_OPTIONS


    new_ndv = False
    below_ndv = False
    if verbose:
        L.info('input data_type: ' + str(data_type) + ', input ndv: ' + str(ndv))
    if data_type == 1:
        if ndv != 255:
            old_ndv = ndv
            ndv = 255
            L.critical('rewrite_array triggered because ndv was not 255 and datatype was 1.')
            rewrite_array = True
            new_ndv = True
    elif data_type < 6:
        if ndv != 9999:  # NOTE INT
            old_ndv = ndv
            ndv = 9999
            L.critical('rewrite_array triggered because ndv was not 9999 and datatype was of int type.')
            rewrite_array = True
            new_ndv = True
    else:
        if ndv != -9999.0:
            old_ndv = ndv
            ndv = -9999.0
            L.critical('rewrite_array triggered because ndv was not -9999.0 and datatype was > 5 (i.e. is a float).')
            rewrite_array = True
            new_ndv = True

    if set_ndv_below_value is not None:
        if data_type == 1:
            if ndv != 255:
                ndv = 255
                rewrite_array = True
                new_ndv = True
        elif data_type < 6:
            if ndv != 9999:  # NOTE INT
                ndv = 9999
                rewrite_array = True
                new_ndv = True
        else:
            if ndv != -9999.0:
                ndv = -9999.0
                rewrite_array = True
                new_ndv = True

    L.info('output data_type: ' + str(data_type) + ', output ndv: ' + str(ndv))



    ds = None

    L.info('rewrite_array ' + str(rewrite_array))
    temp_write_path = hb.temp('.tif', filename_start='temp_write_' + str(hb.file_root(input_path)), remove_at_exit=clean_temporary_files)
    displacement_path = hb.temp('.tif', filename_start='displaced_by_make_path_global_pyramid_on_' + str(hb.file_root(input_path)), remove_at_exit=clean_temporary_files)

    if rewrite_array:

        input_ds = gdal.OpenEx(input_path)

        driver = gdal.GetDriverByName('GTiff')
        new_ds = driver.Create(temp_write_path, n_c, n_r, 1, data_type, options=options)
        new_ds.SetGeoTransform(output_geotransform)
        new_ds.SetProjection(hb.wgs_84_wkt)
        new_ds.GetRasterBand(1).SetNoDataValue(ndv)
        read_callback = hb.make_logger_callback("ReadAsArray percent complete:")
        write_callback = hb.make_logger_callback("WriteArray percent complete:")
        array = input_ds.ReadAsArray(callback=read_callback, callback_data=[output_path]).astype(hb.gdal_number_to_numpy_type[data_type])

        if new_ndv and  set_ndv_below_value is None:
            np.where(np.isclose(array, old_ndv), ndv, array)
            # array[array == old_ndv] = ndv

        if set_ndv_below_value is not None:
            # array = np.where(array < set_ndv_below_value, ndv, array)
            array[array < set_ndv_below_value] = ndv


        new_ds.GetRasterBand(1).WriteArray(array, callback=write_callback, callback_data=[output_path])

        input_ds = None
        new_ds = None

        # Rename files to displace old input. This has to be done before external-file operations are completed.
        os.rename(input_path, displacement_path)
        os.rename(temp_write_path, input_path)
    # Rename files to displace old input. This has to be done before external-file operations are completed.
    if output_path:
        hb.create_directories(os.path.split(output_path)[0])
        os.rename(temp_write_path, output_path)
        processed_path = output_path
    else:
        if os.path.exists(temp_write_path):
            os.rename(input_path, displacement_path)
            os.rename(temp_write_path, input_path)
        processed_path = input_path

    # Do metadata and compression tasks
    if make_overviews_external:
        ds = gdal.OpenEx(input_path)
    else:
        ds = gdal.OpenEx(input_path, gdal.GA_Update)

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    # gdal.SetConfigOption('USE_RRD', 'YES')  # FORCE EXTERNAL ,possibly as ovr? # USE_RRD is outdated (saves x.aux file). If you want external, just make sure you open the DS in read only.

    if make_overviews or overwrite_overviews:
        if not os.path.exists(processed_path + '.ovr') or overwrite_overviews:
            if verbose:
                L.info('Starting to make overviews for ' + str(processed_path))
            ds.BuildOverviews('nearest', [2, 4, 8, 16, 32])  # Based on commonly used data shapes

    if calculate_stats or overwrite_stats:
        if not os.path.exists(processed_path + '.aux.xml') or overwrite_overviews:
            if verbose:
                L.info('Starting to calculate stats for ' + str(processed_path))
            ds.GetRasterBand(1).ComputeStatistics(False)  # False here means approx NOT okay
            ds.GetRasterBand(1).GetHistogram(approx_ok=0)


    ds = None
    return True

def add_statistics_to_raster(input_path, verbose=False):
    try:
        ds = gdal.OpenEx(input_path)
    except Exception as e:
        raise NameError('Missing path: ' + str(input_path) + ' raised exception ' + str(e))
    if verbose:
        L.info('Starting to calculate stats for ' + str(processed_path))
    ds.GetRasterBand(1).ComputeStatistics(False)  # False here means approx NOT okay
    ds.GetRasterBand(1).GetHistogram(approx_ok=0)

    ds = None

def compress_path(input_path, clean_temporary_files=False):
    hb.make_path_spatially_clean(input_path, make_overviews=False, calculate_stats=False, clean_temporary_files=clean_temporary_files)

def assert_paths_same_pyramid(path_1, path_2, raise_exception=False, surpress_output=False):


    bool_1 = hb.is_path_global_pyramid(path_1)
    bool_2 = hb.is_path_global_pyramid(path_2)
    bool_3 = hb.is_path_same_geotransform(path_1, path_2, raise_exception=raise_exception, surpress_output=surpress_output)

    results = [bool_1, bool_2, bool_3]
    if all(results):
        return True
    else:
        result_string = '\nPaths not pyramidal:\n' + str(path_1) + '\n' + str(path_2)
        if raise_exception:
            if raise_exception:
                raise NameError(result_string)
            else:
                L.critical(result_string)
                return False


def set_geotransform_to_tuple(input_path, desired_geotransform):
    """
    FROM CONFIG:
    geotransform_global_5m = (-180.0, 0.08333333333333333, 0.0, 90.0, 0.0, -0.08333333333333333)  # NOTE, the 0.08333333333333333 is defined very precisely as the answer a 64 bit compiled python gives from the answer 1/12 (i.e. 5 arc minutes)
    geotransform_global_30s = (-180.0, 0.008333333333333333, 0.0, 90.0, 0.0, -0.008333333333333333)  # NOTE, the 0.008333333333333333 is defined very precisely as the answer a 64 bit compiled python gives from the answer 1/120 (i.e. 30 arc seconds) Note that this has 1 more digit than 1/12 due to how floating points are stored in computers via exponents.
    geotransform_global_10s = (-180.0, 0.002777777777777778, 0.0, 90.0, 0.0, -0.002777777777777778)  # NOTE, the 0.002777777777777778 is defined very precisely
    """
    ds = gdal.OpenEx(input_path, gdal.GA_Update)
    gt = ds.GetGeoTransform()
    ds.SetGeoTransform(desired_geotransform)
    gt = ds.GetGeoTransform()
    ds = None

def change_array_datatype_and_ndv(input_path, output_path, data_type, input_ndv=None, output_ndv=None):
    output_data_type_numpy = hb.default_no_data_values_by_gdal_number_in_numpy_types[data_type]
    if input_ndv is None:
        input_ndv = hb.get_ndv_from_path(input_path)
    if output_ndv is None:
        output_ndv = hb.default_no_data_values_by_gdal_number_in_numpy_types[data_type]
    output_ndv = np.float64(output_ndv)
    hb.raster_calculator_af_flex(input_path, lambda x: np.where(x == input_ndv, output_ndv, x).astype(output_data_type_numpy), output_path, datatype=data_type, ndv=output_ndv)


def set_projection_to_wkt(input_path, desired_projection_wkt):
    ds = gdal.OpenEx(input_path, gdal.GA_Update)
    ds.SetProjection(desired_projection_wkt)
    ds = None

def load_geotiff(input_path, raise_all_exceptions=False):
    callback = hb.make_logger_callback("load_geotiff %.1f%% complete %s")
    ds = gdal.OpenEx(input_path)
    if ds is None:
        raise NameError("Cannot use gdal.OpenEx on " + str(input_path) + ' in load_geotiff. Probably the file doesnt exist.')

    try:
        a = ds.ReadAsArray(callback=callback, callback_data=[input_path])
    except:
        L.critical('Failed to ReadAsArray in load_geotiff for ' + str(input_path))

    return a

def load_geotiff_chunk_by_cr_size(input_path, cr_size, stride_rate=None, datatype=None, output_path=None, ndv=None, raise_all_exceptions=False):
    """Convenience function to load a chunk of an array given explicit row and column info."""

    ds = gdal.OpenEx(input_path)

    if ds is None:
        mod_path = os.path.split(input_path)[0].replace('/', '\\')
        raise NameError("Cannot find " + str(input_path) + ' in load_geotiff_chunk_by_cr_size.')
        # raise NameError("Cannot find " + str(input_path) + " in dir:\n\tFile \"" + mod_path + "\\\", line 1")
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    c = int(cr_size[0])
    r = int(cr_size[1])
    c_size = int(cr_size[2])
    r_size = int(cr_size[3])

    if stride_rate:
        if stride_rate > 1:
            L.debug('load_geotiff_chunk_by_cr_size with stride rate ' + str(stride_rate) + ' on ' + input_path)

    if stride_rate is None:
        stride_rate = 1


    if not 0 <= r <= n_r:
        raise NameError('r given to load_geotiff_chunk_by_cr_size didnt fit. r, n_r: ' + str(r) + ' ' + str(n_r) + ' for path ' + input_path)

    if not 0 <= c <= n_c:
        raise NameError('c given to load_geotiff_chunk_by_cr_size didnt fit. c, n_c: ' + str(c) + ' ' + str(n_c) + ' for path ' + input_path)

    if not 0 <= r + r_size / stride_rate <= n_r:
        raise NameError('r_size given to load_geotiff_chunk_by_cr_size didnt fit. r_size, n_r: ' + str(r_size) + ' ' + str(n_r) + ' for path ' + input_path)

    if not 0 <= c + c_size / stride_rate <= n_c:
        raise NameError('c given to load_geotiff_chunk_by_cr_size didnt fit. c, n_c: ' + str(c_size) + ' ' + str(n_c) + ' for path ' + input_path)

    # callback = hb.make_logger_callback("load_geotiff_chunk_by_cr_size %.1f%% complete %s")
    # callback = hb.invoke_timed_callback("load_geotiff_chunk_by_cr_size %.1f%% complete %s")
    # callback = hb.make_simple_gdal_callback("load_geotiff_chunk_by_cr_size %.1f%% complete %s")
    # # hb.load_gdal_ds_as_strided_array()
    # ds = gdal.Open(input_path)
    # band = ds.GetRasterBand(1)
    # array = band.ReadAsArray(0, 0, ds.RasterXSize, ds.RasterYSize, buf_xsize=int(ds.RasterXSize / stride_rate), buf_ysize=int(ds.RasterYSize / stride_rate))
    #
    # band = None
    # gdal.Dataset.__swig_destroy__(ds)
    # ds = None
    # return array

    callback = hb.make_logger_callback("load_geotiff_chunk_by_cr_size %.1f%% complete %s")
    buf_xsize = int(c_size / stride_rate)
    buf_ysize = int(r_size / stride_rate)
    if raise_all_exceptions:
        a = ds.ReadAsArray(c, r, c_size, r_size, buf_xsize=buf_xsize,
                           buf_ysize=buf_ysize, buf_type=datatype, callback=callback, callback_data=[input_path])
    else:
        fail = 1
        if fail:
            a = ds.ReadAsArray(c, r, c_size, r_size, buf_xsize=buf_xsize,
                               buf_ysize=buf_ysize, buf_type=datatype, callback=callback, callback_data=[input_path])
        else:
            try:
                a = ds.ReadAsArray(c, r, c_size, r_size, buf_xsize=buf_xsize,
                                   buf_ysize=buf_ysize, buf_type=datatype, callback=callback, callback_data=[input_path])
            except:
                L.critical('Failed to ReadAsArray in load_geotiff_chunk_by_cr_size for ' + str(input_path))

    if output_path is not None:

        if datatype is not None:
            data_type = datatype
        # else:
        #     data_type = hb.get_datatype_from_uri(input_path)

        if not isinstance(datatype, int):
            try:
                data_type = hb.get_datatype_from_uri(input_path)
            except:
                data_type = hb.numpy_type_to_gdal_number[hb.get_datatype_from_uri(input_path)]

        src_ndv = hb.get_ndv_from_path(input_path)
        if ndv is None:
            ndv = hb.get_ndv_from_path(input_path)

        if ndv != src_ndv:
            a = np.where(np.isclose(a, src_ndv), ndv, a)

        gt = list(hb.get_geotransform_uri(input_path))
        lat, lon = hb.rc_path_to_latlon(r, c, input_path)
        gt[0] = lon
        gt[3] = lat
        geotransform_override = gt
        projection_override = hb.get_dataset_projection_wkt_uri(input_path)
        n_cols_override, n_rows_override = (c_size, r_size)

        if output_path is True:
            output_path = hb.temp('.tif')

        hb.save_array_as_geotiff(a, output_path, data_type=data_type, ndv=ndv, geotransform_override=geotransform_override,
                                 projection_override=projection_override, n_cols_override=n_cols_override, n_rows_override=n_rows_override)

    return a

def load_geotiff_chunk_by_bb(input_path, bb, inclusion_behavior='centroid', stride_rate=None, datatype=None, output_path=None, ndv=None, raise_all_exceptions=False):
    """Load a geotiff chunk as a numpy array from input_path. Requires that input_path be pyramid_ready. If datatype given,
    returns the numpy array by GDAL number, defaulting to the type the data was saved as.

    If BB is none, loads the whole array.

    Inclusion_behavior determines how cells that are only partially within the bb are considered. Default is centroid, but can be exclusive or exclusive.

    inclusion_behavior = one of 'centroid', 'inclusive', 'exclusive'

    if given output_path will make it write there (potentially EXTREMELY computaitonally slow)
    if output_path is True and not a string, will save to a atemp file.
     """
    c, r, c_size, r_size = hb.bb_path_to_cr_size(input_path, bb, inclusion_behavior=inclusion_behavior)
    L.debug('bb_path_to_cr_widthheight generated', c, r, c_size, r_size)

    a = hb.load_geotiff_chunk_by_cr_size(input_path, (c, r, c_size, r_size), stride_rate=stride_rate, datatype=datatype, raise_all_exceptions=raise_all_exceptions)

    if output_path is not None:

        data_type = hb.get_datatype_from_uri(input_path)

        src_ndv = hb.get_ndv_from_path(input_path)
        if ndv is None:
            ndv = hb.get_ndv_from_path(input_path)

        if ndv != src_ndv:
            a = np.where(np.isclose(a, src_ndv), ndv, a)

        gt = list(hb.get_geotransform_uri(input_path))
        gt[0] = bb[0]
        gt[3] = bb[3]
        geotransform_override = gt
        projection_override = hb.get_dataset_projection_wkt_uri(input_path)
        n_cols_override, n_rows_override = (c_size, r_size)

        if output_path is True:
            output_path = hb.temp('.tif')

        hb.save_array_as_geotiff(a, output_path, data_type=data_type, ndv=ndv, geotransform_override=geotransform_override,
                                 projection_override=projection_override, n_cols_override=n_cols_override, n_rows_override=n_rows_override)

    return a

def bb_path_to_cr_size(input_path, bb, inclusion_behavior='centroid'):
    """input path of larger file from which bb cuts."""
    # BB must be in lat-lon units (not projected units yet) in xmin, ymin, xmax, ymax order
    # Useful for getting gdal-type cr_widthheight from a subset of a raster via it's bb from path.
    # Note that gdal Open uses col, row, n_cols, n_row notation. This function converts lat lon bb to rc in this order based on the proportional size of the input_path.

    if not os.path.exists(input_path):
        L.warning('bb_path_to_cr_size unable to open ' + str(input_path))
    ds = gdal.OpenEx(input_path)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    gt = hb.get_geotransform_uri(input_path)
    lower_lat = bb[1]
    upper_lat = bb[3]
    left_lon = bb[0]
    right_lon = bb[2]

    if inclusion_behavior == 'inclusive':
        r, c = hb.latlon_path_to_rc(upper_lat, left_lon, input_path, r_shift_direction='up', c_shift_direction='left')
        r_right, c_right = hb.latlon_path_to_rc(lower_lat, right_lon, input_path, r_shift_direction='down', c_shift_direction='right')
    elif inclusion_behavior == 'exclusive':
        r, c = hb.latlon_path_to_rc(upper_lat, left_lon, input_path, r_shift_direction='down', c_shift_direction='right')
        r_right, c_right = hb.latlon_path_to_rc(lower_lat, right_lon, input_path, r_shift_direction='up', c_shift_direction='left')
    else:
        r, c = hb.latlon_path_to_rc(upper_lat, left_lon, input_path, r_shift_direction='centered', c_shift_direction='centered')
        r_right, c_right = hb.latlon_path_to_rc(lower_lat, right_lon, input_path, r_shift_direction='centered', c_shift_direction='centered')
    r_size = r_right - r
    c_size = c_right - c

    if c_size == 0 or r_size == 0:
        L.debug('Inputs given result in zero size: ' + str(c) + ' ' + str(r) + ' ' + str(c_size) + ' ' + str(r_size))

    return round(c), round(r), round(c_size), round(r_size)


def latlon_path_to_rc(lat, lon, input_path, r_shift_direction='centered', c_shift_direction='centered'):
    """Calculate the row and column index from a raster at input_path for a given lat, lon value.
    Because latlon is continuous and rc is integer, specify the behavior for rounding. Default is centered, but can shift in any direction
    for applications that need precision (e.g. clipping country borders and requiring exclusivity.
    """

    ds = gdal.OpenEx(input_path)
    n_c, n_r = Decimal(ds.RasterXSize), Decimal(ds.RasterYSize)
    gt = ds.GetGeoTransform()
    ulx, xres, _, uly, _, yres = Decimal(gt[0]), Decimal(gt[1]), Decimal(gt[2]), Decimal(gt[3]), Decimal(gt[4]), Decimal(gt[5])

    lat = Decimal(lat)
    lon = Decimal(lon)
    gt_xmin_lon = ulx
    gt_ymin_lat = uly + yres * n_r
    gt_xmax_lon = ulx + xres * n_c
    gt_ymax_lat = uly
    prop_r = (gt_ymax_lat - lat) / (gt_ymax_lat - gt_ymin_lat)
    # prop_r = (lat - gt_ymin_lat) / (gt_ymax_lat - gt_ymin_lat)
    prop_c = (lon - gt_xmin_lon) / (gt_xmax_lon - gt_xmin_lon)
    r = prop_r * n_r
    c = prop_c * n_c

    initial_r = r
    initial_c = c

    if r_shift_direction == 'up':
        r = math.floor(r)
    elif r_shift_direction == 'down':
        r = math.ceil(r)
    elif r_shift_direction == 'nearest':
        r = round(r)

    if c_shift_direction == 'left':
        c = math.floor(c)
    elif c_shift_direction == 'right':
        c = math.ceil(c)
    elif c_shift_direction == 'nearest':
        c = round(c)

    verbose = False
    if verbose:
        print ('latlon_path_to_rc generated: lat', lat, 'lon', lon, 'n_c', n_c, 'n_r', n_r, 'ulx', ulx, 'xres', xres, 'uly', uly, 'yres', yres, 'prop_r', prop_r, 'prop_c', prop_c, 'r', r, 'c', c)

    return r, c

def rc_path_to_latlon(r, c, input_path):
    ds = gdal.OpenEx(input_path)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    gt = ds.GetGeoTransform()

    ulx, xres, _, uly, _, yres = gt[0], gt[1], gt[2], gt[3], gt[4], gt[5]

    prop_r = r / n_r
    prop_c = c / n_c

    lat = uly - prop_r * (uly - (uly + yres * n_r))
    lon = ulx - prop_c * (ulx - (ulx + xres * n_c))

    # CAUTION: Recall that a geotransform is ul_LON, xres, 0 ul_LAT, 0, yres)
    return lat, lon

def generate_geotransform_of_chunk_from_cr_size_and_larger_path(cr_size, larger_raster_path):
    # gt = [0, 0, 0, 0, 0, 0]
    lat, lon = hb.rc_path_to_latlon(cr_size[1], cr_size[0], larger_raster_path)
    res = hb.get_cell_size_from_uri(larger_raster_path)
    return [lon, res, 0., lat, 0., -res]

def get_pyramid_compatible_bb_from_vector_and_resolution(input_vector, pyramid_resolution):
    """
    get a BB expanded outwards to include all of the input vector up to the nearest bounds of pyramid resolution

    :param input_vector: GPKG pointiing to the AOI or other vector needd to calculate inclusive coarse pyramid tiles.
    :param pyramid_resolution: in arcseconds
    :return: [r, c, r_size, c_size]
    """
    exact_bb = hb.get_bounding_box(input_vector)

    pyramid_resolution_degrees = hb.pyramid_compatible_resolutions[pyramid_resolution]

    bb = [0, 0, 0, 0]
    bb[0] = pyramid_resolution_degrees * float(math.floor(exact_bb[0] / pyramid_resolution_degrees))
    bb[1] = pyramid_resolution_degrees * float(math.floor(exact_bb[1] / pyramid_resolution_degrees))
    bb[2] = pyramid_resolution_degrees * float(math.ceil(exact_bb[2] / pyramid_resolution_degrees))
    bb[3] = pyramid_resolution_degrees * float(math.ceil(exact_bb[3] / pyramid_resolution_degrees))

    return bb

def is_path_same_geotransform(input_path, match_path, raise_exception=False, surpress_output=False):
    """Throw exception if input_path is not the same geotransform as the match path."""
    if not os.path.exists(input_path):
        result_string = 'Unable to find input path:\n' + str(input_path)
        if raise_exception:
            raise NameError(result_string)
        else:
            if not surpress_output:
                L.warning(result_string)
            return False

    if not os.path.exists(match_path):
        result_string = 'Unable to find match path:\n' + str(match_path)
        if raise_exception:
            raise NameError(result_string)
        else:
            if not surpress_output:
                L.warning(result_string)
            return False

    ds = gdal.OpenEx(input_path)
    try:
        gt = ds.GetGeoTransform()
    except:
        gt = None

    ds_match = gdal.OpenEx(match_path)
    gt_match = ds_match.GetGeoTransform()

    if not gt == gt_match:
        result_string = 'Input path did not have the same geotransform as match path:\n' + str(input_path) + '\n' + str(gt) + '\n' + str(match_path) + '\n' + str(gt_match)
        if raise_exception:
            raise NameError(result_string)
        else:
            if not surpress_output:
                L.warning(result_string)
            return False


    # Passed all the tests
    return True

def convert_ndv_to_alpha_band(input_path, output_path, ndv_replacement_value=0):
    """Take a 1 band geotiff with an ndv value, extract the ndv value, replace it, then write the ndv value as an alpha band.

    Writes a 2 band geotiff to output path."""

    ds = gdal.OpenEx(input_path)
    band = ds.GetRasterBand(1)
    array = band.ReadAsArray()

    ndv = band.GetNoDataValue()
    data_type = band.DataType

    n_cols = array.shape[1]
    n_rows = array.shape[0]
    geotransform = hb.get_geotransform_path(input_path)
    projection = hb.get_dataset_projection_wkt_uri(input_path)

    # For later, make it inherit the right metadata with the following
    metadata = ds.GetMetadata('IMAGE_STRUCTURE')
    metadata = ds.GetMetadata()

    # For now, I just have it use the default gtiff options
    dst_options = hb.DEFAULT_GTIFF_CREATION_OPTIONS

    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(output_path, n_cols, n_rows, 2, data_type, dst_options)
    dst_ds.GetRasterBand(2).SetColorInterpretation(gdal.GCI_AlphaBand)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(projection)

    # dst_ds.GetRasterBand(1).SetNoDataValue(ndv)

    alpha_array = np.where(array == ndv, 0, 255)

    array[array == ndv] = ndv_replacement_value
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds.GetRasterBand(2).WriteArray(alpha_array)

    dst_ds = None
    ds = None

    # From gdal_edit.py script.
    # ds.GetRasterBand(band).SetColorInterpretation(colorinterp[band])
    # gdal.GCI_AlphaBand

def get_aspect_ratio_of_two_arrays(coarse_res_array, fine_res_array):
    # Test that map resolutions are workable multiples of each other
    # assert int(round(fine_res_array.shape[0] / coarse_res_array.shape[0])) == int(
    #     round(fine_res_array.shape[1] / coarse_res_array.shape[1]))
    aspect_ratio = int(round(fine_res_array.shape[0] / coarse_res_array.shape[0]))
    return aspect_ratio


def calc_proportion_of_coarse_res_with_valid_fine_res(coarse_res, fine_res):
    """Useful wehn allocating to border cells."""

    if not isinstance(coarse_res, np.ndarray):
        try:
            coarse_res = hb.as_array(coarse_res).astype(np.float64)
        except:
            raise NameError('Unable to load ' + str(coarse_res) + ' as array in calc_proportion_of_coarse_res_with_valid_fine_res.')

    if not isinstance(fine_res, np.ndarray):
        try:
            fine_res = hb.as_array(fine_res).astype(np.int64)
        except:
            raise NameError('Unable to load ' + str(fine_res) + ' as array in calc_proportion_of_coarse_res_with_valid_fine_res.')

    aspect_ratio = get_aspect_ratio_of_two_arrays(coarse_res, fine_res)

    #
    # coarse_res_proportion_array = np.zeros(coarse_res.shape).astype(np.float64)
    # fine_res_proportion_array = np.zeros(fine_res.shape).astype(np.float64)

    proportion_valid_fine_per_coarse_cell = hb.cython_calc_proportion_of_coarse_res_with_valid_fine_res(coarse_res.astype(np.float64), fine_res.astype(np.int64))

    return proportion_valid_fine_per_coarse_cell

def is_compressed(input_path):
    # Make flex?

    ds = gdal.OpenEx(input_path)
    md = ds.GetMetadata()
    image_structure = ds.GetMetadata('IMAGE_STRUCTURE')
    compression = image_structure.get('COMPRESSION', False)

    if compression:
        return True
    else:
        return False


def add_rows_or_cols_to_geotiff(input_path, r_above, r_below, c_left, c_right, output_path=None, fill_value=None, remove_temporary_files=False):
    # if output_path is None, assume overwriting
    input_ds = gdal.OpenEx(input_path)
    input_gt = input_ds.GetGeoTransform()
    input_projection = input_ds.GetProjection()
    datatype = hb.get_raster_info_hb(input_path)['datatype']

    callback = hb.make_simple_gdal_callback('Reading array')
    input_array = input_ds.ReadAsArray(callback=callback)
    output_gt = list(input_gt)
    output_gt = [input_gt[0] + c_left * input_gt[1], input_gt[1], 0.0, input_gt[3] + r_above * input_gt[1], 0.0, input_gt[5]]

    if fill_value is None:
        fill_value = input_ds.GetRasterBand(1).GetNoDataValue()

    n_rows = int(input_ds.RasterYSize + r_above + r_below)
    n_cols = int(input_ds.RasterXSize + c_left + c_right)

    input_ds = None # Close the dataset so that we can move or overwrite it.

    # If there is no output_path, assume that we are going to be doing the operation in-place. BUT, if remove_temporary_files
    # is not True, simply move the input file to temp as a backup.
    if output_path is None:
        temp_path = hb.temp('.tif', 'displaced_' + hb.file_root(input_path), remove_temporary_files)
        hb.rename_with_overwrite(input_path, temp_path)
        output_path = input_path
        input_path = temp_path

    driver = gdal.GetDriverByName('GTiff')

    local_gtiff_creation_options = list(hb.DEFAULT_GTIFF_CREATION_OPTIONS)
    local_gtiff_creation_options.extend(['COMPRESS=DEFLATE'])

    n_bands = 1

    output_raster = driver.Create(output_path, n_cols, n_rows, n_bands, datatype, options=local_gtiff_creation_options)
    output_raster.SetProjection(input_projection)
    output_raster.SetGeoTransform(output_gt)

    output_band = output_raster.GetRasterBand(1)

    output_band.SetNoDataValue(fill_value) # NOTE, this has to happen before WriteArray or it will assume filling with 0.
    output_band.WriteArray(input_array, c_left, r_above)
    output_raster.FlushCache()
    output_raster = None


def fill_to_match_extent(input_path, match_path, output_path=None, fill_value=None, remove_temporary_files=False):

    # gdal.Translate()

    ds = gdal.OpenEx(input_path)
    input_gt = ds.GetGeoTransform()

    match_ds = gdal.OpenEx(match_path)
    match_gt = match_ds.GetGeoTransform()

    c_left = -1 * (match_gt[0] - input_gt[0]) * match_gt[1]
    r_above = (match_gt[3] - input_gt[3]) / match_gt[1]

    c_right = match_ds.RasterXSize - (c_left + ds.RasterXSize)
    r_below = match_ds.RasterYSize - (r_above + ds.RasterYSize)

    n_cols = ds.RasterXSize + c_left + c_right
    n_rows = ds.RasterYSize + r_above + r_below

    ds = None
    match_ds = None

    hb.add_rows_or_cols_to_geotiff(input_path, r_above, r_below, c_left, c_right, output_path=output_path, fill_value=fill_value, remove_temporary_files=remove_temporary_files)



def fill_to_match_extent_using_warp(input_path, match_path, output_path=None, fill_value=None, remove_temporary_files=False):
    # Slower it seems than fill_to_match_extent.
    match_ds = gdal.OpenEx(match_path)
    match_gt = match_ds.GetGeoTransform()
    match_srs = match_ds.GetProjection()
    match_gdal_win = hb.get_raster_info_hb(match_path)['gdal_win']

    if output_path is None:
        output_path = hb.temp('.tif', 'filled', False)

    width = match_ds.RasterXSize
    height = match_ds.RasterYSize
    callback = hb.make_logger_callback(
        "fill_to_match_extent %.1f%% complete %s")
    gdal.Warp(output_path, input_path, width=width, height=height, outputBounds=match_gdal_win,
              callback=callback, callback_data=[output_path])

def snap_bb_points_to_outer_pyramid(input_bb, pyramidal_raster_path):
    """
    Converts a BB to one that has points that preceisly correspond to the Pyramid definition given by Pyramidal_raster_path.
    :param input_bb:
    :param pyramidal_raster_path:
    :return:
    """
    # NOTE INTERESTING BEHAVIOR: exclusive works, centroid does not. it shifts everyone 1 to the right.
    # Is this a bahavior that happens with centroid and coords that precisely hit a pyramid cell edge?
    res = Decimal(determine_pyramid_resolution(pyramidal_raster_path))

    # Convert to decimal types
    input_bb = [Decimal(input_bb[0]), Decimal(input_bb[1]), Decimal(input_bb[2]), Decimal(input_bb[3])]

    snapped_bb = [Decimal(0.0), Decimal(0.0), Decimal(0.0), Decimal(0.0)]
    snapped_bb[0] = input_bb[0] - (Decimal(input_bb[0]) % res)
    snapped_bb[1] = input_bb[1] - (input_bb[1] % res)
    snapped_bb[2] = input_bb[2] + (res - input_bb[2] % res)
    snapped_bb[3] = input_bb[3] + (res - input_bb[3] % res)

    returned_bb = [float(i) for i in snapped_bb]
    return returned_bb


def write_geotiff_as_netcdf(input_path, output_path):

    return 1

def load_netcdf_as_array(input_path):
    nc_fid = netCDF4.Dataset(input_path, 'r')  # Dataset is the class behavior to open the file
    """w (write mode) to create a new file, use clobber=True to over-write and existing one
    r (read mode) to open an existing file read-only
    r+ (append mode) to open an existing file and change its contents"""
    # and create an instance of the ncCDF4 class
    nc_fid.close()

def create_netcdf_at_path(output_path):
    f = netCDF4.Dataset(output_path, 'w')

    """The first dimension is called time with unlimited size (i.e. variable values may be 
    appended along the this dimension). Unlimited size dimensions must be declared before (“to the left of”) other dimensions. 
    We usually use only a single unlimited size dimension that is used for time."""
    f.createDimension('time', None)
    f.createDimension('z', 3)
    f.createDimension('y', 4)
    f.createDimension('x', 5)

    lats = f.createVariable('lat', float, ('y',), zlib=True)
    lons = f.createVariable('lon', float, ('x',), zlib=True)
    orography = f.createVariable('orog', float, ('y', 'x'), zlib=True, least_significant_digit=1, fill_value=0)

    # create latitude and longitude 1D arrays
    lat_out = [60, 65, 70, 75]
    lon_out = [30, 60, 90, 120, 150]
    # Create field values for orography
    data_out = np.arange(4 * 5)  # 1d array but with dimension x*y
    data_out.shape = (4, 5)  # reshape to 2d array
    orography[:] = data_out

    """lats is a netCDF variable; a lot more than a simple numpy array while lats[:] allows you to access 
    the latitudes values stored in the lats netCDF variable. lats[:] is a numpy array."""

    lats[:] = lat_out
    lons[:] = lon_out
    # close file to write on disk
    f.close()

def show_netcdf(input_path):
    import netCDF4
    import numpy as np
    import scipy
    import scipy.cluster.vq
    # from scipy.cluster.vq import *
    from matplotlib import colors as c
    import matplotlib.pyplot as plt

    np.random.seed((1000, 2000))

    f = netCDF4.Dataset(input_path, 'r')
    lats = f.variables['latitude'][:]
    lons = f.variables['longitude'][:]
    pw = f.variables['precipitable_water'][0, :, :]

    f.close()
    # Flatten image to get line of values
    flatraster = pw.flatten()
    flatraster.mask = False
    flatraster = flatraster.data

    # In first subplot add original image
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    # Create figure to receive results
    fig.set_figheight(20)
    fig.set_figwidth(15)

    fig.suptitle('K-Means Clustering')
    ax1.axis('off')
    ax1.set_title('Original Image\nMonthly Average Precipitable Water\n over Ice-Free Oceans (kg m-2)')
    original = ax1.imshow(pw, cmap='rainbow', interpolation='nearest', aspect='auto', origin='lower')
    plt.colorbar(original, cmap='rainbow', ax=ax1, orientation='vertical')
    # In remaining subplots add k-means clustered images
    # Define colormap
    list_colors = ['blue', 'orange', 'green', 'magenta', 'cyan', 'gray', 'red', 'yellow']

    print ("Calculate k-means with 6 clusters.")

    # This scipy code classifies k-mean, code has same length as flattened
    # raster and defines which cluster the value corresponds to
    centroids, variance = scipy.cluster.vq.kmeans(flatraster.astype(float), 6)
    code, distance = scipy.cluster.vq.vq(flatraster, centroids)

    # Since code contains the clustered values, reshape into SAR dimensions
    codeim = code.reshape(pw.shape[0], pw.shape[1])

    # Plot the subplot with 4th k-means
    ax2.axis('off')
    xlabel = '6 clusters'
    ax2.set_title(xlabel)
    bounds = range(0, 6)
    cmap = c.ListedColormap(list_colors[0:6])
    kmp = ax2.imshow(codeim, interpolation='nearest', aspect='auto', cmap=cmap, origin='lower')
    plt.colorbar(kmp, cmap=cmap, ticks=bounds, ax=ax2, orientation='vertical')

    #####################################

    thresholded = np.zeros(codeim.shape)
    thresholded[codeim == 3] = 1
    thresholded[codeim == 5] = 2

    # Plot only values == 5
    ax3.axis('off')
    xlabel = 'Keep the fifth cluster only'
    ax3.set_title(xlabel)
    bounds = range(0, 2)
    cmap = c.ListedColormap(['white', 'green', 'cyan'])
    kmp = ax3.imshow(thresholded, interpolation='nearest', aspect='auto', cmap=cmap, origin='lower')
    plt.colorbar(kmp, cmap=cmap, ticks=bounds, ax=ax3, orientation='vertical')

    plt.show()


def compress_netcdf(input_path, output_path):


    src = nc.Dataset(input_path)
    trg = nc.Dataset(output_path, mode='w')

    # Create the dimensions of the file
    for name, dim in src.dimensions.items():
        trg.createDimension(name, len(dim) if not dim.isunlimited() else None)

    # Copy the global attributes
    trg.setncatts({a: src.getncattr(a) for a in src.ncattrs()})

    # Create the variables in the file
    for name, var in src.variables.items():
        trg.createVariable(name, var.dtype, var.dimensions, zlib=True)

        # Copy the variable attributes
        trg.variables[name].setncatts({a: var.getncattr(a) for a in var.ncattrs()})

        # Copy the variables values (as 'f4' eventually)
        trg.variables[name][:] = src.variables[name][:]

    # Save the file
    trg.close()
    src.close()

def combine_earthstat_tifs_to_nc(tif_paths, nc_path):
    # get Dims
    z = len(tif_paths)
    size_check = list(set([hb.get_shape_from_dataset_path(path) for path in tif_paths]))

    if len(size_check) < 1:
        raise NameError('Shapes given as a list to combine_tifs_to_nc led to no shape.')
    elif len(size_check) > 1:
        raise NameError('Shapes given as a list to combine_tifs_to_nc didnt all have the same shape.')
    else:
        pass

    y = size_check[0][0]
    x = size_check[0][1]

    match = nc.Dataset(r"C:\OneDrive\Projects\base_data\luh2\raw_data\RCP26_SSP1\multiple-states_input4MIPs_landState_ScenarioMIP_UofMD-IMAGE-ssp126-2-1-f_gn_2015-2100.nc")


    # y = match.variables['primf'].current_shape


    target_nc = nc.Dataset(nc_path, mode='w', format='NETCDF4')
    target_nc.description = 'Description is here.'

    # copy Global attributes from original file
    for att in match.ncattrs():
        setattr(target_nc, att, getattr(match, att))

    # Get metadata from known source

    hb.pp(match)
    hb.pp(match['primf'])

    target_nc.createDimension('y', y)
    target_nc.createDimension('x', x)

    lon_var = target_nc.createVariable('lon', 'f4', ('x'))
    lat_var = target_nc.createVariable('lat', 'f4', ('y'))
    # x_var = target_nc.createVariable('x', 'f4', ('x'))
    # y_var = target_nc.createVariable('y', 'f4', ('y'))
    primf_var = target_nc.createVariable('primf', 'f4', ('y', 'x'))

    # for var in match.variables:
    # for var in ['bounds']:
    for var in ['lat', 'lon', 'primf']:
        hb.pp(match.variables[var].ncattrs())
        for att in match.variables[var].ncattrs():
            setattr(target_nc.variables[var], att, getattr(match.variables[var], att))
    lon_var[:] = match.variables['lon'][:]
    lat_var[:] = match.variables['lat'][:]
    primf_var[:] = match.variables['primf'][:]
    # x_var[:] = match.variables['x'][:]
    # y_var[:] = match.variables['y'][:]

    target_nc.Conventions = 'CF-1.6'



    target_nc.extent = hb.global_bounding_box
    target_nc.close()


def combine_earthstat_tifs_to_nc_new(tif_paths, nc_path):
    # get Dims
    z = len(tif_paths)
    size_check = list(set([hb.get_shape_from_dataset_path(path) for path in tif_paths]))

    if len(size_check) < 1:
        raise NameError('Shapes given as a list to combine_tifs_to_nc led to no shape.')
    elif len(size_check) > 1:
        raise NameError('Shapes given as a list to combine_tifs_to_nc didnt all have the same shape.')
    else:
        pass
    y = size_check[0][0]
    x = size_check[0][1]

    target_nc = nc.Dataset(nc_path, mode='w')
    # target_nc.createDimension('time', z)
    # target_nc.createDimension('esa_lulc_class', z)
    target_nc.createDimension('lon', y)
    target_nc.createDimension('lat', x)

    # time = target_nc.createVariable('time', float, ('time',), zlib=True, fill_value=-9999)
    lats = target_nc.createVariable('lat', float, ('lat',), zlib=False, fill_value=-9999.)
    lons = target_nc.createVariable('lon', float, ('lon',), zlib=False, fill_value=-9999.)

    y_res = 180.0 / y
    x_res = 360.0 / x

    lats[:] = np.arange(-180., 180., x_res)
    lons[:] = np.arange(-90., 90., y_res)

    lats[:] = np.arange(-180. + x_res / 2., 180. + x_res / 2., x_res)
    lons[:] = np.arange(-90. + y_res / 2., 90. + y_res / 2., y_res)

    for c, path in enumerate(tif_paths):
        crop_name = os.path.split(path)[1].split('_')[0]
        var = target_nc.createVariable(crop_name, float, ('lon', 'lat'), zlib=True, fill_value=-9999.0, chunksizes=(43, 21))
        ds = gdal.OpenEx(path)
        current_array = ds.ReadAsArray()
        var[:] = np.flipud(current_array)
        # var[c, :] = current_array
    #
    # close file to write on disk
    target_nc.close()

def read_earthstat_nc_slice(input_nc_path, crop_name):
    # START HERE, conclusion is that ::4 slicing is 10x faster in gdal but chunk slicing in a square is 2x faster in nc.
    start = time.time()
    ds = nc.Dataset(input_nc_path)

    start = time.time()
    ds = gdal.OpenEx(r"C:\OneDrive\Projects\base_data\crops\earthstat\crop_production\barley_HarvAreaYield_Geotiff\barley_HarvestedAreaFraction.tif")

def prune_nc_by_vars_list(input_path, output_path, vars_to_include):

    # HACKish, but basically all the spatial reference stuff comes from input file, with the axes named canonically as follows
    vars_to_include += ['time', 'lat', 'lon']

    with netCDF4.Dataset(input_path) as src, netCDF4.Dataset(output_path, "w") as dst:
        # copy global attributes all at once via dictionary
        L.info('Setting global nc attributes: ' +str(src.__dict__))
        dst.setncatts(src.__dict__)
        # copy dimensions
        for name, dimension in src.dimensions.items():
            L.info('Creating dimensions ' + str(name))
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
        # copy all file data except for the excluded
        for name, variable in src.variables.items():
            if name in vars_to_include:
                x = dst.createVariable(name, variable.datatype, variable.dimensions, zlib=True)
                # copy variable attributes all at once via dictionary

                L.info('Setting variable nc attributes for ' + str(name) + ': ' + str(src[name].__dict__))
                dst[name].setncatts(src[name].__dict__)


                dst[name][:] = src[name][:]

def generate_nc_from_attributes(output_path):

    dsout = nc.Dataset(output_path, 'w', clobber=True)

    rows = 2180
    cols = 4320
    lats = np.linspace(-90.0, 90.0, cols)
    lons = np.linspace(-180.0, 180.0, rows)

    time = dsout.createDimension('time', 0)

    lat = dsout.createDimension('lat', cols)
    lat = dsout.createVariable('lat', 'f4', ('lat',), zlib=True)
    lat.standard_name = 'latitude'
    lat.units = 'degrees_north'
    lat.axis = "Y"
    lat[:] = lats

    lon = dsout.createDimension('lon', rows)
    lon = dsout.createVariable('lon', 'f4', ('lon',), zlib=True)
    lon.standard_name = 'longitude'
    lon.units = 'degrees_east'
    lon.axis = "X"
    lon[:] = lons

    times = dsout.createVariable('time', 'f4', ('time',), zlib=True)
    times.standard_name = 'time'
    times.long_name = 'time'
    times.units = 'hours since 1970-01-01 00:00:00'
    times.calendar = 'gregorian'

    actual_variable = dsout.createVariable(
        'actual_variable_name',
        'f4',
        ('time', 'lat', 'lon'),
        zlib=True,
        complevel=4,
        # least_significant_digit=1,
        fill_value=-9999., chunksizes=(1, 432, 216)
    )


    actual_variable[:] = np.ones((1, rows, cols))
    actual_variable.standard_name = 'acc_precipitation_amount'
    actual_variable.units = 'mm'
    actual_variable.setncattr('grid_mapping', 'spatial_ref')

    crs = dsout.createVariable('spatial_ref', 'i4')
    crs.spatial_ref = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'

def dask_compute(input_paths, op, output_path):
    from dask.distributed import Client, LocalCluster, Lock

    if isinstance(input_paths, str):
        input_paths = [input_paths]

    if not isinstance(input_paths, list):
        raise NameError('dask_compute inputs must be a single path-string or a list of strings.')

    block_sizes = []
    for path in input_paths:
        if not hb.path_exists(path):
            raise NameError('dask_compute unable to find path: ' + str(path))
        block_sizes.append(hb.get_blocksize_from_path(path))

    # LEARNING POINT
    t_b = tuple([tuple(i) for i in block_sizes])

    if len(set(t_b)) > 1:
        critical_string = 'Paths given to dask_computer were not all saved in the same blocksize. This will have dramatic performance implications.'
        critical_string += '\n' + str(input_paths)
        critical_string += '\n' + str(block_sizes)
        L.critical(critical_string)

    with LocalCluster() as cluster, Client(cluster) as client:
    # with LocalCluster() as cluster, Client(cluster) as client:
    # with LocalCluster(n_workers=math.floor(multiprocessing.cpu_count() / 2), threads_per_worker=2, memory_limit=str(math.floor(64 / (multiprocessing.cpu_count() + 1))) + 'GB') as cluster, Client(cluster) as client:

        L.info('Starting Local Cluster at http://localhost:8787/status')

        xds_list = []
        for input_path in input_paths:
            # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
            # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
            xds = rioxarray.open_rasterio(input_path, chunks='auto', lock=False)
            xds_list.append(xds)

        delayed_computation = op(*xds_list)
        delayed_computation.rio.to_raster(output_path, tiled=True, compress='DEFLATE', lock=Lock("rio", client=client))  # NOTE!!! MUCH FASTER WITH THIS. I think it's because it coordinates with the read to start the next thing asap.



def zonal_statistics_dask(
    input_raster,
    zone_vector_path,
    zone_ids_raster_path=None,
    id_column_label=None,
    zones_raster_data_type=None,
    values_raster_data_type=None,
    zones_ndv=None,
    values_ndv=None,
    all_touched=None,
    assert_projections_same=True,
    unique_zone_ids=None,
    csv_output_path=None,
    vector_output_path=None,
    stats_to_retrieve='sums',
    enumeration_classes=None,
    multiply_raster_path=None,
    verbose=False,
    rewrite_zone_ids_raster=True,
    max_enumerate_value=1000,
):

    L.info('Launching dask_zonal_statistics.')

    # Test that input_raster and shapefile are in the same projection. Sillyness results if not.
    if assert_projections_same:
        hb.assert_gdal_paths_in_same_projection([input_raster, zone_vector_path])
    else:
        if verbose:
            a = hb.assert_gdal_paths_in_same_projection([input_raster, zone_vector_path], return_result=True)
            if not a:
                L.critical('Ran zonal_statistics_flex but the inputs werent in identical projections.')
        else:
            pass

    # if zone_ids_raster_path is not defined, use the PGP version, which doesn't use a rasterized approach.
    if not zone_ids_raster_path and rewrite_zone_ids_raster is False:
        to_return = pgp.zonal_statistics(
            base_raster_path_band, zone_vector_path,
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
        hb.convert_polygons_to_id_raster(zone_vector_path, zone_ids_raster_path, input_raster, id_column_label=id_column_label, data_type=zones_raster_data_type,
                                         ndv=zones_ndv, all_touched=all_touched)
    else:
        if verbose:
            L.info('Zone_ids_raster_path existed, so not creating it.')

    # Much of the optimization happens by using sparse arrays rather than look-ups so that the index int is the id of the zone.
    if unique_zone_ids is None:
        gdf = gpd.read_file(zone_vector_path)
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
        r = hb.zonal_statistics_rasterized_dask(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv, unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)
        # unique_ids, sums = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
        #                                                   unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)
        print(r)
        df = pd.DataFrame(index=unique_ids, data={'sums': sums})
        df[df == 0] = np.nan
        df.dropna(inplace=True)
        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
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
        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'enumeration':
        L.debug('Exporting enumeration.')

        if enumeration_classes is None:
            enumeration_classes = hb.unique_raster_values_path(input_raster)

        unique_ids, enumeration = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                 unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve,
                                                                 enumeration_classes=enumeration_classes, multiply_raster_path=multiply_raster_path,
                                                                 verbose=verbose, )
        enumeration = np.asarray(enumeration)
        df = pd.DataFrame(index=unique_ids, columns=[str(i) for i in list(range(0, len(enumeration_classes)))], data=enumeration)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')
            gdf_no_geom = gdf.drop(columns='geometry')

        if csv_output_path is not None:
            gdf_no_geom.to_csv(csv_output_path)

        return df

