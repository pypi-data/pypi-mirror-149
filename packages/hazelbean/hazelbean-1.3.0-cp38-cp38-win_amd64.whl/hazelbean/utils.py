import os, sys, shutil, warnings

import pprint
from collections import OrderedDict
import numpy as np

import hazelbean as hb
import math
from osgeo import gdal
import contextlib
import logging

import pandas as pd

L = hb.get_logger('hazelbean utils')

def hprint(*args, **kwargs):
    return hb_pprint(*args, **kwargs)

def pp(*args, **kwargs):
    return hb_pprint(*args, **kwargs)

def hb_pprint(*args, **kwargs):

    num_values = len(args)

    print_level = kwargs.get('print_level', 2) # NO LONGER IMPLEMENTED
    return_as_string = kwargs.get('return_as_string', False)
    include_type = kwargs.get('include_type', False)

    indent = kwargs.get('indent', 2)
    width = kwargs.get('width', 120)
    depth = kwargs.get('depth', None)

    printable = ''

    for i in range(num_values):
        if type(args[i]) == hb.ArrayFrame:
            # handles its own pretty printing via __str__
            line = str(args[i])
        elif type(args[i]) is OrderedDict:
            line = 'OrderedDict\n'
            for k, v in args[i].items():
                if type(v) is str:
                    item = '\'' + v + '\''
                else:
                    item = str(v)
                line += '    ' + str(k) + ': ' + item + ',\n'
                # PREVIOS ATTEMPT Not sure why was designed this way.
                # line += '    \'' + str(k) + '\': ' + item + ',\n'
        elif type(args[i]) is dict:
            line = 'dict\n'
            line += pprint.pformat(args[i], indent=indent, width=width, depth=depth)
            # for k, v in args[i].items():
            #     if type(v) is str:
            #         item = '\'' + v + '\''
            #     else:
            #         item = str(v)
            #     line += '    ' + str(k) + ': ' + item + ',\n'
        elif type(args[i]) is list:
            line = 'list\n'
            line += pprint.pformat(args[i], indent=indent, width=width, depth=depth)
            # for j in args[i]:
            #     line += '  ' + str(j) + '\n'
        elif type(args[i]) is np.ndarray:

            try:
                line = hb.describe_array(args[i])
            except:
                line = '\nUnable to describe array.'

        else:
            line = pprint.pformat(args[i], indent=indent, width=width, depth=depth)

        if include_type:
            line = type(args[i]).__name__ + ': ' + line
        if i < num_values - 1:
            line += '\n'
        printable += line

    if return_as_string:
        return printable
    else:
        print (printable)
        return printable

@contextlib.contextmanager
def capture_gdal_logging():
    """Context manager for logging GDAL errors with python logging.

    GDAL error messages are logged via python's logging system, at a severity
    that corresponds to a log level in ``logging``.  Error messages are logged
    with the ``osgeo.gdal`` logger.

    Parameters:
        ``None``

    Returns:
        ``None``"""
    osgeo_logger = logging.getLogger('osgeo')

    def _log_gdal_errors(err_level, err_no, err_msg):
        """Log error messages to osgeo.

        All error messages are logged with reasonable ``logging`` levels based
        on the GDAL error level.

        Parameters:
            err_level (int): The GDAL error level (e.g. ``gdal.CE_Failure``)
            err_no (int): The GDAL error number.  For a full listing of error
                codes, see: http://www.gdal.org/cpl__error_8h.html
            err_msg (string): The error string.

        Returns:
            ``None``"""
        osgeo_logger.log(
            level=GDAL_ERROR_LEVELS[err_level],
            msg='[errno {err}] {msg}'.format(
                err=err_no, msg=err_msg.replace('\n', ' ')))

    gdal.PushErrorHandler(_log_gdal_errors)
    try:
        yield
    finally:
        gdal.PopErrorHandler()

