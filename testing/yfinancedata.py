import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# def signal_momentum_candle(df):
#     if df.Open.iloc[-1] < df.Open.iloc[-2] and df.Open.iloc[-1] < df.Close.iloc[-2] and df.Close.iloc[-1] > df.Open.iloc[-2] and df.Close.iloc[-1] > df.Close.iloc[-2]:#bullish
#         return 2
#     elif df.Open.iloc[-1] > df.Open.iloc[-2] and df.Open.iloc[-1] > df.Close.iloc[-2] and df.Close.iloc[-1] < df.Open.iloc[-2] and df.Close.iloc[-1] < df.Close.iloc[-2]:#bearish
#         return 1
#     return -1
    

#data = yf.download("AAPL", start="2023-12-23", interval="1d")   
try:
    stock_data = yf.Ticker("0")
    info = stock_data.info
    print(bool(info)) 
except Exception as e:
    print(f"An error occurred: {e}")
# data = data.tail(3) #getting most recent data
# signal = []
# candle_length = []
# candle_length.append(0)
# signal.append(0)

# # Add candle stick length column to data frame
# for i in range(1,len(data)):
#     candle_length.append(data.Open.iloc[i] - data.Close.iloc[i])
# data["candle_length"] = candle_length

# # Add signal column to data frame
# for i in range(1,len(data)):
#     df = data[i-1:i+1]
#     signal.append(signal_momentum_candle(df))
# data["signal"] = signal    

# print(data)

# chart = go.Candlestick(high=data["High"], low=data["Low"], close=data["Close"], open=data["Open"])
# fig = go.Figure(data=[chart])
# fig.show()