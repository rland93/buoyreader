import buoyreader
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def testing():
    buoy_number = 46232
    line = buoyreader.get_first_line(buoyreader.get_buoy_data(buoy_number))
    buoy_date = buoyreader.ldatetime(line)
    height =    buoyreader.lheight(line)
    height_ft = buoyreader.meters_to_feet(buoyreader.lheight(line))
    period =    buoyreader.lperiod(line)
    wavedir =   buoyreader.ldir(line)
    tempc =     buoyreader.ltemp(line)
    tempf =     buoyreader.meters_to_feet(buoyreader.ltemp(line))

    return render_template("index.html",
                            line = line,
                            buoy_number = buoy_number,
                            buoy_date = buoy_date,
                            height = height,
                            height_ft = height_ft,
                            period = period,
                            wavedir = wavedir,
                            tempc = tempc,
                            tempf = tempf
                            )

if __name__ == "__main__":
    app.run()