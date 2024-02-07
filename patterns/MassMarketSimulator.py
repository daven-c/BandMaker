from MarketSimulator import simulate_trading
from TestingUtils import *
from patterns import *
import random

if __name__ == '__main__':
    pattern_matchers: List[PatternMatcher] = [eval(pattern)() for pattern in PatternMatcher.SUBCLASSES]  # Choose pattern to be tested
    
    ticker_list = list(map(lambda line: line.strip(), open("tickers.txt").readlines()))
    tickers = ['cdw', 'shop', 'dpz', 'bap', 'icl', 'tru', 'erf', 'edu', 'aos', 'vtrs', 'podd', 'l', 'pag', 'ap', 'fts', 'glpi', 'docn', 'on', 'phi']  #  random.choices(ticker_list, k=20)
    for ticker in tickers:
        info = yf.Ticker(ticker)
        data = info.history(period='1y', interval='1d')
        if len(data) == 0:
            print("Ticker not found")
            continue

        result = simulate_trading(pattern_matchers, data, starting_cash=1000, buy_ratio=.4, sell_ratio=1, print_trades=False)
        
        # Final balance
        print(ticker, result, get_annual_increase(ticker))
        

