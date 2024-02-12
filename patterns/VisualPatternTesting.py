import plotly.graph_objects as go
import yfinance as yf
from patterns import *
import pandas as pd
import random
from typing import Tuple
from TestingUtils import *


def annotate_patterns(fig, patterns: Tuple[pd.Series, int], matcher: str = None):
    for pattern in patterns:
        fig.add_annotation(
            text=matcher[0:3].upper() if matcher is not None else 'o',
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


def visualize_patterns(data: pd.DataFrame, pattern_matchers: PatternMatcher, display: bool = True, save: bool = False):
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'],
                    close=data['Close'], high=data['High'], low=data['Low'])])

    total_patterns_found = 0
    for pattern in pattern_matchers:
        patterns_found = pattern.process(data)
        total_patterns_found += len(patterns_found)
        print(
            f"{pattern.type} - {len(patterns_found)} patterns found in {len(data)} candles")
        annotate_patterns(fig, patterns_found, pattern.type)

    fig.update_layout(
        title_text=f"{ticker} - {total_patterns_found} patterns(s) detected - {', '.join([pattern.type for pattern in pattern_matchers])}")

    if display:
        fig.show()
    if save:
        fig.write_image(f"{ticker} - {pattern.type}")


if __name__ == '__main__':
    tickers = ['crwd', 'on', 'nxe', 'googl', 'tenb']
    for ticker in tickers:
        pattern_matchers: List[PatternMatcher] = [
            eval(pattern)() for pattern in PatternMatcher.SUBCLASSES]

        info = yf.Ticker(ticker)
        data = info.history(period='1y', interval='1d')

        visualize_patterns(data, pattern_matchers)