def describe(input_object, file_extensions_in_folder_to_describe=None, surpress_print=False, surpress_logger=False):
    # Generalization of describe_array for many types of things.

    description = ''

    input_object_type = type(input_object).__name__
    if type(input_object) is hb.ArrayFrame:
        description = hb.describe_af(input_object.path)

    if type(input_object) is np.ndarray:
        description = hb.describe_array(input_object)
    elif type(input_object) is str:
        try:
            folder, filename = os.path.split(input_object)
        except:
            folder, filename = None, None
        try:
            file_label, file_ext = os.path.splitext(filename)
        except:
            file_label, file_ext = None, None
        if file_ext in hb.common_gdal_readable_file_extensions or file_ext in ['.npy']:
            description = hb.describe_path(input_object)
        elif not file_ext:
            description = 'type: folder, contents: '
            description += ' '.join(os.listdir(input_object))
            if file_extensions_in_folder_to_describe == '.tif':
                description += '\n\nAlso describing all files of type ' + file_extensions_in_folder_to_describe
                for filename in os.listdir(input_object):
                    if os.path.splitext(filename)[1] == '.tif':
                        description += '\n' + describe_path(input_object)
        else:
            description = 'Description of this is not yet implemented: ' + input_object

    ds = None
    array = None
    if not surpress_print:
        pp_output = hb.hb_pprint(description)
    else:
        pp_output = hb.hb_pprint(description, return_as_string=True)

    if not surpress_logger:
        L.info(pp_output)
    return description

def safe_string(string_possibly_unicode_or_number):
    """Useful for reading Shapefile DBFs with funnycountries"""
    return str(string_possibly_unicode_or_number).encode("utf-8", "backslashreplace").decode()

def describe_af(input_af):
    if not input_af.path and not input_af.shape:
        return '''Hazelbean ArrayFrame (empty). The usual next steps are to set the shape (af.shape = (30, 50),
                    then set the path (af.path = \'C:\\example_raster_folder\\example_raster.tif\') and finally set the raster
                    with one of the set raster functions (e.g. af = af.set_raster_with_zeros() )'''
    elif input_af.shape and not input_af.path:
        return 'Hazelbean ArrayFrame with shape set (but no path set). Shape: ' + str(input_af.shape)
    elif input_af.shape and input_af.path and not input_af.data_type:
        return 'Hazelbean ArrayFrame with path set. ' + input_af.path + ' Shape: ' + str(input_af.shape)
    elif input_af.shape and input_af.path and input_af.data_type and not input_af.geotransform:
        return 'Hazelbean ArrayFrame with array set. ' + input_af.path + ' Shape: ' + str(input_af.shape) + ' Datatype: ' + str(input_af.data_type)

    elif not os.path.exists(input_af.path):
        raise NameError('AF pointing to ' + str(input_af.path) + ' used as if the raster existed, but it does not. This often happens if tried to load an AF from a path that does not exist.')

    else:
        if input_af.data_loaded:
            return '\nHazelbean ArrayFrame (data loaded) at ' + input_af.path + \
                   '\n      Shape: ' + str(input_af.shape) + \
                   '\n      Datatype: ' + str(input_af.data_type) + \
                   '\n      No-Data Value: ' + str(input_af.ndv) + \
                   '\n      Geotransform: ' + str(input_af.geotransform) + \
                   '\n      Bounding Box: ' + str(input_af.bounding_box) + \
                   '\n      Projection: ' + str(input_af.projection)+ \
                   '\n      Num with data: ' + str(input_af.num_valid) + \
                   '\n      Num no-data: ' + str(input_af.num_ndv) + \
                   '\n      ' + str(hb.pp(input_af.data, return_as_string=True)) + \
                   '\n      Histogram ' + hb.pp(hb.enumerate_array_as_histogram(input_af.data), return_as_string=True) + '\n\n'
        else:
            return '\nHazelbean ArrayFrame (data not loaded) at ' + input_af.path + \
                   '\n      Shape: ' + str(input_af.shape) + \
                   '\n      Datatype: ' + str(input_af.data_type) + \
                   '\n      No-Data Value: ' + str(input_af.ndv) + \
                   '\n      Geotransform: ' + str(input_af.geotransform) + \
                   '\n      Bounding Box: ' + str(input_af.bounding_box) + \
                   '\n      Projection: ' + str(input_af.projection)

                    # '\nValue counts (up to 30) ' + str(hb.pp(hb.enumerate_array_as_odict(input_af.data), return_as_string=True)) + \

