import streamlit as st
from utils.data_fetcher import fetch_options_dates, fetch_option_chain, fetch_stock_data,fetch_options_data
from utils.plotters import create_oi_volume_charts, create_treemap, create_donut_chart,create_bar_chart
from utils.data_transformer import transform_options_df, reorder_and_round
from utils.indicators import calculate_technical_indicators
import yfinance as yf

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

    # Fetch & calculate technical indicators
    delta, rsi, ma50, ma200 = calculate_technical_indicators(ticker)
    prev_delta = delta - 0.1  # Placeholder for delta change
    delta_arrow = "↑" if delta > prev_delta else "↓" if delta < prev_delta else "→"

    prev_rsi = rsi - 0.5  # Placeholder for RSI change
    rsi_arrow = "↑" if rsi > prev_rsi else "↓" if rsi < prev_rsi else "→"

    prev_ma50 = ma50 - 0.2  # Placeholder for MA change
    ma50_arrow = "↑" if ma50 > prev_ma50 else "↓" if ma50 < prev_ma50 else "→"

    prev_ma200 = ma200 - 0.3  # Placeholder for MA change
    ma200_arrow = "↑" if ma200 > prev_ma200 else "↓" if ma200 < prev_ma200 else "→"

    # Display all metrics in a single row using columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f} {price_arrow}")

    with col2:
        st.metric("Volume", f"{volume:,}", f"{volume_change:,} {volume_arrow}")

    with col3:
        st.metric("Delta", f"{delta:.2f}", f"{delta - prev_delta:.2f} {delta_arrow}")

    with col4:
        st.metric("RSI", f"{rsi:.2f}", f"{rsi - prev_rsi:.2f} {rsi_arrow}")

    with col5:
        st.metric("50-day MA", f"${ma50:.2f}", f"{ma50 - prev_ma50:.2f} {ma50_arrow}")

    with col6:
        st.metric("200-day MA", f"${ma200:.2f}", f"{ma200 - prev_ma200:.2f} {ma200_arrow}")

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

        # Display Top 10 calls/puts sorted by volume
        calls_sorted = transform_options_df(calls).sort_values(by='volume', ascending=False).head(10)
        puts_sorted = transform_options_df(puts).sort_values(by='volume', ascending=False).head(10)

        st.write("### Top 10 Calls by Volume")
        st.write(calls_sorted)
        st.write("### Top 10 Puts by Volume")
        st.write(puts_sorted)


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

    # Fetch & calculate technical indicators
    delta, rsi, ma50, ma200 = calculate_technical_indicators(ticker)
    prev_delta = delta - 0.1  # Placeholder for delta change
    delta_arrow = "↑" if delta > prev_delta else "↓" if delta < prev_delta else "→"

    prev_rsi = rsi - 0.5  # Placeholder for RSI change
    rsi_arrow = "↑" if rsi > prev_rsi else "↓" if rsi < prev_rsi else "→"

    prev_ma50 = ma50 - 0.2  # Placeholder for MA change
    ma50_arrow = "↑" if ma50 > prev_ma50 else "↓" if ma50 < prev_ma50 else "→"

    prev_ma200 = ma200 - 0.3  # Placeholder for MA change
    ma200_arrow = "↑" if ma200 > prev_ma200 else "↓" if ma200 < prev_ma200 else "→"

    # Display all metrics in a single row using columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f} {price_arrow}")

    with col2:
        st.metric("Volume", f"{volume:,}", f"{volume_change:,} {volume_arrow}")

    with col3:
        st.metric("Delta", f"{delta:.2f}", f"{delta - prev_delta:.2f} {delta_arrow}")

    with col4:
        st.metric("RSI", f"{rsi:.2f}", f"{rsi - prev_rsi:.2f} {rsi_arrow}")

    with col5:
        st.metric("50-day MA", f"${ma50:.2f}", f"{ma50 - prev_ma50:.2f} {ma50_arrow}")

    with col6:
        st.metric("200-day MA", f"${ma200:.2f}", f"{ma200 - prev_ma200:.2f} {ma200_arrow}")


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