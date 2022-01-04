from get_data import GET_DATA_CCXT, GET_DATA_SAN
from dashboard_metrics import dashboard_gapo, dashboard_stc, dashboard_flashing_indicator, dashboard_dbsi
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


# plot for GAPO Index or GRI
class plot_gapo:

	def __init__(self, coin, timeframe, period):
		self.coin = coin
		self.timeframe = timeframe
		self.period = period

	def plot_gapo(self):
		data_object = GET_DATA_CCXT(self.coin, self.timeframe) 
		data = data_object.get_data()
		plot_data = data_object.get_data()
		gapo_object = dashboard_gapo(data, self.period)
		gapo_list = gapo_object.calculate_gapo()
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		fig.add_candlestick(x = plot_data['Date'], open = plot_data['Open'], high = plot_data['High'], low = plot_data['Low'], close = plot_data['Close'], secondary_y = False, name = "Price candles")
		plot_data_date = list(plot_data['Date'])[:(1 - self.period)]
		fig.add_trace(go.Scatter(x = plot_data_date, y = gapo_list, opacity = 0.2, name = f'GAPO', line_color = 'blue'), secondary_y = True)
		return(fig)



# plot for The Scaff Trend Cycle
class plot_stc:

	def __init__(self, coin, timeframe, short_term_period, long_term_period):

		self.coin = coin
		self.timeframe = timeframe
		self.short_term_period = short_term_period
		self.long_term_period = long_term_period

	def plot_stc(self):
		data_object = GET_DATA_CCXT(self.coin, self.timeframe) 
		data = data_object.get_data()
		scaff_trend_object = dashboard_stc(data, self.short_term_period, self.long_term_period)
		scaff_tuple = scaff_trend_object.calculate_stc()
		out = scaff_tuple[0]
		another_out = scaff_tuple[1]
		fig1 = px.line(out.STC)
		fig1.update_traces(line_color = 'red')
		fig2 = px.line(another_out.Coin_Close_Price)
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		fig.add_trace(fig1.data[0], secondary_y=False)
		fig.add_trace(fig2.data[0], secondary_y=True)
		return(fig)

# plot for The Flashing Indicator
class plot_flashing_indicator:

	def __init__(self, coin, timeframe, autocorrelation_period, bollinger_band_constant, ma_constant, roc_period, correlation):

		self.coin = coin
		self.timeframe = timeframe
		self.autocorrelation_period = autocorrelation_period
		self.bollinger_band_constant = bollinger_band_constant
		self.ma_constant = ma_constant
		self.roc_period = roc_period
		self.correlation = correlation

	def plot_flashing_indicator(self):
		data_object = GET_DATA_CCXT(self.coin, self.timeframe) 
		data = data_object.get_data()
		flashing_indicator_object = dashboard_flashing_indicator(data, self.autocorrelation_period, self.ma_constant, self.roc_period, self.bollinger_band_constant)
		flashing_indicator_tuple = flashing_indicator_object.calculate_flashing_indicator(self.correlation)
		final_df = flashing_indicator_tuple[0]
		another_date_list = flashing_indicator_tuple[1]
		another_roc_list = flashing_indicator_tuple[2]
		fig1 = px.line(final_df['Upper Band'])
		fig1.update_traces(line_color = 'red')
		fig2 = px.line(final_df['Lower Band'])
		fig2.update_traces(line_color = 'green')
		fig3 = px.line(final_df['ROC'])
		fig3.update_traces(line_color = 'black')
		fig = make_subplots(specs = [[{"secondary_y": True}]])
		fig.add_trace(fig1.data[0], secondary_y = True)
		fig.add_trace(fig2.data[0], secondary_y = True)
		fig.add_trace(fig3.data[0], secondary_y = False)
		fig.add_trace(go.Scatter(
        	x = another_date_list,
        	y = another_roc_list,
        	name = 'Autocorrelation > ' + str(self.correlation),
        	mode = 'markers',
        	marker = dict(symbol = '1')))

		return(fig)

class plot_dbsi:

	def __init__(self, coin, timeframe, start_date):
		self.coin = coin
		self.timeframe = timeframe 
		self.start_date = start_date

	def plot_dbsi(self, selective_signals = True, remove_consecutive_signals = True):
		data_object = GET_DATA_SAN(self.coin, self.timeframe, self.start_date)
		data = data_object.get_data()
		dbsi_object = dashboard_dbsi(data)
		dbsi = dbsi_object.calculate_dbsi()
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		fig.add_candlestick(x = dbsi['datetime'], open = dbsi['open'], high = dbsi['high'], low = dbsi['low'], close = dbsi['close'], secondary_y = False, name = "Price candles")
		# plotting bull and bear percentages
		fig.add_trace(go.Scatter(x = dbsi['datetime'], y = dbsi['bull_perc'], opacity = 0.1, name = f'Bull power percentage', line_color = 'green'), secondary_y = True)
		fig.add_trace(go.Scatter(x = dbsi['datetime'], y = dbsi['bear_perc'], opacity = 0.1, name = f'Bear power percentage', line_color='red'), secondary_y = True)
		if selective_signals:
			bulls_winning = dbsi['bull_perc'] > dbsi['bear_perc']
			bears_winning = dbsi['bear_perc'] > dbsi['bull_perc']
			buy_signals = dbsi.loc[dbsi['crossover'][dbsi['crossover'] & bulls_winning].index, 'datetime']
			sell_signals = dbsi.loc[dbsi['crossunder'][dbsi['crossunder'] & bears_winning].index, 'datetime']
		else:
			buy_signals = dbsi.loc[dbsi['crossover'][dbsi['crossover']].index, 'datetime']
			sell_signals = dbsi.loc[dbsi['crossunder'][dbsi['crossunder']].index, 'datetime']
		if remove_consecutive_signals:
			if len(sell_signals) + len(buy_signals) > 0:
				all_signals = [(1, s) for s in buy_signals] + [(0, s) for s in sell_signals]
				all_signals = sorted(all_signals, key=lambda x: x[1])
				all_signals = [all_signals[0]] + [s for s, last_s in zip(all_signals[1:], all_signals[:-1]) if s[0] != last_s[0]]
				buy_signals = [s[1] for s in all_signals if s[0] == 1]
				sell_signals = [s[1] for s in all_signals if s[0] == 0]

        # plotting buy/sell signals
		for bs in buy_signals:
			fig.add_vline(x = bs, line_color = 'green', opacity = 0.5, exclude_empty_subplots = False)
		for ss in sell_signals:
			fig.add_vline(x = ss, line_color = 'red', opacity = 0.5, exclude_empty_subplots = False)

        # setting titles
		fig.update_yaxes(title_text = "Price in USD", secondary_y = False, showgrid = False)
		fig.update_yaxes(title_text = "Bull/Bear power percentage", secondary_y = True, showgrid = False)
		return(fig)