def describe_dataframe(df):
    p = 'Dataframe of length ' + str(len(df.index)) + ' with ' + str(len(df.columns)) + ' columns. Index first 10: ' + str(list(df.index.values)[0:10])
    for column in df.columns:
        col = df[column]
        p += '\n    ' + str(column) + ': min ' + str(np.min(col)) + ', max ' + str(np.max(col)) + ', mean ' + str(np.mean(col)) + ', median ' + str(np.median(col)) + ', sum ' + str(np.sum(col)) + ', num_nonzero ' + str(np.count_nonzero(col)) + ', nanmin ' + str(np.nanmin(col)) + ', nanmax ' + str(np.nanmax(col)) + ', nanmean ' + str(np.nanmean(col)) + ', nanmedian ' + str(np.nanmedian(col)) + ', nansum ' + str(np.nansum(col))
    return(p)

def describe_path(path):
    ext = os.path.splitext(path)[1]
    # TODOO combine the disparate describe_* functionality
    # hb.pp(hb.common_gdal_readable_file_extensions)
    if ext in hb.common_gdal_readable_file_extensions:
        ds = gdal.Open(path)
        if ds.RasterXSize * ds.RasterYSize > 10000000000:
            return 'too big to describe'  # 'type: LARGE gdal_uri, dtype: ' + str(ds.GetRasterBand(1).DataType) + 'no_data_value: ' + str(ds.GetRasterBand(1).GetNoDataValue()) + ' sum: ' + str(sum_geotiff(input_object)) +  ', shape: ' + str((ds.RasterYSize, ds.RasterXSize)) + ', size: ' + str(ds.RasterXSize * ds.RasterYSize) + ', object: ' + input_object
        else:
            try:
                array = ds.GetRasterBand(1).ReadAsArray()
                return hb.describe_array(array)
            except:
                return 'Too big to open.'
    elif ext in ['.npy', '.npz']:
        try:
            array = hb.load_npy_as_array(path)
            return hb.describe_array(array)
        except:
            return 'Unable to describe NPY file because it couldnt be opened as an array'

    # try:
    #     af = hb.ArrayFrame(input_path)
    #     s = describe_af(af)
    #     L.info(str(s))
    # except:
    #     pass


def describe_array(input_array):
    description = 'Array of shape '  + str(np.shape(input_array))+ ' with dtype ' + str(input_array.dtype) + '. sum: ' + str(np.sum(input_array)) + ', min: ' + str(
        np.min(input_array)) + ', max: ' + str(np.max(input_array)) + ', range: ' + str(
        np.max(input_array) - np.min(input_array)) + ', median: ' + str(np.median(input_array)) + ', mean: ' + str(
        np.mean(input_array)) + ', num_nonzero: ' + str(np.count_nonzero(input_array)) + ', size: ' + str(np.size(input_array)) + ' nansum: ' + str(
        np.nansum(input_array)) + ', nanmin: ' + str(
        np.nanmin(input_array)) + ', nanmax: ' + str(np.nanmax(input_array)) + ', nanrange: ' + str(
        np.nanmax(input_array) - np.nanmin(input_array)) + ', nanmedian: ' + str(np.nanmedian(input_array)) + ', nanmean: ' + str(
        np.nanmean(input_array))
    return description


def round_significant_n(input, n):
    # round_significant_n(3.4445678, 1)
    x = input
    try:
        int(x)
        absable = True
    except:
        absable = False
    if x != 0 and absable:
        out = round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))
    else:
        out = 0.0
    return out

