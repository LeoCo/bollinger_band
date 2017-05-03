from datamanager import Data as Data
import time
from trader import Trader as Trader

class Engine(object):

    def __init__(self, time_window = 5, interval=1, bb_length = 3):

        #Update interval
        self.interval = interval

        #Time window to visualize
        self.time_window = time_window

        #Create the Data() object
        self.data = Data(buffer_days=self.time_window)

        #Initialize the object
        self.data.init_data(self.interval)

        #Initialize and use the bollingerbands
        self.data.init_bollingerbands(length=bb_length)

        #Initialize the trader agent
        self.trader = Trader(self.data)


    def run(self, loops = 10000):

        counter = 0

        while (counter < loops):

            # Print the dataset
            ## print(self.data.historic_data)

            #Print loop number:
            #print('Loop: ' + str(counter) + ' Price:' + str(self.data.historic_data['Price'].iloc[-1]) +'\tShares: ' +
            #      str(self.trader.current_stocks))

            # Exec the trading
            self.trader.trade()

            # Wait the interval
            time.sleep(self.interval)

            # Update the historic dataset
            self.data.update_data()

            # Counter++
            counter += 1