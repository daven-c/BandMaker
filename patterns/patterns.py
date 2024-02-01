import yfinance as yf
from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod


@ABC
class PatternMatcher(ABC):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process(self):
        ...

    def stockDirection(df):
        # return values: 1 bullish, -1 bearish
        if (df.Open.iloc[-1] - df.Close.iloc[-1] >= 0):
            return -1
        else:
            return 1


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
        close_difference = df.Open.iloc[1] - df.Close.iloc[1]
        prev_difference = df.Open.iloc[0] - df.Close.iloc[0]

        if abs(close_difference) > abs(scale * prev_difference):
            return (-1 if close_difference > 0 else 1)

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
        
        if(bodyLength * scale <= WickSize): #if candle is not doji (wicks not long enough in comparison to body)
            if(super.stockDirection(df[1]) == )
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

if __name__ == '__main__':
    # Class testing
    symbol = 'AAPL'
    stock = yf.download(symbol, start="2023-12-1", interval="1d")

    candle = MomentumCandle(stock)
    data = {'open': [1, 2, 6], 'close': [10, 3, 1]}
    # DataFrame = pd.DataFrame(data)
    print(candle.process())
