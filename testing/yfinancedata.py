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
import pandas as pd
import matplotlib.pyplot as plt

# Generate some example data (you can replace this with your own dataset)
data = {'Date': pd.date_range(start='2022-01-01', periods=50),
        'Close': [100, 105, 110, 95, 105, 115, 120, 125, 110, 105,
                  100, 95, 105, 110, 115, 120, 125, 130, 125, 120,
                  115, 110, 105, 100, 95, 105, 110, 115, 120, 125,
                  130, 125, 120, 115, 110, 105, 100, 95, 105, 110,
                  115, 120, 125, 130, 125, 120, 115, 110, 105, 100],
        'Day': range(1, 51)}


df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

# Calculate the moving average (let's use a 10-day moving average as an example)
ma_window = 10
df['MA'] = df['Close'].rolling(window=ma_window).mean()




# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Close'], label='Closing Price', color='blue')
plt.plot(df.index, df['MA'], label=f'{ma_window}-day Moving Average', color='red')

plt.title('Stock Price with Moving Average')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
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