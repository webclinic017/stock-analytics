import numpy as np
import matplotlib.pyplot as plt


class BasicBollingerAgent:
    def __init__(self, window=20, dev=2):
        self.window = window
        self.dev = dev

    def __call__(self, df):
        df = df.iloc[-self.window:]
        price = df.iloc[-1].loc['Close']
        avg = np.mean(df["Close"])
        std = np.std(df["Close"])
        upper = avg + std * self.dev
        lower = avg - std * self.dev
        if price > upper:
            return 0
        if price < lower:
            return 2
        else:
            return 1

    def render(self, df_res):

        df_res = df_res.dropna().copy()
        df_res["rolling_std"] = df_res['Close'].rolling(window=self.window).std()
        df_res['avg'] = df_res['Close'].rolling(window=self.window).mean()
        df_res['lower'] = df_res['avg'] - df_res["rolling_std"] * self.dev
        df_res['upper'] = df_res['avg'] + df_res["rolling_std"] * self.dev

        df_ind_s = df_res[df_res["action"] == 0]
        df_ind_b = df_res[df_res["action"] == 2]

        plt.figure(figsize=(20, 8))
        plt.plot(df_res["Date"], df_res["Close"], c="b")

        # Plot average and bands
        plt.plot(df_res["Date"], df_res['avg'], c="orange")
        plt.plot(df_res["Date"], df_res["lower"], c="red")
        plt.plot(df_res["Date"], df_res["upper"], c="red")

        # Plot the indicators. Green when we should buy(falling below std), and red for selling(above std)
        plt.scatter(df_ind_b["Date"], df_res.loc[df_ind_b.index]["Close"], c="green")
        plt.scatter(df_ind_s["Date"], df_res.loc[df_ind_s.index]["Close"], c="red")

        plt.show()
