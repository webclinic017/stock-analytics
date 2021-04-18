#1) Wait for an uptrend (10 EMA (Orange) crosses ABOVE 20 EMA (Blue))
#2) Wait for price to breakout then retest the EMA's (either one(based on the trend type)) need to retest either 20 or 10.
#only use 10 if there is a high trend, mening rapid changes
#3) Wait for bullish confirmation candle after the retest
#4) Enter after the confirmation candle
#5) Set a stop loss underneath the previous swing low (previous Zigzag point)
#6) Take profit one the EMA's cross the other direction (10 EMA crosses BELOW 20 EMA)
import numpy
import pandas_ta as ta
from talib import MA_Type


class scalpingAgent:
    def __init__(self, window=20):
        self.window = window
        self.uptrend = 0
        self.ref = 0
        self.bull_confirmed = 0
        self.downtrend = 0
        self.retest = 0
        self.uptrend = 0
        self.last_zigzag = 0
        self.inposition = 0

    def __call__(self, df):

        df = df.iloc[-self.window:]
        high, low, closes = df["High"], df["Low"], df["Close"]
        EMA_20 = ta.ema(closes, 12)
        EMA_10 = ta.ema(closes, 6)
        ema20 = float(EMA_20.to_list()[-1])
        ema10 = float( EMA_10.to_list()[-1])
        close = closes.to_list()[-1]

        # 1) Wait for an uptrend (10 EMA (Orange) crosses ABOVE 20 EMA (Blue))
        if ema10 > ema20:
            self.uptrend = 1
            self.downtrend = 0
            self.ref = close

        if ema10 < ema20:
            self.downtrend = 1
            self.uptrend = 0
            self.ref = close

        # 2) Wait for price to breakout then retest the EMA's (either one(based on the trend type)) need to retest either 20 or 10.
        # only use 10 if there is a high trend, mening rapid changes
        if close > ema10:
            self.bull_confirmed = 1

        # 3) Wait for bullish confirmation candle after the retest
        if self.bull_confirmed and not self.inposition:
            # 4) Enter after the confirmation candle
            if close <= (ema10 or ema20):
                self.inposition = 1
                return 2

        # 5) Set a stop loss underneath the previous swing low (previous Zigzag point)
        if abs((close-self.ref)/self.ref) > 0.1:
                self.uptrend = 0
                self.bull_confirmed = 0
                self.downtrend = 0
                self.retest = 0
                self.uptrend = 0
                self.last_zigzag = 0
                self.inposition = 0
                print(abs((close - self.ref) / self.ref))
                return 0

        # 6) Take profit one the EMA's cross the other direction (10 EMA crosses BELOW 20 EMA)
        if self.downtrend:
            if self.inposition:
                self.uptrend = 0
                self.bull_confirmed = 0
                self.downtrend = 0
                self.retest = 0
                self.uptrend = 0
                self.last_zigzag = 0
                self.inposition = 0
                return 0
        return 1

        def render(self, df_res):
            df_res = df_res.dropna().copy()

            df_ind_s = df_res[df_res["action"] == 0]
            df_ind_b = df_res[df_res["action"] == 2]

            plt.figure(figsize=(20, 8))
            plt.plot(df_res["Date"], df_res["Close"], c="b")
            plt.scatter(df_ind_b["Date"], df_res.loc[df_ind_b.index]["Close"], c="green")
            plt.scatter(df_ind_s["Date"], df_res.loc[df_ind_s.index]["Close"], c="red")

            plt.show()