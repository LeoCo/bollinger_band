from data import LiveData as LiveData
from data import Data as Data
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import logging

class Engine(object):

    def __init__(self, time_window = 5, interval=1, bb_length = 5):

        #Update interval
        self.interval = interval

        #Time window to visualize
        self.time_window = time_window

        #Create the Data() object
        self.data = Data(buffer_days=self.time_window)

        #Initialize the object
        self.data.init_data(self.time_window)

        #Initialize and use the bollingerbands
        self.data.init_bollingerbands(length=bb_length)


    def run(self, graphics=False, candlestick = True):

        while (True):

            # Print the dataset
            print(self.data.historic_data)

            if graphics == True:
                # Copy the historic dataset
                data = self.data.historic_data.copy()

                # Create a new column for the dates (to fix compatibility issue with matplotlib dates)
                data['Date2'] = mdates.date2num(data.index.to_pydatetime())

                # Enable interactive plotting
                plt.ion()

                fig, ax = plt.subplots()

                # Set x axis format as a date
                ax.xaxis_date()

                # Labels
                plt.xticks(rotation=45)
                plt.xlabel("Date")
                plt.ylabel("Price")

                # Plot BB if activated
                if self.data.bollingerbands == True:
                    plt.plot(data['Rolling Mean'], label='Mean')
                    plt.plot(data['Upper BB'], label='Upper BB')
                    plt.plot(data['Lower BB'], label='Lower BB')

                # Title
                plt.title("Live Chart")

                if candlestick == True:
                    # Candle stick chart
                    candlestick_ohlc(ax, data[['Date2', 'Open', 'High', 'Low', 'Close']].values, width=.000001, colorup='g',
                                     alpha=.4)
                else:
                    plt.plot(data['Close'], label='Price')

                ax.legend(loc='upper left', shadow=True)


                # Plot and pause the chart
                plt.pause(self.interval)

                # Close the figure to save memory
                plt.close(fig)

            if graphics == False:
                # Wait the interval
                time.sleep(self.interval)

            # Update the historic dataset
            self.data.update_data()