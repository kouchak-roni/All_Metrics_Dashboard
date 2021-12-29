# required packages 
import ccxt
import san
import pandas as pd
from datetime import datetime

# fetching the data using ccxt
class GET_DATA_CCXT:

	def __init__(self, symbol, timeframe):
		self.symbol = symbol
		self.timeframe = timeframe

	def get_data(self):
		exchange = ccxt.binance()
		candles = exchange.fetch_ohlcv(self.symbol, timeframe = self.timeframe, limit = 1000) # fetching Open, High, Low, Close data
		data = pd.DataFrame(candles, columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']) # creating dataframe
		date_list = []
		for i in data['Date']:
			date_list.append(datetime.fromtimestamp(i/1000)) # converting to unix time to readable datetime format
		data['Date'] = date_list
		return(data)

# fetching data using sanpy

class GET_DATA_SAN:

	def __init__(self, symbol, timeframe, start_date):
		self.symbol = symbol
		self.timeframe = timeframe
		self.start_date = start_date

	def get_data(self):
		ohlcv = san.get(f'ohlcv/{self.symbol}', from_date = self.start_date, interval = self.timeframe)
		ohlcv.columns = ["open", "close", "high", "low", "volume", "marketcap"]
		ohlcv.reset_index(inplace=True)
		return(ohlcv)
	