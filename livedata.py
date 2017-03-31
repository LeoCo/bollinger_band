import pandas as pd
import datetime

class livedata(object):

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

    def get_mock_prices(self):

        if self.counter < (len(self.mockdata) - 1):

            result = self.mockdata.ix[self.counter]
            self.counter += 1
            return result.values.tolist()
        else:
            return self.mockdata.ix[-1].values.tolist()

if __name__ == '__main__':
    print('Test of the mock loader')

    live = livedata()

    for _ in range(0,5):
        print(live.get_mock_prices())