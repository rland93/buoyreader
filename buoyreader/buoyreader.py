from urllib import request
import datetime
import numpy as np

# West Point Loma Buoy 46232

def get_buoy_data(buoy_number, buoy_root="http://www.ndbc.noaa.gov/data/realtime2/"):
    """NOAA Buoy Number and URL -> Data in ascii
    Keyword Arguments:
    buoy_number -- the NOAA buoy number
    buoy_root -- base url for NOAA buoys. Defaults to http://www.ndbc.noaa.gov/data/realtime2/
    """
    buoy_url = buoy_root + "{}.txt".format(str(buoy_number))
    bdata = request.urlopen(buoy_url, data=None)
    # urlobject -> str
    with bdata as response:
        raw_data = response.read().decode("ascii") 
    
    # raw data -> 2d array
    data = []
    for line in raw_data.splitlines():
        if not line.startswith("#"):
            data.append(line_format(line.split()))    
    return data
            
def swell_quality(waveheight,waveperiod):
    """Wave height and Wave Period -> Swell Quality (Float 0-10)
    
    Arguments:
    Wave Height - Wave height in meters.
    Wave Period - Wave period in seconds.
    """
    b = waveperiod  # b is the dominant wave period
    x = waveheight  # x is surf height in meters.
    quality_good = 8.5 * (23/20)**x + (2/5) * b - 3 - 8.5
    quality_bad = (b - 8) * x
    quality =  max(0, min(quality_good, quality_bad))
    return quality

def line_format(split_line):
    """Prune unimportant info from a line and return the pruned list."""
    date_time = ldatetime(split_line)
    try:
        dominant_wave_height = float(split_line[8])
    except:
        dominant_wave_height = np.nan
    try:
        dominant_period = int(split_line[9])
    except:
        dominant_period = np.nan
    try:
        dominant_direction = int(split_line[11])
    except:
        dominant_direction = np.nan
    try:
        temperature = float(split_line[14])
    except:
        temperature = np.nan

    quality = swell_quality(dominant_wave_height, dominant_period)

    return [date_time, dominant_wave_height, dominant_period, dominant_direction, temperature, quality]

def ldatetime(line):
    """split line from raw data -> datetime object"""
    return datetime.datetime(
                            int(line[0]),
                            int(line[1]),
                            int(line[2]),
                            int(line[3]),
                            int(line[4]))