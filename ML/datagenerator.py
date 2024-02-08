import yfinance as yf
import pandas as pd

def generate_data(ticker: str):
    ticker = yf.Ticker(ticker)
    
    stock_data = ticker.history(period='1y', interval='1d', rounding=2)[['Close', 'Volume']]
    stock_data.rename(columns={'Close': 'Price'}, inplace=True)
    
    # Calculating MA
    stock_data['MA'] = stock_data['Price'].rolling(window=30).mean()
    stock_data = stock_data.iloc[30:]  # Remove the first 30 days which dont have MAs
    
    # Data normalization
    normalized_data = pd.DataFrame()
    min_value = stock_data['Volume'].min()
    max_value = stock_data['Volume'].max()
    normalized_data['Volume'] = (stock_data['Volume'] - min_value) / (max_value - min_value)
    normalized_data['MA'] = (stock_data['MA'] / stock_data['Price'])
    min_value = stock_data['Price'].min()
    max_value = stock_data['Price'].max()
    normalized_data['Price'] = (stock_data['Price'] - min_value) / (max_value - min_value)

    training_data = {'Date': [], 'X':[], 'y':[]}
    days_window = 30
    for first_day_idx in range(len(stock_data) - days_window):
        current_data = stock_data.iloc[first_day_idx: first_day_idx + days_window + 1]
        current_normalized_data = normalized_data.iloc[first_day_idx: first_day_idx + days_window + 1]
        current_day = current_data.iloc[-2]
        next_day = current_data.iloc[-1]
        
        training_data['Date'].append(current_day.name)
        training_data['X'].append(current_normalized_data.iloc[:-1].values)
        training_data['y'].append(round(((next_day.Price - current_day.Price) / current_day.Price * 100), 2))
        
    training_data = pd.DataFrame(training_data, index=training_data['Date'], columns=['X', 'y'])
    print(training_data)