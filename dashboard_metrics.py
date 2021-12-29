from metrics import STC, Flashing_Indicator, DBSI
import pandas as pd

class dashboard_stc:

	def __init__(self, data, short_term_period, long_term_period):
		self.data = data
		self.short_term_period = short_term_period
		self.long_term_period = long_term_period

	def calculate_stc(self): # Getting outputs for required plot
		stc_object = STC(self.data) 
		date_list = list(self.data.Date) 
		close_list = list(self.data.Close)
		ema_list_1 = stc_object.ema(self.short_term_period)
		ema_list_2 = stc_object.ema(self.long_term_period)
		macd_list = stc_object.macd(ema_list_1, ema_list_2)
		stc_list = stc_object.stc(macd_list)
		out = pd.DataFrame({'STC' : stc_list}, index = date_list) 
		another_out = pd.DataFrame({'Coin_Close_Price' : close_list[self.long_term_period - 1:]}, index = date_list[self.long_term_period - 1:])
		return((out, another_out))

class dashboard_flashing_indicator:

	def __init__(self, data, autocorrelation_period, ma_constant, roc_period, bollinger_band_constant):
		self.data = data
		self.autocorrelation_period = autocorrelation_period
		self.ma_constant = ma_constant
		self.roc_period = roc_period
		self.bollinger_band_constant = bollinger_band_constant

	def calculate_flashing_indicator(self, correlation): # Getting outputs for required plot
		date_list = list(self.data.Date)
		close_list = list(self.data.Close)
		indicator_object = Flashing_Indicator(self.data)
		aut_corr_tuple = indicator_object.autocorrelation(self.autocorrelation_period)
		aut_corr_list = aut_corr_tuple[0]
		aut_corr_df = aut_corr_tuple[1]
		roc_list = indicator_object.roc(self.roc_period)
		ma_list = indicator_object.ma(self.ma_constant)
		bollinger_band = indicator_object.bollinger_bands(ma_list, self.bollinger_band_constant)
		if len(ma_list) > len(roc_list):
			diff = len(ma_list) - len(roc_list)
			corr_list_diff = len(aut_corr_list) - len(roc_list)		
			out = {'Lower Band': bollinger_band[0][diff:], 'Upper Band': bollinger_band[1][diff:], 'ROC': roc_list , 'Autocorrelation': aut_corr_list[corr_list_diff:]}
		else:
			diff = len(roc_list) - len(ma_list)
			corr_list_diff = len(aut_corr_list) - len(ma_list)	
			out = {'Lower Band': bollinger_band[0], 'Upper Band': bollinger_band[1], 'ROC': roc_list[diff:] , 'Autocorrelation': aut_corr_list[corr_list_diff:]}

		lag = len(date_list) - len(out['ROC'])
		final_df = pd.DataFrame(out, index = date_list[lag:])
		another_date_list = []
		another_roc_list = []
		multiple = 0
		if self.autocorrelation_period >= max(self.ma_constant, self.roc_period):
			aut_corr_df_final = aut_corr_df
		else:
			for i in range(1, 1000):
				if self.autocorrelation_period*i >= max(self.ma_constant, self.roc_period):
					multiple = i 
					break
			aut_corr_df_final = aut_corr_df.iloc[multiple:]
	
		for i in aut_corr_df_final.Date:
			if final_df.Autocorrelation[i] > correlation:
				another_date_list.append(i)
				another_roc_list.append(final_df.ROC[i])

		return((final_df, another_date_list, another_roc_list))


class dashboard_dbsi:

	def __init__(self, data):
		self.data = data 

	def calculate_dbsi(self):
		indicator_object = DBSI(self.data)
		indicator_df = indicator_object.dbsi_indicator()
		out = pd.concat((self.data, indicator_df), axis = 1)
		return(out)
