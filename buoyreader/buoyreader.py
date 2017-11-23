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
        return ("HTTPerror", str(e))
        print(str(e))
    except request.URLError as e:
        return ("URLerror", str(e))
        print(str(e))
    else:
        with httpobject as response:
            raw_data = response.read().decode("ascii") 
        # return data as str
        return raw_data

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

def lyear(line):
    return int(line[0])

def lmonth(line):
    return int(line[1])

def lday(line):
    return int(line[2])

def lhour(line):
    return int(line[3]) + 16

def lminute(line):
    return int(line[4])

def lheight(line):
    return float(line[8])

def lperiod(line):
    return int(line[9])

def ldir(line):
    return int(line[11])

def ltemp(line):
    return float(line[14])

def ldatetime(line):
    return datetime.datetime(lyear(line),
                          lmonth(line),
                          lday(line),
                          lhour(line),
                          lminute(line))

def ltimedelta(line):
    current_time = datetime.datetime.today()
    return current_time - ldatetime(line)

def meters_to_feet(m):
    ft = round(m * 3.28084,ndigits=1)
    return ft

def celcius_to_freedom_units(degc):
    degf = round(degc * (9/5) + 32, ndigits=1)
    return degf


current = get_first_line(get_buoy_data(46232))
month = lmonth(current)
day = lday(current)
hour = lhour(current)
minute = lminute(current)


print("Data for {}-{} at {}:{}".format(month,day,hour,minute))