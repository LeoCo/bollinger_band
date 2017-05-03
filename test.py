import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import numpy as np


def dateparse (time_in_secs):
    return datetime.datetime.fromtimestamp(float(time_in_secs))

#import
file_name = 'data/goog.csv'

data = pd.read_csv(file_name, parse_dates=True, date_parser=dateparse, index_col='Date') #index_col='Date

print(data)

#bollinger bands
def bbands(price, length=3, numsd=3):
    """ returns average, upper band, and lower band"""
    ave = pd.stats.moments.rolling_mean(price,length)
    sd = pd.stats.moments.rolling_std(price,length)
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return np.round(ave,3), np.round(upband,3), np.round(dnband,3)

data['Average'], data['Upper'], data['Lower'] = bbands(data['Close'], length=30, numsd=1)

print(data)

#plot
data['Date2'] = mdates.date2num(data.index.to_pydatetime())

print(data['Date2'])

fig, ax = plt.subplots()
ax.xaxis_date()
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("GOOG")
plt.plot(data['Average'])
plt.plot(data['Upper'])
plt.plot(data['Lower'])
candlestick_ohlc(ax, data[['Date2','Open','High','Low','Close']].values, width=.001, colorup='g', alpha =.4)

plt.show()