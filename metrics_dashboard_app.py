# Required Packages
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plot_metrics import plot_stc, plot_flashing_indicator

# Configuration of Webpage
st.set_page_config(page_title = 'Metrics Dashboard', layout = 'wide')
# Coins to Get Data for
coin_symbol_dict = {
	'Bitcoin': 'BTC/USDT',
	'Ethereum': 'ETH/USDT',
	'Binance Coin': 'BNB/USDT'
	}

coin = st.sidebar.selectbox('Select Coin', coin_symbol_dict.keys()) # selecting the coin
time_frame = st.sidebar.selectbox('Select Timeframe', ['1d', '4h', '1h']) # selecting time frame for data
metric = st.sidebar.selectbox('Select the Metric', ['The Scaff Trend Cycle', 'The Flashing Indicator']) # selecting the metric name
# The Scaff Trend Cycle
if metric == 'The Scaff Trend Cycle':
	# inputs for the metric
	short_term_period = st.sidebar.text_input('Write the Short-Term Period to Calculate MACD') 
	long_term_period = st.sidebar.text_input('Write the Long-Term Period to Calculate MACD')
	input_title = st.sidebar.text_input('Enter a Title for your plot')
	button = st.sidebar.button('Click Here to Get the Plot for The Scaff Trend') # Creating button
	if button:
		short_term_period = int(short_term_period)
		long_term_period = int(long_term_period)
		# Customizing the plot title
		if input_title == '':
			title = 'Schaff Trend Cycle Plot for ' + coin + ' for timeframe ' + time_frame
		else:
			title = input_title
		# Creating the plot
		plot_object = plot_stc(coin_symbol_dict[coin], time_frame, short_term_period, long_term_period)
		fig = plot_object.plot_stc()
		fig.update_layout(title = title, width = 1200, height = 600)
		st.plotly_chart(fig)
		st.download_button('Click here to download the Interactive Chart', fig.to_html(), title + '.html')
	else:
		st.write('Please enter the proper values and click on the button below to get your required plot')

# The Flashing Indicator
if metric == 'The Flashing Indicator':
	# inputs for the metric
	autocorrelation_period = st.sidebar.text_input('Write the period for Autocorrelation')
	bollinger_band_constant = st.sidebar.text_input('Write the constant for Bollinger Bands')
	ma_constant = st.sidebar.text_input('Time Period for Moving Avarage')
	roc_period = st.sidebar.text_input('Time Period for ROC')
	correlation = st.sidebar.text_input('Value of the allowed Correlation')
	input_title = st.sidebar.text_input('Enter a Title for your plot')
	button = st.sidebar.button('Click Here to Get the Plot for The Flashing Indicator') # creating button
	if button:
		autocorrelation_period = int(autocorrelation_period)
		ma_constant = int(ma_constant)
		roc_period = int(roc_period)
		bollinger_band_constant = int(bollinger_band_constant)
		correlation = float(correlation)
		if input_title == '':
			title = 'The Flashing Indicator for the ' + coin + ' for timeframe ' + time_frame
		else:
			title = input_title
		# creating the plot
		plot_object = plot_flashing_indicator(coin_symbol_dict[coin], time_frame, autocorrelation_period, bollinger_band_constant, ma_constant, roc_period, correlation)
		fig = plot_object.plot_flashing_indicator()
		fig.update_layout(title = title, width = 1200, height = 600)
		st.plotly_chart(fig)
		st.download_button('Click here to download the Interactive Chart', fig.to_html(), title + '.html')
	else:
		st.write('Please enter the proper values and click on the button below to get your required plot')



