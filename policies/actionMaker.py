#lookback_window_size =40

import numpy
import talib
from talib import MA_Type


def handle_data(obs):
    prices, volumes = obs
    price = prices[len(prices)-1]
    rsi = talib.RSI(prices)[len(prices)-1]
    sma = talib.SMA(prices, 20)[len(prices)-1]
    #upper, middle, lower = talib.BBANDS(prices, matype=MA_Type.T3)
    #output = talib.MOM(prices, timeperiod=5)
    if float(rsi) > 60 and sma <price:
        print("RSI is above 60 annd SMA is below price - SELL SELL SELL", rsi, sma)
        return 1 #sell
    if float(rsi) < 30 and sma> price:
        print("RSI is below 30 and SMA is above price - BUY BUY BUY", rsi, sma)
        return 0 #buy
    else:
        return 2
    return rsi,