def round_to_nearest_containing_increment(input, increment, direction):
    if direction == 'down':
        return int(increment * math.floor(float(input) / increment))
    elif direction == 'up':
        return int(increment * math.ceil(float(input) / increment))
    else:
        raise NameError('round_to_nearest_containing_increment failed.')


# TODOO Rename to_bool and maybe have a separate section of casting functions?
def str_to_bool(input):
    """Convert alternate versions of the word true (e.g. from excel) to actual python bool object."""
    return str(input).lower() in ("yes", "true", "t", "1", "y")

def normalize_array_memsafe(input_path, output_path, low=0, high=1, min_override=None, max_override=None, ndv=None, log_transform=True):

    raster_statistics =  hb.read_raster_stats(input_path)
    if min_override is None:
        min_override = raster_statistics['min']
    if max_override is None:
        max_override = raster_statistics['max']

    input_list = [input_path, low, high, min_override, max_override, ndv, log_transform]
    L.info('normalize_array_memsafe on ', input_path, output_path, low, high, min_override, max_override, ndv, log_transform)
    hb.raster_calculator_af_flex(input_list, normalize_array, output_path=output_path)

def normalize_array(array, low=0, high=1, min_override=None, max_override=None, ndv=None, log_transform=True):
    """Returns array with range (0, 1]
    Log is only defined for x > 0, thus we subtract the minimum value and then add 1 to ensure 1 is the lowest value present. """
    array = array.astype(np.float64)
    if ndv is not None: # Slightly slower computation if has ndv. optimization here to only consider ndvs if given.
        if log_transform:
            if min_override is None:
                L.debug('Starting to log array for normalize with ndv.')
                min = np.min(array[array != ndv])
                L.debug('  Min was ' + str(min))
            else:
                min = min_override
            to_add = np.float64(min * -1.0 + 1.0) # This is just to subtract out the min and then add 1 because can't log zero
            array = np.where(array != ndv, np.log(array + to_add), ndv)
            L.debug('  Finished logging array')

        # Have to do again to get new min after logging.
        if min_override is None:
            L.debug('Getting min from array', array, array[array != ndv], array.shape)

            min = np.min(array[array != ndv])
        else:
            min = min_override

        if max_override is None:
            L.info('Getting max from array', array, array[array != ndv], array.shape)
            max = np.max(array[array != ndv])
        else:
            max = max_override

        normalizer = np.float64((high - low) / (max - min))

        output_array = np.where(array != ndv, (array - min) * normalizer, ndv)
    else:
        if log_transform:
            L.info('Starting to log array for normalize with no ndv.')
            min = np.min(array)
            to_add = np.float64(min * -1.0 + 1.0)
            array = array + to_add

            array = np.log(array)

        # Have to do again to get new min after logging.
        if min_override is None:
            min = np.min(array[array != ndv])
        else:
            min = min_override

        if max_override is None:
            max = np.max(array[array != ndv])
        else:
            max = max_override
        normalizer = np.float64((high - low) / (max - min))

        output_array = (array - min) *  normalizer

    return output_array


def get_ndv_from_path(intput_path):
    """Return nodata value from first band in gdal dataset cast as numpy datatype.

    Args:
        dataset_uri (string): a uri to a gdal dataset

    Returns:
        nodata: nodata value for dataset band 1
    """
    dataset = gdal.Open(intput_path)
    band = dataset.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    if nodata is not None:
        nodata_out = nodata
    else:
        # warnings.warn(
        #     "Warning the nodata value in %s is not set", dataset_uri)
        nodata_out = None

    band = None
    gdal.Dataset.__swig_destroy__(dataset)
    dataset = None
    return nodata_out

