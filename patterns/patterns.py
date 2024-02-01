import yfinance as yf
from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod
from typing import Tuple, List


class PatternMatcher(ABC):

    def __init__(self, type):
        self.type = type

    @abstractmethod
    def process(self):
        ...


class MomentumCandle(PatternMatcher):
    CANDLES_REQUIRED = 2

    # Copy paste this
    def __init__(self, scale: float = 2.5):
        super(MomentumCandle, self).__init__("MomentumCandle")

    def signal_momentum_candle(self, df):
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

    def process(self, data: pd.DataFrame):
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
        for i in range(1, len(data)):
            candle_length.append(data.Open.iloc[i] - data.Close.iloc[i])
        data["candle_length"] = candle_length

        # Add signal column to data frame
        for i in range(1, len(data)):
            df = data[i-1:i+1]
            signal.append(self.signal_momentum_candle(df))
        data["signal"] = signal
        return data


class ShootingStar(PatternMatcher):
    CANDLES_REQUIRED = 1
    def __init__(self, max_body_length: float = 0.2, threshold: float = 0.4):
        """
        Args: 
            max_body_length (float, optional): max length of the body in proportion to the total length. Defaults to 0.2.
            threshold (float, optional): proportion of the total candlestick length that the Open must reside below. Defaults to 0.4.
        """
        super(ShootingStar, self).__init__("ShootingStar")
        self.max_body_length = max_body_length
        self.threshold = threshold

    def process(self, data: pd.DataFrame):
        signals_found: Tuple[datetime, int] = []

        for idx, candlestick in enumerate(data):
            total_length = candlestick.High - candlestick.Low
            body_length = candlestick.Open - candlestick.Close
            # Bearish candle and body is less than the max size and body resides below threshold value
            if (body_length < 0) and (body_length <= total_length * self.max_body_length) and (candlestick.Open <= total_length * self.threshold + candlestick.Low):
                signals_found.append((candlestick.name, -1))

        return signals_found


class Tweezer(PatternMatcher):
    CANDLES_REQUIRED = 2
    
    def __init__(self, max_short_wick_length: float = 0.03, difference_threshold: float = 0.05):
        super(Tweezer, self).__init__("Tweezer")
        self.max_short_wick_length = max_short_wick_length
        self.threshold = difference_threshold

    def process(self, data: pd.DataFrame):
        signals_found: Tuple[datetime, int] = []

        for i in range(1, len(data)):
            prev_candle = data[i - 1]
            curr_candle = data[i]

            prev_candle_body = prev_candle.Open - prev_candle.Close
            curr_candle_body = curr_candle.Open - curr_candle.Close
            # Case 1: Red, Green + wicks at the bottom - bullish
            if (prev_candle_body < 0 and curr_candle_body > 0):
                compare_low = prev_candle.Low / curr_candle.Low
                if 1 - self.threshold <= compare_low <= 1 + self.threshold:
                    signals_found.append((curr_candle.name, 1))
                
            # Case 2: Green, Red + wicks at the top - bearish
            if (prev_candle_body > 0 and curr_candle_body < 0): 
                compare_high = prev_candle.High / curr_candle.High
                if 1 - self.threshold <= compare_high <= 1 + self.threshold:
                    signals_found.append((curr_candle.name, -1))
        return signals_found

class Marubozu(PatternMatcher):
    CANDLES_REQUIRED = 1
    
    def __init__(self):
        super(Marubozu, self).__init__("Marubozu")

    def process(self, data: pd.DataFrame):
        signals_found: Tuple[datetime, int] = []
        
        for idx, candlestick in enumerate(data):
            if data.Open < data.Close:  # Bullish
                if data.Open == data.High and data.Close == data.Low:
                    signals_found.append((candlestick.name, 1))
            else:  # Bearish
                if data.Open == data.Low and data.Close == data.High:
                    signals_found.append((candlestick.name, -1))
        return signals_found

if __name__ == '__main__':
    # Class testing
    symbol = 'AAPL'
    # stock = yf.download(symbol, start="2023-12-1", interval="1d")

    candle = ShootingStar(stock)
    data = {'open': [1, 2, 6], 'close': [10, 3, 1]}
    # DataFrame = pd.DataFrame(data)
    print(candle.process())
    
