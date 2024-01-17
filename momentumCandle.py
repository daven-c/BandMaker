import yfinance as yf
import pandas as pd

#A candle that is 2-3 times larger than the candle before
#Price happens to go in the direction of the large candle
#Used in choppy markets

class momentumCandle:
    def __init__(self, stockName):
        self.stockName = stockName
        self.priceArea = []
    
    def detect(self):
        ticker = yf.ticker(self.stockName)
        #Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        data = ticker.history(period='60m', interval='5m')
        ret = ["bullish" , False]
        for index, row in data.iterrows():
            self.priceArea.append(row['close'] - row['open']) 
        for i in range(len(self.priceArea) - 1):
            if abs(self.priceArea[i]) > abs(self.priceArea[i + 1] * 2.5):
                ret[1] = True
                if self.priceArea[i] < 0:
                    ret[0] = "bearish"
            print(self.priceArea)
            return ret
        return ret
        
#class testing
# Candle = momentumCandle("appl")
# data = {'open': [1, 2, 6], 'close': [10, 3, 1]}
# dataFrame = pd.DataFrame(data)
# print(Candle.detect(dataFrame))