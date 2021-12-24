# required packages 
import ccxt
import pandas as pd
from datetime import datetime

# fetching the data using ccxt
class GET_DATA:

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