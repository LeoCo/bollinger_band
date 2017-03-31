from livedata import LiveData as LiveData
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import logging

class Engine(object):

    def __init__(self, time_window = 5, interval=1):

        #Update interval
        self.interval = interval

        #Time window to visualize
        self.time_window = time_window

        #Historic data
        self.historic_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

        #Load the livedata object
        self.live = LiveData()

        #Initialize the data
        for x in range(0, self.time_window):
            temp_df = pd.DataFrame([self.live.get_live_data()], columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                                   index=[pd.to_datetime('now')])
            self.historic_data = self.historic_data.append(temp_df)
            time.sleep(self.interval)

        #Set bollingerbands as false
        self.bollingerbands = False


    def run(self, graphics=False, candlestick = True):

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

                # Plot BB if activated
                if self.bollingerbands == True:
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
            self.update_data()

    def update_data(self):

        #Remove the first (latest in time) element
        self.historic_data = self.historic_data[1:]

        #Create the new record to append
        temp_df = pd.DataFrame([self.live.get_live_data()], columns=['Open', 'High', 'Low', 'Close', 'Volume'],
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

            # Update the last value of Upper BB
            self.historic_data['Upper BB'].iloc[-1] = rollingmean.iloc[-1] + 2 * rollingstd.iloc[-1]

            # Update the last value of Lower BB
            self.historic_data['Lower BB'].iloc[-1] = rollingmean.iloc[-1] - 2 * rollingstd.iloc[-1]


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

        #Initialize Upper Bollinger Band
        self.historic_data['Upper BB'] = np.nan

        # Initialize Lower Bollinger Band
        self.historic_data['Lower BB'] = np.nan

class Trader(object):

    def __init__(self):
        pass


class Wallet(object):

    BUDGET = 1000

    def __init__(self):
        self.money = self.BUDGET

        # Initialize logger
        self.logger = logging.getLogger('wallet_logger')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler('log/wallet.log')
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

        # Log Starting Balance
        self.logger.info('')
        self.logger.info('Starting Balance: ' + str(self.money))



    def withdraw(self, amount):
        self.money = self.money - amount
        self.logger.info('Withdraw: ' + str(amount) + ' | Balance: ' + str(self.money))
        return amount

    def deposit(self, amount):
        self.money = self.money + amount
        self.logger.info('Deposit: ' + str(amount) + ' | Balance: ' + str(self.money))
        return amount

    def balance(self):
        return self.money

    def print(self):
        print("The money in the wallet is: " + str(self.money))


if __name__ == '__main__':

    wallet = Wallet()

    wallet.withdraw(300)

    wallet.deposit(200)

    wallet.print()