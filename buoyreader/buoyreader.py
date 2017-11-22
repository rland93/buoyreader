# http://www.ndbc.noaa.gov/data/realtime2/46232.txt
#
#               what it should look like:
#
#  YY   MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS PTDY  TIDE
#  yr   mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC  nmi  hPa    ft
#  2017 11 16 00 41  MM   MM   MM   1.2    13   7.4 225     MM    MM  17.5    MM   MM   MM    MM
#    0   1  2  3  4   5    6    7     8     9    10  11     12    13    14    15   16   17    18


# WDIR 	Wind direction (the direction the wind is coming from in degrees clockwise from true N) during the same period used for WSPD. See Wind Averaging Methods
# WSPD 	Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for land stations. Reported Hourly. See Wind Averaging Methods.
# GST 	Peak 5 or 8 second gust speed (m/s) measured during the eight-minute or two-minute period. The 5 or 8 second period can be determined by payload, See the Sensor Reporting, Sampling, and Accuracy section.
# WVHT 	Significant wave height (meters) is calculated as the average of the highest one-third of all of the wave heights during the 20-minute sampling period. See the Wave Measurements section.
# DPD 	Dominant wave period (seconds) is the period with the maximum wave energy. See the Wave Measurements section.
# APD 	Average wave period (seconds) of all waves during the 20-minute period. See the Wave Measurements section.
# MWD 	The direction from which the waves at the dominant period (DPD) are coming. The units are degrees from true North, increasing clockwise, with North as 0 (zero) degrees and East as 90 degrees. See the Wave Measurements section.
# PRES 	Sea level pressure (hPa). For C-MAN sites and Great Lakes buoys, the recorded pressure is reduced to sea level using the method described in NWS Technical Procedures Bulletin 291 (11/14/80). ( labeled BAR in Historical files)
# ATMP 	Air temperature (Celsius). For sensor heights on buoys, see Hull Descriptions. For sensor heights at C-MAN stations, see C-MAN Sensor Locations
# WTMP 	Sea surface temperature (Celsius). For buoys the depth is referenced to the hull's waterline. For fixed platforms it varies with tide, but is referenced to, or near Mean Lower Low Water (MLLW).
# DEWP 	Dewpoint temperature taken at the same height as the air temperature measurement.
# VIS 	Station visibility (nautical miles). Note that buoy stations are limited to reports from 0 to 1.6 nmi.
# PTDY 	Pressure Tendency is the direction (plus or minus) and the amount of pressure change (hPa)for a three hour period ending at the time of observation. (not in Historical files)
# TIDE 	The water level in feet above or below Mean Lower Low Water (MLLW). 

from urllib import request
import datetime

# West Point Loma Buoy 46232

def get_buoy_data(buoy_number, buoy_root="http://www.ndbc.noaa.gov/data/realtime2/"):
    # create buoy url from buoy number
    buoy_url = buoy_root + "{}.txt".format(str(buoy_number))
    # open url as httpobject
    try:
        httpobject = request.urlopen(buoy_url, data=None)
    except request.HTTPError as e:
        print("HTTPError: " + str(e))
    except request.URLError as e:
        print("URLError: " + str(e))
    else:
        with httpobject as response:
            raw_data = response.read().decode("ascii") # I don't anticipate any encoding errors in this data.
        return raw_data

print(get_buoy_data(22222))


# get the most current line for real time information.
def get_first_line(string):
    i = string.splitlines()
    # This ensures that the headings (lines begin with #) 
    # aren't read and we only take the top row.
    for line in i:
        if not line.startswith('#'):
            firstline = line
            break
    return firstline.split()

def separate_data(split_line):
    today = datetime.datetime.today()
    t = datetime.datetime(int(split_line[0]),       # years (yyyy)
                          int(split_line[1]),       # months (mm)
                          int(split_line[2]),       # days (dd)
                          int(split_line[3]) -8,    # hh (subtract 8 GMT -> Pacific Time)
                          int(split_line[4]))       # minutes (mm)
    waveheight = round(float(split_line[8]) * 3.28084,ndigits=1)    # meters (m->ft)
    waveperiod = split_line[9]                                      # period (s)
    wavedir = split_line[11]                                        # direction (deg)
    temp = round(float(split_line[14]) * (9/5) + 32,ndigits=1)      # water temp (fahrenheight)

    wavedata = {
        "Current Time": today,
        "Old Data?": today - t,
        "Wave Height": waveheight,
        "Wave Period": waveperiod,
        "Wave Direction": wavedir,
        "Temperature": temp,}
    return wavedata

