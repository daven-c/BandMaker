import yfinance as yf
from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict


class PatternMatcher(ABC):
    
    SUBCLASSES = None

    def __init__(self, type):
        self.type = type
        
    @abstractmethod
    def process(self, data: pd.DataFrame) -> Tuple[pd.Series, int]:
        ...

    @staticmethod
    def stockDirection(df):
        # return values: 1 bullish, -1 bearish
        if (df.Open - df.Close >= 0):
            return -1
        else:
            return 1

class MomentumCandle(PatternMatcher):
    CANDLES_REQUIRED = 2

    # Copy paste this
    def __init__(self, scale: float = 5):
        super(MomentumCandle, self).__init__("MomentumCandle")
        self.scale = scale

    def process(self, data: pd.DataFrame):

        signals_found = []

        for i in range(1, len(data)):
            prev_candle = data.iloc[i - 1]
            curr_candle = data.iloc[i]
            close_difference = abs(curr_candle.Open - curr_candle.Close)
            prev_difference = abs(prev_candle.Open - prev_candle.Close)

            if close_difference > self.scale * prev_difference:
                signals_found.append((curr_candle, super().stockDirection(curr_candle)))
        return signals_found

class EngulfingCandle(PatternMatcher):
    CANDLES_REQUIRED = 2

    def __init__(self):
        super(EngulfingCandle, self).__init__("EngulfingCandle")

    def process(self, data : pd.DataFrame):

        signals_found = []

        for i in range(1, len(data)):
            prev_candle = data.iloc[i-1]
            curr_candle = data.iloc[i]
            if curr_candle.Open < prev_candle.Open and curr_candle.Open < prev_candle.Close and curr_candle.Close > prev_candle.Open and curr_candle.Close > prev_candle.Close:  # bullish
                signals_found.append((curr_candle, 1))
            elif curr_candle.Open > prev_candle.Open and curr_candle.Open > prev_candle.Close and curr_candle.Close < prev_candle.Open and curr_candle.Close < prev_candle.Close:  # bearish
                signals_found.append((curr_candle, -1))
        return signals_found
"""
class MultipleCandle(PatternMatcher):
    CANDLES_REQUIRED = 3
    
    def __init__(self, scale : float = 0.10):
        super(MultipleCandle, self).__init__("MultipleCandle")

    def signal_multiple_candle(self, df):
        wickDirection = set()
        for i in range(0, len(df)):
            direction = super().stockDirection(df.iloc[i])
            if direction == 1:  # bullish
                topWickSize = df.High.iloc[i] - df.Close.iloc[i]
                botWickSize = df.Open.iloc[i] - df.Low.iloc[i]
                wickDirection.add(-1 if topWickSize > botWickSize else 1)  # puts the direction the bigger wick is going into wickDirection set
            elif direction == -1:  # bearish
                topWickSize = df.High.iloc[i] - df.Open.iloc[i]
                botWickSize = df.Close.iloc[i] - df.Low.iloc[i]
                wickDirection.add(-1 if topWickSize > botWickSize else 1)
        if len(wickDirection) > 1:
            return 0
        return wickDirection.pop()
        
        
    def process(self, data: pd.DataFrame):
        signals_found = []

        for i in range(2, len(data)):
            df = data[i-2:i+1]
            curr_candle = data.iloc[i]
            signal = self.signal_multiple_candle(df)
            if signal == 1 or signal == -1:
                signals_found.append((curr_candle, signal))
        return signals_found
"""

class DojiCandle(PatternMatcher): #TODO: tweak the ratio A LOT 
    CANDLES_REQUIRED = 3

    def __init__(self, scale : float = 20):
        super(DojiCandle, self).__init__("DojiCandle")
        self.scale = scale

    def signal_doji_candle(self, df):#scale: the two wicks combined is "scale" times larger than body
        #check if first candle is a doji candle
        bodyLength = abs(df.Open.iloc[0] - df.Close.iloc[0])
        direction = super().stockDirection(df.iloc[0])
        if (direction == 1):  # bullish
            WickSize = (df.High.iloc[0] - df.Close.iloc[0]) + (df.Open.iloc[0] - df.Low.iloc[0])
        elif (direction == -1):  # bearish
            WickSize = (df.High.iloc[0] - df.Open.iloc[0]) + (df.Close.iloc[0] - df.Low.iloc[0])
        
        if (bodyLength * self.scale <= WickSize): #if candle is doji (wicks long enough in comparison to body)
            if(super().stockDirection(df.iloc[1]) == direction and super().stockDirection(df.iloc[2]) == direction): 
                return direction
        else:
            return 0

    def process(self, data : pd.DataFrame):
        signals_found = []

        for i in range(2, len(data)):
            df = data[i-2:i+1]
            signal = self.signal_doji_candle(df)
            if signal == -1 or signal == 1:
                signals_found.append((data.iloc[i-2], signal))
        return signals_found

