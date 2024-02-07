from MarketSimulator import simulate_trading
from TestingUtils import get_random_ticker
from patterns import *
import random

if __name__ == '__main__':
    pattern_matchers: List[PatternMatcher] = [eval(pattern)() for pattern in PatternMatcher.SUBCLASSES]  # Choose pattern to be tested
    
    results = []
    ticker_list = list(map(lambda line: line.strip(), open("tickers.txt").readlines()))
    tickers = random.choices(ticker_list, k=10)
    for ticker in tickers:
        info = yf.Ticker(ticker)
        data = info.history(period='1y', interval='1d')
        if len(data) == 0:
            print("Ticker not found")
            quit()

        result = simulate_trading(pattern_matchers, data, starting_cash=1000, buy_ratio=.2, sell_ratio=.3, print_trades=False)
        
        # Final balance
        results.append(result)

    for ticker, key in zip(tickers, results):
        print(ticker, key)
        
