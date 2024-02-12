import yfinance as yf
from patterns import *
import pandas as pd
from datetime import datetime, timedelta
import sys
from TestingUtils import *


def format_date(date, get_next_day: bool = False):
    dt_object = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z")
    if get_next_day:
        dt_object = dt_object + timedelta(days=1)
    formatted_date = dt_object.strftime("%m-%d-%y")
    return formatted_date


def simulate_trading(pattern_matchers: List[PatternMatcher], data: pd.DataFrame, starting_cash: int = 1000, buy_ratio: float = 1.0, sell_ratio: float = 1.0, print_trades: bool = False):

    current_cash = starting_cash
    shares = 0
    trades_made = 0

    if print_trades:
        print(
            f"{'Date':<15} {'Pattern':<15} {'Buy/Sell':<10} {'Shares':<10} {'Price':<10} {'Value':<10}")

    # Iterate up to the most recent day, sell all shares on the last day
    # Buy/Sell at the opening price of the next day, simulates placing orders overnight
    for day_idx in range(len(data) - 1):
        for pattern in pattern_matchers:
            if pattern.CANDLES_REQUIRED - 1 > day_idx:  # Checks if there are insufficient candles to use
                continue

            # Check if pattern can be detected from past day
            result = pattern.process(
                data=data.iloc[day_idx - pattern.CANDLES_REQUIRED + 1:day_idx + 1])
            if result != []:  # pattern found
                current_day = result[0][0]
                next_day_price = round(data.iloc[day_idx + 1].Open, 2)

                next_day_date = format_date(
                    current_day.name, get_next_day=True)

                if result[0][1] == 1:  # Bullish pattern found
                    # Buy the stock
                    # Allows change in purchasing strategy
                    shares_bought = round(
                        current_cash * buy_ratio / next_day_price, 2)
                    cost = shares_bought * next_day_price
                    shares += shares_bought
                    current_cash = current_cash - cost
                    trades_made += 1
                    if print_trades:
                        print(
                            f"\033[92m{next_day_date:<15} {pattern.type:<15} {'Buy':<10} {shares_bought:<10.2f} ${next_day_price:<10.2f} ${cost:<10.2f}\033[0m")
                elif result[0][1] == -1:
                    # Sell the stock
                    # Allows change in purchasing strategy
                    shares_sold = round(shares * sell_ratio, 2)
                    profit = shares_sold * next_day_price
                    shares -= shares_sold
                    current_cash = current_cash + profit
                    trades_made += 1
                    if print_trades:
                        print(
                            f"\033[91m{next_day_date:<15} {pattern.type:<15} {'Sell':<10} {shares_sold:<10.2f} ${next_day_price:<10.2f} ${profit:<10.2f}\033[0m")

    # Sell all remaining stock on last day
    current_day = data.iloc[-1]
    current_day_price = round(current_day.Close, 2)
    formatted_date = format_date(current_day.name)
    shares_sold = shares  # Allows change in purchasing strategy
    profit = shares_sold * next_day_price
    shares -= shares_sold
    current_cash += profit
    trades_made += 1
    if print_trades:
        print(
            f"\033[91m{formatted_date:<15} {'Final':<15} {'Sell':<10} {shares_sold:<10.2f} ${current_day_price:<10.2f} ${profit:<10.2f}\033[0m")

    # Calculating results
    total_profit = round(current_cash - starting_cash, 2)
    profit_percent = round(current_cash / starting_cash * 100 - 100, 2)

    return {'value': current_cash, 'num_trades': trades_made, 'profit': total_profit, 'profit_percent': profit_percent}


if __name__ == '__main__':
    # No command line arguments
    if len(sys.argv) == 1:
        ticker = 'CRWD'  # IOR, INTL
        print_trades = True
    else:  # <Ticker> <Flags>
        ticker = sys.argv[1]
        print_trades = '-p' in sys.argv

    pattern_matchers: List[PatternMatcher] = [eval(pattern)(
    ) for pattern in PatternMatcher.SUBCLASSES]  # Choose pattern to be tested

    info = yf.Ticker(ticker)
    data = info.history(period='1y', interval='1d')
    if len(data) == 0:
        print("Ticker not found")
        quit()

    result = simulate_trading(pattern_matchers, data, starting_cash=1000,
                              buy_ratio=.5, sell_ratio=.2, print_trades=print_trades)

    # Final balance
    print(result)
