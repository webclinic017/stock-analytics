import talib
import numpy

class RoundRobin:
    turn = 0

    def __call__(self, obs):
        return self.select_action(obs)

    def select_action(self, obs):
        action = self.turn
        self.turn = 1 - self.turn
        return action

class ATR_swing:
    def __call__(self, obs):
        return self.select_action(obs)

    def select_action(self, obs):
        highs, lows, closes = 'High', 'Low', 'Close' in obs
        return talib.ATR(list(map(int, highs)), list(map(int, lows)), list(map(int, closes)), timeperiod = 3)




#You must know the behaviour of the markets you’re trading; some have trending behaviour and some a mean-reverting behaviour
#The market is unlikely to exceed 2 ATR in a day. So, you can use it as a gauge to determine how far the market can potentially move in a day.
#The previous week high/low are important levels to pay attention to
#If the volatility of the markets is low over the last few days, then expect volatility to expand soon
#You want to trade during the most volatile hours of the session
#Be aware of major news release as the spread tends to widen (and you could get stopped out of your trades)
#If you want low risk and high reward trading setups, then enter your trades near Support & Resistance (on the higher timeframe)