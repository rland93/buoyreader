from urllib import request
import datetime
import numpy as np
import pandas as pd

# West Point Loma Buoy 46232

def get_buoy_data(buoy_number, buoy_root="http://www.ndbc.noaa.gov/data/realtime2/"):
    """NOAA Buoy Number and URL -> Data in ascii
    Keyword Arguments:
    ``buoy_number``: the NOAA buoy number
    ``buoy_root``: base url for NOAA buoys. Defaults to http://www.ndbc.noaa.gov/data/realtime2/
    """
    buoy_url = buoy_root + "{}.txt".format(str(buoy_number))
    bdata = request.urlopen(buoy_url, data=None)
    # urlobject -> str
    with bdata as response:
        raw_data = response.read().decode("ascii")
    return raw_data

def read_historical_data(textfile):
    """read a textfile instead of live data.
    
    Arguments:
    ``textfile``: some plain text file with buoy data.

    Whole lot of those can be found here:
    http://www.ndbc.noaa.gov/historical_data.shtml
    """
    with open(textfile, "r") as file:
        raw_data = file.read()
    return raw_data
            
def swell_quality(waveheight,waveperiod):
    """Wave height and Wave Period -> Swell Quality 0-10
    
    Arguments:
    * ``waveheight``: Wave height (float or int) in meters.
    * ``waveperiod``: Wave period (float or int) in seconds.
    """
    p = waveperiod  # b is the dominant wave period
    h = waveheight  # x is surf height in meters.

    quality = min(10, (2/7)*h*(47/40)**((8/9)*(p+3)))

    return quality

def bin_period_data(period, longperiod=14, shortperiod=9):
    """Period (float) -> Descriptive Magnitude (str).
    
    ie, a long period swell, a mid period swell, and
    a short period swell.

    Arguments:
    * ``period``: swell period. Must be float.
    * ``long``: swells over this value will be long period.
    * ``short``: swells under this value will be short period.
    Swells between long and short will be mid period.
    """
    if period > longperiod:
        period_bin = "Long (>{}s)".format(longperiod)
    elif longperiod >= period > shortperiod:
        period_bin = "Mid ({}s > x > {}s)".format(longperiod, shortperiod)
    elif shortperiod >= period:
        period_bin = "Short (<{}s)".format(shortperiod)
    return period_bin

def ldatetime(line):
    """split line from raw data -> datetime object
    
    Aguments:
    * ``line``: Single line ['yyyy','mm','dd','hh','mm']
    """
    return datetime.datetime(
        int(line[0]),
        int(line[1]),
        int(line[2]),
        int(line[3]),
        int(line[4]))

def format_data(buoy_data):
    """Bouy data as string -> Pandas dataframe

    Args:

    ``buoy_data``: buoy data (string)
    """
    # first line will have heading info.
    heading = []
    subheading = []
    buoy_data = buoy_data.splitlines()

    # Build headings:
    for i, line in enumerate(buoy_data):
        if i == 0 and line.startswith("#"):
            heading = line.split()
        if i == 1 and line.startswith("#"):
            subheading = line.split()
    for index, (value_h, value_s) in enumerate(zip(heading, subheading)):
        # Remove "#" from headings.
        if value_h.startswith("#"):
            value_h = value_h.replace("#", "")
        if value_s.startswith("#"):
            value_s = value_s.replace("#", "")
        # Combine headings
        heading[index] = (value_h + " (" + value_s + ")")
    # Build data:
    data = []
    # datetimes will become the index of our dataframe.
    datetimes = []
    # cases of "missing data" we want to replace
    missing_data_to_replace = frozenset(["999", "99.0", "9999.0", "999.0", "99.00"])
    for i, line in enumerate(buoy_data):
        if i > 2:
            # build lines
            split_line = line.split()
            # some of the NOAA data has "99" or "99.0" or "999.0"
            # in cases where data is missing; we don't want numerical
            # values so we replace those.
            split_line = [np.NaN if x in missing_data_to_replace else x for x in split_line]
            # for n, item in enumerate(split_line):
            #     if item in missing_data_to_replace:
            #         split_line[n] = np.NaN

            # append swell quality to dataframe
            split_line.append(swell_quality(float(split_line[8]), float(split_line[9])))

            data.append(split_line)
            # build index
            datetimes.append(ldatetime(split_line))
    
    # append swell quality col to dataframe
    heading.append("WVQL (0-10)")
    return pd.DataFrame(data, columns=[i for i in heading], index=datetimes)
    