import streamlit as st
from utils.data_fetcher import fetch_options_dates, fetch_option_chain, fetch_stock_data,fetch_options_data
from utils.plotters import create_oi_volume_charts, create_treemap, create_donut_chart,create_bar_chart
from utils.data_transformer import transform_options_df, reorder_and_round

import yfinance as yf
import pandas as pd

# Set page layout and title
st.set_page_config(layout="wide")
st.title("Real-Time Stock Options Data")

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Options Data", "Gamma Exposure"])

if page == "Options Data":
    # Arrange ticker, expiry date, and color selections in a single row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        ticker = st.text_input("Ticker", value="AAPL")

    with col2:
        selected_expiries = st.multiselect("Expiry Date(s)", options=fetch_options_dates(ticker), default=[fetch_options_dates(ticker)[0]])

    with col3:
        discrete_palette = st.selectbox("Discrete Palette", ["Plotly", "Pastel", "Dark2"], index=0)

    with col4:
        continuous_scale = st.selectbox("Continuous Scale", ["Hot", "Reds", "Viridis"], index=0)

    # Fetch stock data
    stock_data = fetch_stock_data(ticker)

    # Get current & previous day's values
    current_price = stock_data['Close'][0]
    prev_price = stock_data['Close'][1] if len(stock_data) > 1 else current_price
    price_change = current_price - prev_price
    price_arrow = "↑" if price_change > 0 else "↓" if price_change < 0 else "→"

    volume = stock_data['Volume'][0]
    prev_volume = stock_data['Volume'][1] if len(stock_data) > 1 else volume
    volume_change = volume - prev_volume
    volume_arrow = "↑" if volume_change > 0 else "↓" if volume_change < 0 else "→"

   

    if selected_expiries:
        expiry_date = selected_expiries[0]  # Assuming user selects a date
        calls, puts = fetch_option_chain(ticker, expiry_date)

        # Further processing and visualization
        call_vol_sum = calls['volume'].sum()
        put_vol_sum = puts['volume'].sum()

        donut_fig = create_donut_chart(call_vol_sum, put_vol_sum, discrete_palette)
        treemap_fig = create_treemap(calls, puts, continuous_scale, expiry_date)

        colA, colB = st.columns(2)
        with colA:
            st.plotly_chart(donut_fig, use_container_width=True, key="volume_ratio_donut")
        with colB:
            st.plotly_chart(treemap_fig, use_container_width=True, key="treemap")

        # Bar charts for OI & Volume
        fig_oi, fig_volume = create_oi_volume_charts(calls, puts, discrete_palette)
        st.plotly_chart(fig_oi, use_container_width=True, key="oi_chart")
        st.plotly_chart(fig_volume, use_container_width=True, key="vol_chart")

        calls["Type"] = "Call"
        puts["Type"] = "Put"
        combined_options = pd.concat([calls, puts]).sort_values(by="volume", ascending=False).head(20)
        combined_options = transform_options_df(combined_options)

        st.write("### Top 20 Options (Calls & Puts) by Volume")
        st.dataframe(combined_options)


if page == "Gamma Exposure":
    # Arrange ticker, expiry date, and color selections in a single row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        ticker = st.text_input("Ticker", value="AAPL")

    with col2:
        selected_expiries = st.multiselect("Expiry Date(s)", options=fetch_options_dates(ticker), default=[fetch_options_dates(ticker)[0]])

    with col3:
        discrete_palette = st.selectbox("Discrete Palette", ["Plotly", "Pastel", "Dark2"], index=0)

    with col4:
        continuous_scale = st.selectbox("Continuous Scale", ["Hot", "Reds", "Viridis"], index=0)

    # Fetch stock data
    stock_data = fetch_stock_data(ticker)

    # Get current & previous day's values
    current_price = stock_data['Close'][0]
    prev_price = stock_data['Close'][1] if len(stock_data) > 1 else current_price
    price_change = current_price - prev_price
    price_arrow = "↑" if price_change > 0 else "↓" if price_change < 0 else "→"

    volume = stock_data['Volume'][0]
    prev_volume = stock_data['Volume'][1] if len(stock_data) > 1 else volume
    volume_change = volume - prev_volume
    volume_arrow = "↑" if volume_change > 0 else "↓" if volume_change < 0 else "→"

   


    symbol = ticker
    stock = yf.Ticker(symbol)
    expiration_dates = stock.options

    # Multi-select for expiration dates
  

    if selected_expiries:
        for expiration_date in selected_expiries:
            combined = fetch_options_data(symbol, expiration_date)

            # Create and display bar charts
            fig_gamma = create_bar_chart(combined, 'gamma_exposure', f'Gamma Exposure for {symbol} Options Expiring on {expiration_date}')
            fig_delta = create_bar_chart(combined, 'delta_exposure', f'Delta Exposure for {symbol} Options Expiring on {expiration_date}')
            fig_vanna = create_bar_chart(combined, 'vanna_exposure', f'Vanna Exposure for {symbol} Options Expiring on {expiration_date}')

            st.plotly_chart(fig_gamma)
            st.plotly_chart(fig_delta)
            st.plotly_chart(fig_vanna)
    else:
        st.write("Please select at least one expiration date.")