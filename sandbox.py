import buoyreader.get_data as br
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

plt.style.use("seaborn-notebook")
sns.set_context("paper")


point_loma = br.format_data(br.get_buoy_data(46232))




wvql = point_loma["WVQL (0-10)"].rolling(window = 20).mean()

wvql.plot()
plt.xlabel("Time")
plt.ylabel("SWELL Quality 0-10")
plt.title("Wave Quality over Time, Pt Loma Buoy #46232, Rolling Average (10 Hours)")
plt.show()