import plotly.graph_objects as go
import yfinance as yf
from patterns import *
import pandas as pd
import random


def get_patterns(matcher: PatternMatcher, data: pd.DataFrame):
    patterns_found = matcher.process(data)
    return patterns_found


def annotate_patterns(fig, patterns: Tuple[pd.Series, int]):
    for pattern in patterns:
        fig.add_annotation(
            text=" ",
            # x-coordinate of the annotation (use any valid x-value)
            x=pattern[0].name,
            # y-coordinate of the annotation (use any valid y-value)
            y=pattern[0].High,
            align="center",
            showarrow=True,  # Display arrow pointing to the specified coordinates
            arrowhead=2,  # Arrowhead style
            arrowsize=1,  # Arrow size
            borderwidth=1,
            borderpad=1,
            bgcolor="#00ff00" if pattern[1] > 0 else "#ff0000",
        )


def visualize_patterns(data: pd.DataFrame, pattern_matcher: PatternMatcher, display: bool = True, save: bool = False):
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'],
                    close=data['Close'], high=data['High'], low=data['Low'])])

    patterns = get_patterns(pattern_matcher, data)
    print(f"{len(patterns)} patterns found in {len(data)} candles")
    fig.update_layout(
        title_text=f"{ticker} - {len(patterns)} {pattern_matcher.type}(s) detected")
    annotate_patterns(fig, patterns)

    if display:
        fig.show()
    if save:
        fig.write_image(f"{ticker} - {pattern_matcher.type}")


if __name__ == '__main__':
    ticker = ''  # Leave blank ('') if random ticker wanted
    pattern_matcher: PatternMatcher = Marubozu()
    data = []
    
    if ticker != '':
        info = yf.Ticker(ticker)
        data = info.history(period='1y', interval='1d')
        
    else:
        while len(data) == 0:
            ticker = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(random.randint(3, 5)))
            info = yf.Ticker(ticker)
            data = info.history(period='1y', interval='1d')
            if len(get_patterns(matcher=pattern_matcher, data=data)) < 30:
                data = []


    print(ticker)
    visualize_patterns(data, pattern_matcher)
    