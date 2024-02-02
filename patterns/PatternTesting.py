import plotly.graph_objects as go
import yfinance as yf
from patterns import *
import pandas as pd


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


def visualize_patterns(ticker: str, pattern_matcher: PatternMatcher, save: bool = False):
    info = yf.Ticker(ticker)

    data = info.history(period='1y', interval='1d')

    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'],
                    close=data['Close'], high=data['High'], low=data['Low'])])
    fig.update_layout(
        title_text=f"{ticker} - {pattern_matcher.type}")

    patterns = get_patterns(pattern_matcher, data)
    print(f"{len(patterns)} patterns found in {len(data)} candles")
    annotate_patterns(fig, patterns)

    fig.show()


if __name__ == '__main__':
    ticker = 'AAPL'
    pattern_matcher: PatternMatcher = Tweezer(
        max_short_wick_length=0.01, difference_threshold=0.01)
    visualize_patterns(ticker, pattern_matcher)
