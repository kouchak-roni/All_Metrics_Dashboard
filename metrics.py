import pandas as pd
from scipy.stats import pearsonr
from math import sqrt


# The Scaff Trend Cycle
class STC:

	def __init__(self, data):
		self.data = data


	def sma(self, period):  # Calculating Simple Moving Average of Particular Period
		close_list = list(self.data['Close'])
		sma_list = []
		while(len(close_list) >= period):
			sma_data = close_list[ : period]
			close = sum(sma_data)/period
			close_list.pop(0)
			sma_list.append(close)
		return(sma_list)
	
	def ema(self, period): # Calculating Exponential Moving Average of Particular Period
		close_list = list(self.data['Close'])
		ema_list = [close_list[0]]
		count_ema = 0
		smoothing_constant = 2/(period + 1)
		another_close_list = list(self.data['Close'])
		while(len(close_list) - 1 > 0):
			elem = (another_close_list[count_ema + 1] - ema_list[count_ema])*smoothing_constant + ema_list[count_ema]
			ema_list.append(elem)
			count_ema += 1
			close_list.pop(0)
		return(ema_list)

	def macd(self, ema_1, ema_2): # moving average convergence divergence
		len_diff = len(ema_1) - len(ema_2)
		ema_list = ema_1[len_diff:]
		macd_list = []
		for i in range(len(ema_2)):
			macd_list.append(ema_list[i] - ema_2[i])
		return(macd_list)


	def stc(self, macd_list): # Calculating the Scaff Trend Cycle
		out_list = []
		macd_min = min(macd_list)
		macd_max = max(macd_list)
		for i in macd_list:
			out = (i - macd_min)/(macd_max - macd_min)
			out_list.append(out*100)
		return(out_list)


# The Flashing Indicator
class Flashing_Indicator:

	def __init__(self, data):
		self.data = data

	def autocorrelation(self, period): # Calculating Autocorrealation for a Particular Period
		close_list = list(self.data.Close)
		parallel_list = list(self.data.Close)[:-1]
		n = len(close_list)
		autocorrelation_list = []
		while(len(parallel_list) != 2):
			shift_list_len = len(close_list) - len(parallel_list)
			corr = corr = pearsonr(close_list[shift_list_len:], parallel_list)
			autocorrelation_list.append(corr[0])
			parallel_list.pop(0)
		diff_len = len(self.data.index) - len(autocorrelation_list)
		index_list = list(self.data.Date)[diff_len:]
		out = {'Date': [], 'Corr_Value': []}
		for i in range(len(autocorrelation_list)):
			if (i + diff_len)%period == 0:
				out['Date'].append(index_list[i])
				out['Corr_Value'].append(autocorrelation_list[i])
		out_df = pd.DataFrame(out)
		return((autocorrelation_list, out_df))

	def roc(self, period): # Calculating Rate of Change for a Particular Period
		close_list = list(self.data.Close)
		roc_list = []
		n = len(close_list)
		for i in range(n-period):
			roc = (close_list[i + period] - close_list[i])/close_list[i]
			roc_list.append(roc*100)
		return(roc_list)

	def ma(self, period): # Calculating Moving Average(Simple Moving Average) for a Particular Period
		close_list = list(self.data.Close)
		ma_list = []
		while(len(close_list) >= period):
			ma_data = close_list[ : period]
			close = sum(ma_data)/period
			close_list.pop(0)
			ma_list.append(close)
		return(ma_list)
	
	def bollinger_bands(self, ma_list, constant): # Getting the Bollinger Bands 
		lower_band_list = []
		upper_band_list = []
		close_list = list(self.data.Close)
		n = len(close_list) - len(ma_list)
		std = 0
		for i in range(len(ma_list)):
			std += (close_list[n+i] - ma_list[i])**2
		std = sqrt(std/n) 
		for i in ma_list:
			lower_band_list.append(i - constant*std)
			upper_band_list.append(i + constant*std)
		out = (lower_band_list, upper_band_list)
		return(out)

	