def get_nodata_from_uri(dataset_uri):
    """Return nodata value from first band in gdal dataset cast as numpy datatype.

    Args:
        dataset_uri (string): a uri to a gdal dataset

    Returns:
        nodata: nodata value for dataset band 1
    """

    warnings.warn('get_nodata_from_uri deprecated for get_ndv_from_path ')
    dataset = gdal.Open(dataset_uri)
    band = dataset.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    if nodata is not None:
        nodata_out = nodata
    else:
        # warnings.warn(
        #     "Warning the nodata value in %s is not set", dataset_uri)
        nodata_out = None

    band = None
    gdal.Dataset.__swig_destroy__(dataset)
    dataset = None
    return nodata_out


# Make a non line breaking printer for updates.
def pdot(pre=None, post=None):
    to_dot = '.'
    if pre:
        to_dot = str(pre) + to_dot
    if post:
        to_dot = to_dot + str(post)
    sys.stdout.write(to_dot)

def parse_input_flex(input_flex):
    if isinstance(input_flex, str):
        output = hb.ArrayFrame(input_flex)
    elif isinstance(input_flex, np.ndarray):
        print('parse_input_flex is NYI for arrays because i first need to figure out how to have an af without georeferencing.')
        # output = hb.create_af_from_array(input_flex)
    else:
        output = input_flex
    return output

# TODOO Move this to a new dataframe_utils file.
def dataframe_reorder_columns(input_df, initial_columns=None, prespecified_order=None, remove_columns=None, sort_method=None):
    """If both initial_columns and prespecified_order are given, initial columns will override. Initial columns will also
    override remove columns. sort_method can be alphabetic or reverse_alphabetic."""
    if initial_columns is None:
        initial_columns = []
    if prespecified_order is None:
        prespecified_order = []
    if initial_columns is None:
        initial_columns = []
    if remove_columns is None:
        remove_columns = []

    if len(prespecified_order) <= 0:

        if sort_method == 'alphabetic':
            sorted_columns = sorted(list(input_df.columns))
        elif sort_method == 'reverse_alphabetic':
            sorted_columns = sorted(list(input_df.columns), reverse=True)
        else:
            sorted_columns = list(input_df.columns)
    else:
        sorted_columns = prespecified_order

    final_columns = initial_columns + [i for i in sorted_columns if i not in initial_columns and i not in remove_columns]

    return input_df[final_columns]

def get_unique_keys_from_vertical_dataframe(df, columns_to_check=None):
    if columns_to_check is None:
        columns_to_check = list(df.columns)

    keys_dict = {}
    lengths_dict = {}

    for column in columns_to_check:
        uniques = df[column].unique()
        keys_dict[column] = uniques
        lengths_dict[column] = len(uniques)

    return lengths_dict, keys_dict

def calculate_on_vertical_df(df, level, op_type, focal_cell, suffix):
    original_indices = df.index.copy()
    original_columns = df.columns.copy()
    if len(original_columns) > 1:
        raise NameError('Are you sure this is vertical data?')
    original_label = original_columns.values[0]

    dfp = df.unstack(level=level)
    r = dfp.columns.get_level_values(level=1)

    dfp.columns = r

    output_labels = []
    for i in dfp.columns:
        if op_type == 'difference_from_row' and i != focal_cell:
            dfp[i + suffix] = dfp[i] - dfp[focal_cell]
            output_labels.append(suffix)
        if op_type == 'percentage_change_from_row' and i != focal_cell:
            dfp[i + suffix] = ((dfp[i] - dfp[focal_cell]) / dfp[i]) * 100.0
            output_labels.append(suffix)

    dfo = pd.DataFrame(dfp.stack())

    dfo = dfo.rename(columns={0: original_label})

    dfor = dfo.reset_index()
    dforr = dfor.set_index(original_indices.names)

    # Reorder indices so it matches the input (restacking puts the targetted level outermost)

    return dforr


