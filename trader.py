import logging

class Trader(object):

    def __init__(self, stockdata):

        # load the data to trade
        self.stockdata = stockdata

        # Initialize current shares
        self.current_stocks = 0

        # Portolio to invest
        self.percentage_to_invest = 0.9

        # Create the wallet obj
        self.wallet = Wallet()

        # Initialize logger
        self.logger = logging.getLogger('trader_logger')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler('log/trader.log')
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

        # Log Starting Balance
        self.logger.info('')
        self.logger.info('Start trading')
        self.logger.info('Pos \tPrice\tUpp_BB\tDown_BB')

    def trade(self):

        if self.current_stocks == 0:

            self.take_position()

        else:

            self.leave_position()

    def trading_allowance(self, price):

            budget = self.wallet.balance() * self.percentage_to_invest

            stocks = int(budget / price)

            return stocks


    def take_position(self):

        position_to_take = 'wait'

        price = self.stockdata.historic_data['Price'].iloc[-1]

        upper_bb = self.stockdata.historic_data['Upper BB'].iloc[-1]

        lower_bb = self.stockdata.historic_data['Lower BB'].iloc[-1]

        if price > upper_bb:
            position_to_take = 'short'
        elif price < lower_bb:
            position_to_take = 'long'


        if position_to_take == 'wait':

            # Log
            self.logger.info('Wait\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}'.format(price,upper_bb,lower_bb,self.current_stocks))
            pass

        elif position_to_take == 'long':

            # Set the current shares
            self.current_stocks = self.trading_allowance(price)

            # Update the wallet
            self.wallet.withdraw(self.current_stocks * price)

            # Set the leaving threshold
            self.leave_threshold_upper = self.stockdata.historic_data['Rolling Mean'].iloc[-1] - 1 * self.stockdata.historic_data['Rolling Std'].iloc[-1]
            self.leave_threshold_lower = self.stockdata.historic_data['Rolling Mean'].iloc[-1] - 3 * self.stockdata.historic_data['Rolling Std'].iloc[-1]

            #Log
            self.logger.info('Long\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}\t| Enter Long position - Threshold Upp: {:.2f} Low:{:.2f}'
                                 ' - Balance: {:.2f}'.format(price,self.stockdata.historic_data['Upper BB'].iloc[-1],
                                                             self.stockdata.historic_data['Lower BB'].iloc[-1],
                                                             self.current_stocks,
                                                             self.leave_threshold_upper,self.leave_threshold_lower,
                                                             self.wallet.balance()))

        elif position_to_take == 'short':

            # Set the current shares
            self.current_stocks = - self.trading_allowance(price)

            # Update the wallet
            self.wallet.deposit(-self.current_stocks * price)

            # Set the leaving threshold
            self.leave_threshold_upper = self.stockdata.historic_data['Rolling Mean'].iloc[-1] + 3 * self.stockdata.historic_data['Rolling Std'].iloc[-1]
            self.leave_threshold_lower = self.stockdata.historic_data['Rolling Mean'].iloc[-1] + 1 * self.stockdata.historic_data['Rolling Std'].iloc[-1]

            # Log
            self.logger.info('Short\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}\t| Enter Short position - Threshold Upp: {:.2f} Low:{:.2f}'
                                 ' - Balance: {:.2f}'.format(price,self.stockdata.historic_data['Upper BB'].iloc[-1],
                                                             self.stockdata.historic_data['Lower BB'].iloc[-1],
                                                             self.current_stocks,
                                                             self.leave_threshold_upper,self.leave_threshold_lower,
                                                             self.wallet.balance()))

    def leave_position(self):

        price = self.stockdata.historic_data['Price'].iloc[-1]

        if (price < self.leave_threshold_lower) or (price > self.leave_threshold_upper):

            # Long position
            if self.current_stocks > 0:

                # Cash the stocks
                self.wallet.deposit(self.current_stocks * price)

                # Reset the current stocks
                self.current_stocks = 0

                # Log
                self.logger.info('Leave\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}\t| Leave Long position - Threshold Upp: {:.2f} Low:{:.2f}'
                                 ' - Balance: {:.2f}'.format(price,self.stockdata.historic_data['Upper BB'].iloc[-1],
                                                             self.stockdata.historic_data['Lower BB'].iloc[-1],
                                                             self.current_stocks,
                                                             self.leave_threshold_upper,self.leave_threshold_lower,
                                                             self.wallet.balance()))

            # Short position
            elif self.current_stocks < 0:

                # Repay the stocks
                self.wallet.withdraw(-self.current_stocks * price)

                # Reset the current stocks
                self.current_stocks = 0

                # Log
                self.logger.info('Leave\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}\t| Leave Short position - Threshold Upp: {:.2f} Low:{:.2f}'
                                 ' - Balance: {:.2f}'.format(price,self.stockdata.historic_data['Upper BB'].iloc[-1],
                                                             self.stockdata.historic_data['Lower BB'].iloc[-1],
                                                             self.current_stocks,
                                                             self.leave_threshold_upper,self.leave_threshold_lower,
                                                             self.wallet.balance()))

            # No position
            else:
                self.logger.info('Wait\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}'.format(price, self.stockdata.historic_data['Upper BB'].iloc[-1],
                                                                                        self.stockdata.historic_data['Lower BB'].iloc[-1],
                                                                                        self.current_stocks))

        #No position
        else:
            self.logger.info('Wait\t{:.2f}\t{:.2f}\t{:.2f} - Shares: {:5.0f}'.format(price, self.stockdata.historic_data['Upper BB'].iloc[-1],
                                                                                    self.stockdata.historic_data['Lower BB'].iloc[-1],
                                                                                    self.current_stocks))



class Wallet(object):

    BUDGET = 10000

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
        self.logger.info('Withdraw:\t{:.2f}\t\tBalance:\t{:.2f}'.format(amount,self.money))
        return amount

    def deposit(self, amount):
        self.money = self.money + amount
        self.logger.info('Deposit:\t{:.2f}\t\tBalance:\t{:.2f}'.format(amount,self.money))
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