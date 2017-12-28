import buoyreader.main as br
import pandas as pd
from pandas.tseries import converter
converter.register()
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#['seaborn-dark', 'seaborn-darkgrid', 'seaborn-ticks', 'fivethirtyeight', 'seaborn-whitegrid', 'classic', '_classic_test', 'fast', 'seaborn-talk', 'seaborn-dark-palette', 'seaborn-bright', 'seaborn-pastel', 'grayscale', 'seaborn-notebook', 'ggplot', 'seaborn-colorblind', 'seaborn-muted', 'seaborn', 'Solarize_Light2', 'seaborn-paper', 'bmh', 'seaborn-white', 'dark_background', 'seaborn-poster', 'seaborn-deep']



plt.style.use("seaborn-notebook")
sns.set_context("paper")

def tabulate(buoy_array):
    dates = []
    waveht = []
    waveper = []
    wavedir = []
    temp = []
    quality = []
    period_bin = []
    season = []
    season_hemi = []
    for line in buoy_array:
        dates.append(line.get("datetime"))
        waveht.append(line.get("ht"))
        waveper.append(line.get("period"))
        wavedir.append(line.get("direction"))
        temp.append(line.get("temp"))
        quality.append(line.get("quality"))
        period_bin.append(line.get("period_bin"))
        season.append(line.get("season"))
        season_hemi.append(line.get("season hemi"))
    df = pd.DataFrame({
        "Wave Height (Meters)": waveht,
        "Wave Period": waveper,
        "Wave Direction (Degrees)": wavedir,
        "Water Temperature": temp,
        "Swell Quality": quality,
        "Period Bin": period_bin,
        "Season": season,
        "Season (Summer or Winter Only)":season_hemi},
        index=dates)
    df = df.sort_index(axis=0,ascending=True)
    df["Ticks"] = range(0, len(df.index.values))
    return df

x = br.raw_data_to_array(br.read_historical_data("2014-2016.txt"))
hist = tabulate(x)


f, axes = plt.subplots(1, 2, figsize=(9, 3.5), sharex=False)

'''
univariate_by_season = ["Wave Direction (Degrees)","Wave Height (Meters)","Water Temperature","Wave Period"]
sns.distplot(hist[univariate_by_season[0]].loc[hist["Season"] == "Spring"],label="Spring",hist=False,ax=axes[0])
sns.distplot(hist[univariate_by_season[0]].loc[hist["Season"] == "Summer"], label= "Summer",hist=False,ax=axes[0])
sns.distplot(hist[univariate_by_season[0]].loc[hist["Season"] == "Fall"], label="Fall",hist=False,ax=axes[0])
sns.distplot(hist[univariate_by_season[0]].loc[hist["Season"] == "Winter"], label="Winter",hist=False,ax=axes[0])


sns.distplot(hist[univariate_by_season[1]].loc[hist["Season"] == "Spring"],label="Spring",hist=False,ax=axes[1])
sns.distplot(hist[univariate_by_season[1]].loc[hist["Season"] == "Summer"], label= "Summer",hist=False,ax=axes[1])
sns.distplot(hist[univariate_by_season[1]].loc[hist["Season"] == "Fall"], label="Fall",hist=False,ax=axes[1])
sns.distplot(hist[univariate_by_season[1]].loc[hist["Season"] == "Winter"], label="Winter",hist=False,ax=axes[1])
'''

'''
uni = ["Wave Direction (Degrees)","Wave Height (Meters)"]
sns.distplot(hist[uni[0]].loc[hist["Season (Summer or Winter Only)"] == "Summer"],label="Summer",ax=axes[0])
sns.distplot(hist[uni[0]].loc[hist["Season (Summer or Winter Only)"] == "Winter"],label="Winter",ax=axes[0])

sns.distplot(hist[uni[1]].loc[hist["Season (Summer or Winter Only)"] == "Summer"],label="Summer",ax=axes[1])
sns.distplot(hist[uni[1]].loc[hist["Season (Summer or Winter Only)"] == "Winter"],label="Winter",ax=axes[1])
'''
print(hist.sample(n=100))

#plt.show()