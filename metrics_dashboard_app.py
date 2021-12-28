# Required Packages
import streamlit as st
from get_data import GET_DATA
from dashboard_metrics import dashboard_stc, dashboard_flashing_indicator
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

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
		# getting the data for coin and timeframe
		data_object = GET_DATA(coin_symbol_dict[coin], time_frame) 
		data = data_object.get_data()
		short_term_period = int(short_term_period)
		long_term_period = int(long_term_period)
		scaff_trend_object = dashboard_stc(data, short_term_period, long_term_period) 
		scaff_tuple = scaff_trend_object.calculate_stc() # Calculating required output for the plot
		out = scaff_tuple[0]
		another_out = scaff_tuple[1]
		# Customizing the plot title
		if input_title == '':
			title = 'Schaff Trend Cycle Plot for ' + coin + ' for timeframe ' + time_frame
		else:
			title = input_title
		# Creating the plot
		fig1 = px.line(out.STC)
		fig1.update_traces(line_color = 'red')
		fig2 = px.line(another_out.Coin_Close_Price)
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		fig.add_trace(fig1.data[0], secondary_y=False)
		fig.add_trace(fig2.data[0], secondary_y=True)
		fig.update_layout(title = title, width = 1600, height = 800)
		st.plotly_chart(fig)
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
		# getting the data for coin and timeframe
		data_object = GET_DATA(coin_symbol_dict[coin], time_frame)
		data = data_object.get_data()
		autocorrelation_period = int(autocorrelation_period)
		ma_constant = int(ma_constant)
		roc_period = int(roc_period)
		bollinger_band_constant = int(bollinger_band_constant)
		correlation = float(correlation)
		flashing_indicator_object = dashboard_flashing_indicator(data, autocorrelation_period, ma_constant, roc_period, bollinger_band_constant)
		flashing_indicator_tuple = flashing_indicator_object.calculate_flashing_indicator(correlation) # getting the outputs for the plot
		final_df = flashing_indicator_tuple[0]
		another_date_list = flashing_indicator_tuple[1]
		another_roc_list = flashing_indicator_tuple[2]
		# customizing the plot title
		if input_title == '':
			title = 'The Flashing Indicator for the ' + coin + ' for timeframe ' + time_frame
		else:
			title = input_title
		# creating the plot
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
        	name = 'Autocorrelation > ' + str(correlation),
        	mode = 'markers',
        	marker = dict(symbol = '1'))) # This is to add Flash in the plot
		fig.update_layout(title = title, width = 1600, height = 800)
		st.plotly_chart(fig)
	else:
		st.write('Please enter the proper values and click on the button below to get your required plot')