class Hammer(PatternMatcher):
    CANDLES_REQUIRED = 1

    def __init__(self, max_body_length_min: float = 0.01, max_body_length_max: float = 0.3, threshold: float = 10):
        """
        Args: 
            max_body_length_min (float, optional): min length of the body in proportion to the total length. Defaults to 0.2.
            max_body_length_min (float, optional): max length of the body in proportion to the total length. Defaults to 0.3.
            threshold (float, optional): proportion of the total candlestick length that the Open must reside below. Defaults to 0.4.
        """
        super(Hammer, self).__init__("Hammer")
        self.max_body_length_min = max_body_length_min
        self.max_body_length_max = max_body_length_max
        self.threshold = threshold

    def process(self, data: pd.DataFrame):
        signals_found = []

        for i in range(len(data)):
            candlestick = data.iloc[i]
            total_length = candlestick.High - candlestick.Low
            body_length = candlestick.Open - candlestick.Close
            direction = super().stockDirection(candlestick)
            # Bullish signal if body is wide enough and wick is long enough (no top wick)
            if not(candlestick.Open == candlestick.Close == candlestick.High == candlestick.Low) and (body_length <= total_length * self.max_body_length_max) and (body_length >= total_length * self.max_body_length_min):
                if(direction == 1) and (candlestick.Close / candlestick.High == .05): #TODO: change these == 0s to <= (a range) 
                    signals_found.append((candlestick, 1))
                elif(direction == -1) and (candlestick.Open / candlestick.High == .05):
                    signals_found.append((candlestick, 1))

        return signals_found

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
        signals_found = []

        for i in range(len(data)):
            candlestick = data.iloc[i]
            total_length = candlestick.High - candlestick.Low
            body_length = candlestick.Open - candlestick.Close
            # Bearish candle and body is less than the max size and body resides below threshold value
            if (body_length > 0) and (body_length <= total_length * self.max_body_length) and (candlestick.Open <= total_length * self.threshold + candlestick.Low):
                signals_found.append((candlestick, -1))

        return signals_found


"""
class Tweezer(PatternMatcher):
    CANDLES_REQUIRED = 2

    def __init__(self, difference_threshold: float = 0.005):
        super(Tweezer, self).__init__("Tweezer")
        self.threshold = difference_threshold

    def process(self, data: pd.DataFrame):
        signals_found = []

        for i in range(1, len(data)):
            prev_candle = data.iloc[i - 1]
            curr_candle = data.iloc[i]

            prev_candle_body = prev_candle.Open - prev_candle.Close
            curr_candle_body = curr_candle.Open - curr_candle.Close
            # Case 1: Red, Green + wicks at the bottom - bullish
            if (prev_candle_body > 0 and curr_candle_body < 0):
                compare_low = prev_candle.Low / curr_candle.Low
                if 1 - self.threshold <= compare_low <= 1 + self.threshold:
                    signals_found.append((curr_candle, 1))

            # Case 2: Green, Red + wicks at the top - bearish
            if (prev_candle_body < 0 and curr_candle_body > 0):
                compare_high = prev_candle.High / curr_candle.High
                if 1 - self.threshold <= compare_high <= 1 + self.threshold:
                    signals_found.append((curr_candle, -1))
        return signals_found
"""


class Marubozu(PatternMatcher):
    CANDLES_REQUIRED = 1

    def __init__(self):
        super(Marubozu, self).__init__("Marubozu")

    def process(self, data: pd.DataFrame):
        signals_found = []

        for i in range(len(data)):
            candlestick = data.iloc[i]
            if candlestick.Open < candlestick.Close:  # Bullish
                if candlestick.High == candlestick.Close and candlestick.Low == candlestick.Open:
                    signals_found.append((candlestick, 1))
            elif candlestick.Open > candlestick.Close:  # Bearish
                if candlestick.High == candlestick.Open and candlestick.Low == candlestick.Close:
                    signals_found.append((candlestick, -1))
        return signals_found

# Gets all candle patterns
PatternMatcher.SUBCLASSES = [x.__name__ for x in PatternMatcher.__subclasses__()]

if __name__ == '__main__':
    print(PatternMatcher.SUBCLASSES)