import yfinance as yf
import pandas as pd

ticker = 'GOOGL'

# Download historical data
data = yf.download(ticker, period='1y', interval='1d')

# Print the first few rows of the data
print(data.head(5))

info = yf.Ticker(ticker)
print(list(filter(lambda s: not s.startswith("_"), dir(info))))
print()
for x in info.news:
    print(x, end='\n')