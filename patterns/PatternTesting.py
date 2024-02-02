import plotly.graph_objects as go
import yfinance as yf
from patterns import *
import pandas as pd


def get_patterns(matcher: PatternMatcher, data: pd.Dataframe, *args, **kwargs):
    matcher = matcher(*args, **kwargs)
    patterns_found = matcher.process(data)
    return patterns_found


def annotate_patterns(fig, patterns):
    ...


ticker = 'AAPL'
pattern_matcher = ShootingStar

info = yf.Ticker(ticker)

data = info.history(period='1y', interval='1d')
print(data)

fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'],
                close=data['Close'], high=data['High'], low=data['Low'])])

patterns = get_patterns(ShootingStar, data)
annotate_patterns(fig, patterns)

fig.show()
