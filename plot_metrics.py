from get_data import GET_DATA
from dashboard_metrics import dashboard_stc, dashboard_flashing_indicator
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


# plot for The Scaff Trend Cycle
class plot_stc:

	def __init__(self, coin, timeframe, short_term_period, long_term_period):

		self.coin = coin
		self.timeframe = timeframe
		self.short_term_period = short_term_period
		self.long_term_period = long_term_period

	def plot_stc(self):
		data_object = GET_DATA(self.coin, self.timeframe) 
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
		data_object = GET_DATA(self.coin, self.timeframe) 
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