def df_merge(left_df, right_df, how=None, left_on=False, right_on=False, verbose=False):

    if verbose:
        L.info(
"""Merging: 
    
    left_df:
""" + str(left_df) + """
    right_df: 
""" + str(right_df) + """    
"""
)

    if how is None:
        how = 'outer'

    shared_column_labels = set(left_df.columns).intersection(set(right_df))
    identical_columns = []
    identical_column_labels = []
    for col in shared_column_labels:
        # LEARNING POINT, using df == df failed unintuitively because np.nan != np.nan. Any one instance of a nan cannot EQUAL another instance of a nan even though they seem identical. Perhaps this is because equals is implied to be a function of numbers?
        # LEARNING POINT: left_df[col].equals(right_df[col]) solved the np.nan != np.nan problem that arose with left_df[col] == (right_df[col])
        # LEARNING Point, however the above didn't address the fact that the column values being identical fails equals if the indices associated are not the same.

        if 'int' in str(left_df[col].dtype) or 'float' in str(left_df[col].dtype):
            # temporarily replace np.nan with -9999 so that it can test equality between nans
            left_array = np.where(np.isnan(left_df[col].values), -9999, left_df[col].values.astype(np.int64))
            right_array = np.where(np.isnan(right_df[col].values), -9999, right_df[col].values.astype(np.int64))
            if np.array_equal(left_array, right_array):
            # if left_df[col].equals(right_df[col]):
                identical_columns.append(left_df[col])
                identical_column_labels.append(col)

    for c, col in enumerate(identical_columns):
        if 'int' in str(col.dtype):
            left_on = identical_column_labels[c]
            right_on = identical_column_labels[c]
        break



    for col in shared_column_labels:
        if col != left_on and col != right_on:
            if verbose:
                L.info('Identical cols i that are not index or listed as merging on, so dropping right.')
            right_df = right_df.drop(col, axis=1)



    df = pd.merge(left_df, right_df, how=how, left_on=left_on, right_on=right_on)

    return df


def convert_py_script_to_jupyter(input_path):
    output_lines = []

    output_lines.append('#%% md')
    output_lines.append('')
    output_lines.append('# ' + hb.file_root(input_path))
    output_lines.append('')

    current_state = 'md'
    previous_state = 'md'

    with open(input_path) as fp:
        for line in fp:
            line = line.replace('\n', '')
            if line != '':

                if line.replace(' ', '')[0] == '#':
                    current_state = 'md'
                else:
                    current_state = 'py'
                # print(current_state + ': ', line, line)

                if current_state != previous_state:
                    if current_state == 'md':
                        output_lines.append('#%% md')
                    elif current_state == 'py':
                        output_lines.append('#%%')
                    else:
                        raise NameError('wtf')
                    previous_state = current_state

                if current_state == 'md':
                    to_append = line.split('#', 1)[1].lstrip()
                    output_lines.append(to_append)
                elif current_state == 'py':
                    output_lines.append(line)
                else:
                    raise NameError('wtf')

                # output_lines.append(line + '\n')
            else:
                # print(current_state + ': ', 'BLANK LINE', line)
                output_lines.append('')

    for line in output_lines:
        print(line)

    # ## DOESNT WORK BECAUSE NEED TO STRUCTURE JSON AS WELL, better is just to copy paste into pycharm lol
    # with open(output_path, 'w') as fp:
    #     for line in output_lines:
    #         print(line)
    #         fp.write(line)

def flatten_nested_dictionary(input_dict, return_type='values'):
    # NOT FINISHED. Still will accidentally not return two different values if have same top level key.
    def walk_dictionary(d, return_type):
        for key, value in d.items():

            if isinstance(value, dict):
                yield from walk_dictionary(value, return_type)
            else:
                if return_type == 'both':
                    yield (key, value)
                elif return_type == 'keys':
                    yield key
                elif return_type == 'values':
                    yield value

    # if return_type == 'both':
    #
    #     to_return = {}
    returned_list = list(walk_dictionary(input_dict, return_type))
    # for i in returned_list:
    #     to_return[i[0]] = i[1]
    return returned_list


