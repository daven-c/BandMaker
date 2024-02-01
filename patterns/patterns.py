import yfinance as yf
from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod

@ABC
class PatternMatcher:
    
    def __init__(self, data):
        self.data = data
        
    @abstractmethod
    def process(self):
        ...
        
        
class MomentumCandle(PatternMatcher):
    
    # Copy paste this
    def __init__(self, data):
        super(MomentumCandle, self).__init__(data)
    
    def signal_momentum_candle(self, df, scale: float = 2.5):
        """
        Summary:
            asd

        Args:
            asd

        Returns:
            asd
        """
        close_difference = df.Open.iloc[-1] - df.Close.iloc[-1]
        prev_difference = df.Open.iloc[-2] - df.Close.iloc[-2]

        if abs(close_difference) > abs(scale * prev_difference):
            return (1 if close_difference > 0 else 2)
        
        return -1
    
    def process(self):
        """
        Summary:
            asd

        Args:
            asd

        Returns:
            asd
        """

        signal = []
        candle_length = []
        candle_length.append(0)
        signal.append(0)
        
        # Add candle stick length column to data frame
        for i in range(1,len(data)):
            candle_length.append(data.Open.iloc[i] - data.Close.iloc[i])
        data["candle_length"] = candle_length
        
        # Add signal column to data frame
        for i in range(1,len(data)):
            df = data[i-1:i+1]
            signal.append(self.signal_momentum_candle(df))
        data["signal"] = signal
        return data
    
    
class ShootingStar(PatternMatcher)
if __name__ == '__main__':
    # Class testing
    symbol = 'AAPL'
    stock = yf.download(symbol, start="2023-12-1", interval="1d")   
    
    candle = MomentumCandle(stock)
    data = {'open': [1, 2, 6], 'close': [10, 3, 1]}
    # DataFrame = pd.DataFrame(data)
    print(candle.process())
