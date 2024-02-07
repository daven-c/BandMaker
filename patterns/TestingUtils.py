import random
import yfinance as yf

def get_random_ticker() -> str:
    ticker = ''
    data = []
    while len(data) == 0:
        ticker = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(random.randint(3, 5)))
        info = yf.Ticker(ticker)
        data = info.history(period='1y', interval='1d')
    return ticker

def get_annual_increase(ticker: str) -> float:
    info = yf.Ticker(ticker)
    data = info.history(period='1y', interval='1d')
    return round((data.iloc[-1].Close - data.iloc[0].Close) / data.iloc[0].Close * 100, 2)

if __name__ == '__main__':
    print(get_annual_increase("nvda"))