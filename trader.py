import logging

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