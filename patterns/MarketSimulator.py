import yfinance as yf
from patterns import *
import pandas as pd
from datetime import datetime, timedelta
import sys

def format_date(date, get_next_day: bool = False):
    dt_object = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z")
    if get_next_day:
        dt_object = dt_object + timedelta(days=1)
    formatted_date = dt_object.strftime("%m-%d-%y")
    return formatted_date

def simulate_trading(data: pd.DataFrame, starting_cash: int = 1000, print_trades: bool = False):
    
    current_value = starting_cash
    shares = 0
    trades_made = 0
    
    if print_trades:
        print(f"{'Date':<15} {'Buy/Sell':<10} {'Shares':<10} {'Price':<10} {'Value':<10}")
        
    # Iterate up to the most recent day, sell all shares on the last day
    # Buy/Sell at the opening price of the next day, simulates placing orders overnight
    for day_idx in range(pattern_matcher.CANDLES_REQUIRED - 1, len(data) - 1):
        result = pattern_matcher.process(data=data.iloc[day_idx - Marubozu.CANDLES_REQUIRED + 1:day_idx + 1])  # Check if pattern can be detected from past day
        if result != []:  # pattern found
            current_day = result[0][0]
            next_day_price = round(data.iloc[day_idx + 1].Open, 2)
            
            next_day_date = format_date(current_day.name, get_next_day=True)
            
            if result[0][1] == 1:  # Bullish pattern found
                # Buy the stock
                shares_bought = int(current_value / next_day_price)  # Allows change in purchasing strategy
                cost = round(shares_bought * next_day_price, 2)
                shares += shares_bought
                current_value -= cost
                trades_made += 1
                if print_trades:
                    print(f"\033[92m{next_day_date:<15} {'Buy':<10} {shares_bought:<10} ${next_day_price:<10} ${cost}\033[0m")
            elif result[0][1] == -1:
                # Sell the stock
                shares_sold = shares  # Allows change in purchasing strategy
                profit = round(shares_sold * next_day_price, 2)
                shares -= shares_sold
                current_value += profit
                trades_made += 1
                if print_trades:
                    print(f"\033[91m{next_day_date:<15} {'Sell':<10} {shares_sold:<10} ${next_day_price:<10} ${profit}\033[0m")
                
    # Sell all remaining stock on last day
    current_day = data.iloc[-1]
    current_day_price = round(current_day.Close, 2)
    formatted_date = format_date(current_day.name)
    shares_sold = shares  # Allows change in purchasing strategy
    profit = round(shares_sold * next_day_price, 2)
    shares -= shares_sold
    current_value += profit
    trades_made += 1
    print(f"\033[91m{formatted_date:<15} {'Sell':<10} {shares_sold:<10} ${current_day_price:<10} ${profit}\033[0m")
    
    # Calculating results
    total_profit = round(current_value - starting_cash, 2)
    profit_percent = round(current_value / starting_cash * 100 - 100, 2)
    
    return {'value': current_value, 'num_trades': trades_made, 'profit': total_profit, 'profit_percent': profit_percent}

if __name__ == '__main__':
    # No command line arguments
    if len(sys.argv) == 1:   
        ticker = 'SSIC'  # IOR, INTL
        print_trades = True
    else:  # <Ticker> <Flags>
        ticker = sys.argv[1]
        print_trades = '-p' in sys.argv
        
    pattern_matcher: PatternMatcher = Marubozu()  # Choose pattern to be tested
    
    info = yf.Ticker(ticker)
    data = info.history(period='1y', interval='1d')
    if len(data) == 0:
        print("Ticker not found")
        quit()
    
    result = simulate_trading(data, starting_cash=1000, print_trades=print_trades)
    
    # Final balance
    print(result)
    