import pandas as pd
import datetime
import time
import numpy as np

class LiveData(object):

    def __init__(self, mock=True):

        self.mock = mock

        if self.mock == True:

            #initialize the counter
            self.counter = 0

            #import the google file
            self.file_name = 'goog.csv'

            #Function to parse the dates
            def dateparse(time_in_secs):
                return datetime.datetime.fromtimestamp(float(time_in_secs))

            #Load the csv into mockdata
            self.mockdata = pd.read_csv(self.file_name, parse_dates=True, date_parser=dateparse, index_col='Date')

    def get_live_data(self):

        if self.mock == True:
            if self.counter < (len(self.mockdata) - 1):

                result = self.mockdata.ix[self.counter]
                self.counter += 1
                return result.values.tolist()
            else:
                return self.mockdata.ix[-1].values.tolist()
        else:
            pass

class Data(object):

    def __init__(self, buffer_days = 5):

        #Time window to visualize
        self.buffer_days = buffer_days

        #Historic data
        self.historic_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

        #Load the livedata object
        self.live = LiveData()

        #Set bollingerbands as false
        self.bollingerbands = False

    def init_data(self, interval):
        # Initialize the data
        for x in range(0, self.buffer_days):
            temp_df = pd.DataFrame([self.live.get_live_data()], columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                                   index=[pd.to_datetime('now')])
            self.historic_data = self.historic_data.append(temp_df)
            time.sleep(interval)

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
        if length <= self.buffer_days:
            self.bollingerbands_length = length
        else:
            self.bollingerbands_length = self.buffer_days

        #Initialiaze rolling mean
        self.historic_data['Rolling Mean'] = np.nan

        #Initialiaze rolling std
        self.historic_data['Rolling Std'] = np.nan

        #Initialize Upper Bollinger Band
        self.historic_data['Upper BB'] = np.nan

        # Initialize Lower Bollinger Band
        self.historic_data['Lower BB'] = np.nan

if __name__ == '__main__':
    print('Test of the mock loader')

    live = LiveData()

    for _ in range(0,5):
        print(live.get_live_data())