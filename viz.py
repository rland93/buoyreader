import buoyreader.main as br
import pandas as pd
from pandas.tseries import converter
converter.register()
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use("fivethirtyeight")

def tabulate(buoy_array):
    dates = []
    waveht = []
    waveper = []
    wavedir = []
    temp = []
    quality = []
    period_bin = []
    for line in buoy_array:
        dates.append(line[0])
        waveht.append(line[1])
        waveper.append(line[2])
        wavedir.append(line[3])
        temp.append(line[4])
        quality.append(line[5])
        period_bin.append(line[6])
    df = pd.DataFrame({
        "Wave Height": waveht,
        "Wave Period": waveper,
        "Wave Direction": wavedir,
        "Water Temp": temp,
        "Swell Quality": quality,
        "Period Bin": period_bin},
        index=dates)
    df = df.sort_index(axis=0,ascending=True)
    df["Ticks"] = range(0, len(df.index.values))
    return df

hist = br.raw_data_to_array(br.read_historical_data("2014-2016.txt"))
hist = tabulate(hist)

# window = 48
# hist["Mean Wave Height"] = hist["Wave Height"].rolling(window = window).mean()
# hist["Mean Wave Period"] = hist["Wave Height"].rolling(window = window).mean()
# hist["Mean Swell Quality"] = hist["Wave Height"].rolling(window = window).mean()

#sns.lmplot(x="Wave Height",y="Water Temp",hue="Period Bin",data=hist.sample(n=200))

sns.jointplot(x="Wave Height",y="Wave Period",data=hist,kind="kde", n_levels=10)
plt.show()

# print(hist["Mean Wave Height"].head(100))