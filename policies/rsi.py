import ta
import matplotlib.pyplot as plt


class BasicRSIAgent:

    def __init__(self, window=14):
        self.window = window

    def __call__(self, df):
        df = df.iloc[-self.window:]
        rsi = ta.momentum.RSIIndicator(close=df["Close"]).rsi().values
        last_rsi_value = rsi[-1]

        # The indicator levels for buy/sell should be dynamical
        if last_rsi_value > 70:
            action = 0
        elif last_rsi_value < 30:
            action = 2
        else:
            action = 1

        return action

    def render(self, df_res):
        df_res = df_res.dropna().copy()

        df_ind_s = df_res[df_res["action"] == 0]
        df_ind_b = df_res[df_res["action"] == 2]

        plt.figure(figsize=(20, 8))
        plt.plot(df_res["Date"], df_res["Close"], c="b")
        plt.scatter(df_ind_b["Date"], df_res.loc[df_ind_b.index]["Close"], c="green")
        plt.scatter(df_ind_s["Date"], df_res.loc[df_ind_s.index]["Close"], c="red")

        plt.show()
