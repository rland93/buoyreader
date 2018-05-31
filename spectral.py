'''
Parse spectral data.

For an explanation of spectral and
directional data, see:
http://www.ndbc.noaa.gov/measdes.shtml,
subsection "Spectral Wave Data."
'''
from urllib import request
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_data(buoy_number=46232,
             mode='url',
             buoy_root='http://www.ndbc.noaa.gov/data/realtime2/',
             textfile_data_spec=None, # Spectral Wave Data ie alpha1 data. **
             textfile_swdir=None):    # Directional Wave Data ie r1 data. **
    '''
    :param buoy_number: Buoy Number
    :param mode: Mode. 'file' for a local file, or 'url' for a url.
    :param buoy_root: Bouy root. Defaults to NOAA url.
    :param textfile_data_spec: '.data_spe' file path, optional if :param mode: ='url'.
    :param textfile_swdir: '.swdir' file path, optional if :param mode: ='url'.
    :return:
    '''

    if mode == 'url' and buoy_root and buoy_number:
        # Buoy URLs for magnitude and direction
        url_mag = buoy_root + '{}.data_spec'.format(str(buoy_number))
        url_dir = buoy_root + '{}.swdir'.format(str(buoy_number))
        # Open both with urlopen
        with request.urlopen(url_mag, data=None) as response:
            mag = response.read().decode('ascii')
        with request.urlopen(url_dir, data=None) as response:
            dir = response.read().decode('ascii')
        # Return both as dict
        return {'mag':mag,'dir':dir}

    elif mode == 'file' and textfile_data_spec and textfile_swdir:
        # Get buoy data from files
        mag = open(textfile_data_spec,'r',encoding='ascii').read()
        dir = open(textfile_swdir,'r',encoding='ascii').read()
        # Return both as dict
        return {'mag':mag,'dir':dir}

    else:
        return None


def format_data(buoy_data):
    '''
    :param buoy_data:
    :return: Time series DataFrame. Columns are frequencies
    '''
    mag = []
    for line in buoy_data['mag'].splitlines()[1:]:
        # Make the line(str) into a list
        split_line = line.split()
        # Fix the line by excluding element 5 of the list
        fixed_line = [item for index, item in enumerate(split_line) if index != 5]
        # Append the line(list) to :mag:
        mag.append(fixed_line)
        # We don't need to fix 'dir' because it's lacking that troublesome 5th element
    dir = [x.split() for x in buoy_data['dir'].splitlines()[1:]]

    # Build index
    index = []
    for line in mag:
        index.append(find_datetime(line))

    # Check to see that the datetime indices match up.
    index_CHECK = []
    for line in dir:
        index_CHECK.append(find_datetime(line))
    for equivalent in zip(index, index_CHECK):
        if equivalent[0] != equivalent[1]:
            raise ValueError

    # Build Data
    # From this:
    # mag =[ ['YY','MM','DD','hh','mm','mag','freq1','mag','freq2'...]
    #        ['YY','MM','DD','hh','mm','mag','freq1','mag','freq2'...]
    #        ['YY','MM','DD','hh','mm','mag','freq1','mag','freq2'...] ]
    #
    # dir =[ ['YY','MM','DD','hh','mm','dir','freq1','dir','freq2'...]
    #        ['YY','MM','DD','hh','mm','dir','freq1','dir','freq2'...]
    #        ['YY','MM','DD','hh','mm','dir','freq1','dir','freq2'...] ]
    #
    # To This:
    # df =
    #        <  freq1  ,  freq2  ,  freq_m >
    # date1  [(mag,dir),(mag,dir),(mag,dir)]
    # date2  [(mag,dir),(mag,dir),(mag,dir)]
    #  ...
    # date_n [(mag,dir),(mag,dir),(mag,dir)]
    data = []


    # remove ()
    columns = []
    for x in mag[0][6::2]:
        columns.append(float(x.strip("()")))
    columns

    # evens of mag or dir are identical across rows because they represent frequency bins
    for point in zip(mag,dir):
        x = []
        for item in zip(point[0][5::2],point[1][5::2]):
            x.append(item)
        data.append(x)
    return pd.DataFrame(data=data, index=index, columns=columns)


def find_datetime(line):
    '''
    Get date and time from list where it appears first.
    :param line: Something like ['2018','10','29','11','20', ... ]
    :return: Date time, python date time object
    '''
    return datetime.datetime(
        int(line[0]), #YYYY
        int(line[1]), #MM
        int(line[2]), #DD
        int(line[3]), #hh
        int(line[4]), #mm
    )

# example
# data = format_data(get_data(mode='file', textfile_data_spec='46232.data_spec', textfile_swdir='46232.swdir'))