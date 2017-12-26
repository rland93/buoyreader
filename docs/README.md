# buoyreader
## A simple scraper for NOAA buoy data.
I wanted to write a program that would scrape the data from the NOAA's buoys so that I could learn how to visualize some data.

Right now it is written to scrape the [Point Loma South](http://www.ndbc.noaa.gov/station_page.php?station=46232) buoy near all of my home breaks :-). I think it could be generalized for any buoy data though, since all of the buoys I have seen on the NOAA site have the same format.

Planned features:
* Web interface.
* Historic data view.
* Quick stats 'dashboard' (water temp, largest swell, etc.).
* Cool data viz stuff.
* Nice fonts and design throughout.

## Sample Buoy Data:
    
for example: http://www.ndbc.noaa.gov/data/realtime2/46232.txt

what it should look like (with one line of data):

        YY   MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS PTDY  TIDE
        yr   mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC  nmi  hPa    ft
        2017 11 16 00 41  MM   MM   MM   1.2    13   7.4 225     MM    MM  17.5    MM   MM   MM    MM
