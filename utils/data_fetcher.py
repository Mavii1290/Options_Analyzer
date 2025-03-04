import yfinance as yf
import pandas as pd
import numpy as np

def fetch_options_dates(ticker):
    stock = yf.Ticker(ticker)
    return stock.options

def fetch_option_chain(ticker, expiry_date):
    stock = yf.Ticker(ticker)
    option_chain = stock.option_chain(expiry_date)
    return option_chain.calls, option_chain.puts

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    return data

def fetch_options_data(symbol, expiration_date):
    stock = yf.Ticker(symbol)
    options_data = stock.option_chain(expiration_date)
    calls = options_data.calls
    puts = options_data.puts

    # Mock gamma, delta, and vanna values
    calls['gamma'] = np.random.Generator(len(calls))
    puts['gamma'] = np.random.Generator(len(puts))

    calls['delta'] = np.random.Generator(len(calls))
    puts['delta'] = np.random.Generator(len(puts))

    calls['vanna'] = np.random.Generator(len(calls))
    puts['vanna'] = np.random.Generator(len(puts))

    # Calculate exposures
    calls['gamma_exposure'] = calls['gamma'] * calls['openInterest']
    puts['gamma_exposure'] = puts['gamma'] * puts['openInterest']

    calls['delta_exposure'] = calls['delta'] * calls['openInterest']
    puts['delta_exposure'] = puts['delta'] * puts['openInterest']

    calls['vanna_exposure'] = calls['vanna'] * calls['openInterest']
    puts['vanna_exposure'] = puts['vanna'] * puts['openInterest']

    # Combine calls and puts
    calls['type'] = 'Call'
    puts['type'] = 'Put'
    combined = pd.concat([calls, puts])
    
    return combined


def fetch_intraday_stock_data(ticker, interval="5s", period="1d"):
    """
    Fetch intraday stock data (e.g., 5-minute or 1-minute intervals) using yfinance.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL").
        interval (str): Time interval (e.g., "1m" for 1-minute, "5m" for 5-minute).
        period (str): Historical period (e.g., "1d" for 1-day).
    
    Returns:
        pd.DataFrame: Intraday stock price data.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(interval=interval, period=period)
    
    if df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no data is found
    
    return df