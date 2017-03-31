from livedata import livedata as livedata
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

class engine(object):

    def __init__(self, time_window = 5, interval=1):

        #Update interval
        self.interval = interval

        #Time window to visualize
        self.time_window = time_window

        #Historic data
        self.historic_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

        #Load the livedata object
        self.live = livedata()

        #Initialize the data
        for x in range(0, self.time_window):
            temp_df = pd.DataFrame([self.live.get_mock_prices()], columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                                   index=[pd.to_datetime('now')])
            self.historic_data = self.historic_data.append(temp_df)
            time.sleep(self.interval)

        #Set bollingerbands as false
        self.bollingerbands = False


    def run(self, graphics=False):

        while (True):

            # Print the dataset
            print(self.historic_data)

            if graphics == True:
                # Copy the historic dataset
                data = self.historic_data.copy()

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

                # Title
                plt.title("GOOG")

                # Candle stick chart
                candlestick_ohlc(ax, data[['Date2', 'Open', 'High', 'Low', 'Close']].values, width=.000001, colorup='g',
                                 alpha=.4)

                # Plot and pause the chart
                plt.pause(self.interval)

                # Close the figure to save memory
                plt.close(fig)


            if graphics == False:
                # Wait the interval
                time.sleep(self.interval)

            # Update the historic dataset
            self.update_data()

    def update_data(self):

        #Remove the first (latest in time) element
        self.historic_data = self.historic_data[1:]

        #Create the new record to append
        temp_df = pd.DataFrame([self.live.get_mock_prices()], columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                               index=[pd.to_datetime('now')])

        #Append the record
        self.historic_data = self.historic_data.append(temp_df)

        #If bollingerbands are initialized
        if self.bollingerbands == True:

            # Update the last value of rolling mean
            rollingmean = self.historic_data['Close'].rolling(window=self.bollingerbands_length,center=False).mean()
            self.historic_data['Rolling Mean'].iloc[-1] = rollingmean.iloc[-1]

            # Update the last value of rolling std
            rollingstd = self.historic_data['Close'].rolling(window=self.bollingerbands_length, center=False).std()
            self.historic_data['Rolling Std'].iloc[-1] = rollingstd.iloc[-1]



    def init_bollingerbands(self, length = 3):

        self.bollingerbands = True

        #Check if there are enough data to calculate the rolling mean/std
        if length <= self.time_window:
            self.bollingerbands_length = length
        else:
            self.bollingerbands_length = self.time_window

        #Initialiaze rolling mean
        self.historic_data['Rolling Mean'] = np.nan

        #Initialiaze rolling std
        self.historic_data['Rolling Std'] = np.nan


