import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

ticker = 'TENB'

info = yf.Ticker(ticker)
print(list(filter(lambda s: not s.startswith("_"), dir(info))))
print()

data = info.history(period='1y', interval='1d')


fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], close=data['Close'], high=data['High'], low=data['Low'])])

fig.show()

# Save the figure as a PNG file
fig.write_image("candlestick_chart.png")