# utils/indicators.py
import talib
import yfinance as yf

def calculate_technical_indicators(ticker):
    """
    Fetches stock data for the last 200 days and calculates the following technical indicators:
    - RSI (Relative Strength Index)
    - 50-day Moving Average
    - 200-day Moving Average
    - Delta (Placeholder value, could be implemented based on options data)
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period="200d")

    # Calculate RSI (14-day)
    rsi = talib.RSI(data['Close'], timeperiod=14).iloc[-1]

    # Calculate Moving Averages (50-day and 200-day)
    ma50 = data['Close'].rolling(window=50).mean().iloc[-1]
    ma200 = data['Close'].rolling(window=200).mean().iloc[-1]

    # Delta Placeholder: This can be calculated from options data (you may need to extend this)
    delta = 0.45  # Placeholder delta value for now (can be replaced with actual delta calculation)

    return delta, rsi, ma50, ma200
