def get_random_ticker() -> str:
    ticker = ''
    data = []
    while len(data) == 0:
        ticker = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(random.randint(3, 5)))
        info = yf.Ticker(ticker)
        data = info.history(period='1y', interval='1d')
    return ticker


def get_patterns(matcher: PatternMatcher, data: pd.DataFrame):
    patterns_found = matcher.process(data)
    return patterns_found
