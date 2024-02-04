import yfinance as yf
from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod
from typing import Tuple, List


class PatternMatcher(ABC):

    def __init__(self, type):
        self.type = type
        
    @abstractmethod
    def process(self, data: pd.DataFrame) -> Tuple[pd.Series, int]:
        ...

    def stockDirection(df):
        # return values: 1 bullish, -1 bearish
        if (df.Open.iloc[-1] - df.Close.iloc[-1] >= 0):
            return -1
        else:
            return 1

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
        close_difference = df.Open.iloc[1] - df.Close.iloc[1]
        prev_difference = df.Open.iloc[0] - df.Close.iloc[0]

        if abs(close_difference) > abs(scale * prev_difference):
            return (-1 if close_difference > 0 else 1)
        return 0

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
        data["signal_momentum"] = signal
        return data

#TODO:CHANGE THIS TO GO THROUGH ALL THE DATA
class EngulfingCandle(PatternMatcher):

    # Copy paste this
    def __init__(self, data):
        super(EngulfingCandle, self).__init__(data)

    def signal_engulfing_candle(self, df, scale: float = 2.5):
        """
        Summary:
            asd

        Args:
            asd

        Returns:
            asd
        """
        # -1 is the current candlestick
        if df.Open.iloc[-1] < df.Open.iloc[-2] and df.Open.iloc[-1] < df.Close.iloc[-2] and df.Close.iloc[-1] > df.Open.iloc[-2] and df.Close.iloc[-1] > df.Close.iloc[-2]:  # bullish
            return 1
        elif df.Open.iloc[-1] > df.Open.iloc[-2] and df.Open.iloc[-1] > df.Close.iloc[-2] and df.Close.iloc[-1] < df.Open.iloc[-2] and df.Close.iloc[-1] < df.Close.iloc[-2]:  # bearish
            return -1
        return 0

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
        signal.append(0)
        recentData = data.tail(3)

        # Add signal column to data frame
        for i in range(1, len(data)):
            df = recentData[i-1:i+1]
            signal.append(self.signal_engulfing_candle(df))
        data["signal_engulfing"] = signal
        return data

#CHANGE TO A LIST OF TUPLES RETURN
#CHANGE TO A LIST OF TUPLES RETURN
#CHANGE TO A LIST OF TUPLES RETURN
#CHANGE TO A LIST OF TUPLES RETURN

#CHANGE TO A LIST OF TUPLES RETURN
#CHANGE TO A LIST OF TUPLES RETURN
class MultipleCandle(PatternMatcher): #TODO:CHANGE TO A LIST OF TUPLES RETURN
    # Copy paste this
    def __init__(self, data):
        super(MultipleCandle, self).__init__(data)

    def signal_multiple_candle(self, df):
        wickDirection = {}
        for i in range(0, len(df)):
            direction = super.stockDirection(df[i])
            if (direction == 1):  # bullish
                topWickSize = df.High.iloc[i] - df.Close.iloc[i]
                botWickSize = df.Open.iloc[i] - df.Low.iloc[i]
                wickDirection.update(1 if topWickSize > botWickSize else -1)  # puts the direction the bigger wick is going into wickDirection set
            elif (direction == -1):  # bearish
                topWickSize = df.High.iloc[i] - df.Open.iloc[i]
                botWickSize = df.Close.iloc[i] - df.Low.iloc[i]
                wickDirection.update(1 if topWickSize > botWickSize else -1)
        if(len(wickDirection) > 1):
            return 0
        return wickDirection.pop()
        
        
    def process(self):
        signal = []
        signal.append(0)

        # Add signal column to data frame
        for i in range(2, len(data)):
            df = data[i-2:i+1]
            signal.append(self.signal_mutltiple_candle(df))
        data["signal_multiple"] = signal
        return data

class DojiCandle(PatternMatcher):
    # Copy paste this
    def __init__(self, data):
        super(DojiCandle, self).__init__(data)

    def signal_doji_candle(self, df, scale: 15):#scale: the two wicks combined is "scale" times larger than body
        #check if first candle is a doji candle
        bodyLength = abs(df.Open.iloc[0] - df.Close.iloc[0])
        direction = super.stockDirection(df[0])
        if (direction == 1):  # bullish
            WickSize = (df.High.iloc[0] - df.Close.iloc[0]) + (df.Open.iloc[0] - df.Low.iloc[0])
        elif (direction == -1):  # bearish
            WickSize = (df.High.iloc[0] - df.Open.iloc[0]) + (df.Close.iloc[0] - df.Low.iloc[0])
        
        if (bodyLength * scale <= WickSize): #if candle is not doji (wicks not long enough in comparison to body)
            if(super.stockDirection(df[1]) == direction):   
                ...
        else:
            return 0

    def process(self, data):
        signal = []
        signal.append(0)

        # Add signal column to data frame
        for i in range(2, len(data)):
            df = data[i-2:i+1]
            signal.append(self.signal_doji_candle(df))
        data["signal_doji"] = signal
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
        signals_found = []

        for i in range(len(data)):
            candlestick = data.iloc[i]
            total_length = candlestick.High - candlestick.Low
            body_length = candlestick.Open - candlestick.Close
            # Bearish candle and body is less than the max size and body resides below threshold value
            if (body_length < 0) and (body_length <= total_length * self.max_body_length) and (candlestick.Open <= total_length * self.threshold + candlestick.Low):
                signals_found.append((candlestick, -1))

        return signals_found


class Tweezer(PatternMatcher):
    CANDLES_REQUIRED = 2

    def __init__(self, max_short_wick_length: float = 0.03, difference_threshold: float = 0.05):
        super(Tweezer, self).__init__("Tweezer")
        self.max_short_wick_length = max_short_wick_length
        self.threshold = difference_threshold

    def process(self, data: pd.DataFrame):
        signals_found = []

        for i in range(1, len(data)):
            prev_candle = data.iloc[i - 1]
            curr_candle = data.iloc[i]

            prev_candle_body = prev_candle.Open - prev_candle.Close
            curr_candle_body = curr_candle.Open - curr_candle.Close
            # Case 1: Red, Green + wicks at the bottom - bullish
            if (prev_candle_body < 0 and curr_candle_body > 0):
                compare_low = prev_candle.Low / curr_candle.Low
                if 1 - self.threshold <= compare_low <= 1 + self.threshold:
                    signals_found.append((curr_candle, 1))

            # Case 2: Green, Red + wicks at the top - bearish
            if (prev_candle_body > 0 and curr_candle_body < 0):
                compare_high = prev_candle.High / curr_candle.High
                if 1 - self.threshold <= compare_high <= 1 + self.threshold:
                    signals_found.append((curr_candle, -1))
        return signals_found


class Marubozu(PatternMatcher):
    CANDLES_REQUIRED = 1

    def __init__(self):
        super(Marubozu, self).__init__("Marubozu")

    def process(self, data: pd.DataFrame):
        signals_found = []

        for i in range(len(data)):
            candlestick = data.iloc[i]
            if candlestick.Open <= candlestick.Close:  # Bullish
                if candlestick.High == candlestick.Close and candlestick.Low == candlestick.Open:
                    signals_found.append((candlestick, 1))
            else:  # Bearish
                if candlestick.High == candlestick.Open and candlestick.Low == candlestick.Close:
                    signals_found.append((candlestick, -1))
        return signals_found
