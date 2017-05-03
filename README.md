# Bollinger Band Trading Simultator
This project implements a trading simulator using a [Bollinger Band](http://www.investopedia.com/terms/b/bollingerbands.asp) strategy in intraday trading.
## The Trading Strategy
The strategy is a simple implementation.

Given a customizable time window, the trader compute six bollinger bands.
* Upper bollinger bands:
  * +3 times rolling standard deviations
  * +2 times rolling standard deviations
  * +1 times rolling standard deviations
* Lower bollinger bands:
  * -1 times rolling standard deviations
  * -2 times rolling standard deviations
  * -3 times rolling standard deviations

Then we can have three scenarios:
* The current price is between +2 and -2 rolling std dev:
  * The trader do nothing
* The current price is more than +2 rolling std dev:
  * The trader buys stocks equivalent to a 90% of the money in the wallet
  * The trader set two threshold to leave position when the future current price is
    * less than +1 rolling std dev
    * more than +3 rolling std dev
* The current price is less than -2 rolling std dev:
  * The trader short stocks equivalent to a 90% of the money in the wallet
  * The trader set two threshold to leave position when the future current price is
    * more than -1 rolling std dev
    * less than -3 rolling std dev

## How to run the simulator
1. Clone the repository in a local folder
2. Run the file `run.py`

## Changing the dataset

1. Open the `datamanager.py`
2. Go to `self.file_name = 'data/eni.csv'`
3. Change the csv filename

## Output

The output is stored in the log folder in two files `trader.py` and `wallet.py`.
* `trader.py` contains the log of the trader choices, position and datas
* `wallet.py` contains the log of the bank account where the money is stored

## Results

For the [ENI](https://finance.yahoo.com/quote/ENI.MI?ltr=1) one year intraday dataset we started with 10,000 EUR and we finished with 21,622 EUR, equivalent to a + 116%, not bad at all!

I invite everybody to download the repo and try with his preferred stocks.
