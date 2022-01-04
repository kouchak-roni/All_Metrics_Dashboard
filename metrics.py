import pandas as pd
from scipy.stats import pearsonr
from math import sqrt, log
import numpy as np


# Gopalkrishnan Range Index
class GAPO:

	def __init__(self, data):
		self.data = data

	def create_df_list(self, period):
		df_list = []
		while(len(self.data) >= period):
			df_list.append(self.data.head(period))
			self.data.drop(self.data.index[0], axis = 0, inplace = True)
		return(df_list)

	def calculate_gapo(self, list_df, period):
		min_max_diff_list = []
		for i in list_df:
			min_max_diff_list.append(max(i['High']) - min(i['Low']))
			out_list = [log(i)/log(period) for i in min_max_diff_list]
		return(out_list)


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

class DBSI:

	def __init__(self, data):
		self.data = data 

	def dbsi_indicator(self, standard_length = 13, smoothing_length = 1, total_power_fast_l = 3, total_power_slow_l = 12):
		average_price = self.data['close'].ewm(2/(standard_length+1)).mean()
		bull_power_raw = self.data['high'] - average_price
		bear_power_raw = self.data['low'] - average_price


		bull_power = bull_power_raw.ewm(2/(smoothing_length + 1)).mean()
		bear_power = bear_power_raw.ewm(2/(smoothing_length + 1)).mean()
		total_power_raw = bull_power + bear_power

		bulls_dominating = (self.data['high'] >= average_price) & (self.data['low'] >= average_price)
		bears_dominating = (self.data['high'] <= average_price) & (self.data['low'] <= average_price)
		bears_bulls_fighting = (self.data['high'] >= average_price) & (self.data['low'] <= average_price)

		bull_power_absolute = bull_power_raw.abs().ewm(2/(smoothing_length + 1)).mean()
		bear_power_absolute = bear_power_raw.abs().ewm(2/(smoothing_length + 1)).mean()
		bull_power_percent = np.round(100*bull_power_absolute / (bull_power_absolute + bear_power_absolute))
		bear_power_percent = 100 - bull_power_percent

		total_power_fast = total_power_raw.ewm(2/(total_power_fast_l + 1)).mean()
		total_power_slow = total_power_raw.ewm(2/(total_power_slow_l + 1)).mean()

		crossover_fast_slow = (total_power_fast > total_power_slow) & (total_power_fast.shift(1) < total_power_slow.shift(1))
		crossunder_fast_slow = (total_power_fast < total_power_slow) & (total_power_fast.shift(1) > total_power_slow.shift(1))

		bulls_winning = bull_power_percent >= 50
		bears_winning = bear_power_percent >= 50

		bulls_take_over = bulls_dominating & ~bulls_dominating.shift(1).astype(bool)
		bears_take_over = bears_dominating & ~bears_dominating.shift(1).astype(bool)

		out = pd.DataFrame({'bull_perc': bull_power_percent, 'bear_perc': bear_power_percent,
                         'crossover': crossover_fast_slow, 'crossunder': crossunder_fast_slow,
                         'bulls_dominance': bulls_dominating, 'bears_dominance': bears_dominating})
		return(out)


