import numpy as np
import matplotlib.pyplot as plt

def moving_average(x, n, type=None):
    x = np.asarray(x)
    if type =='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a


class EMA:

    def __init__(self, smaller_window=10, larger_window=20):
        self.smaller_window = smaller_window
        self.larger_window = larger_window
        self.holding = False

    def __call__(self, df):
        ema_small = moving_average(df["Close"], self.smaller_window, type="simple")
        ema_large = moving_average(df["Close"], self.larger_window, type="simple")

        ema_small = ema_small[-1]
        ema_large = ema_large[-1]

        if ema_small >= ema_large:
            if self.holding:
                return 1
            else:
                self.holding = True
                return 2
        if ema_small <= ema_large:
            if self.holding is False:
                return 1
            else:
                self.holding = False
                return 0


    def render(self, df_res):
        df_res = df_res.dropna().copy()

        df_ind_s = df_res[df_res["action"] == 0]
        df_ind_b = df_res[df_res["action"] == 2]

        plt.figure(figsize=(20, 8))
        plt.plot(df_res["Date"], df_res["Close"], c="b", alpha=0.5)
        plt.scatter(df_ind_b["Date"], df_res.loc[df_ind_b.index]["Close"], c="green", s=50)
        plt.scatter(df_ind_s["Date"], df_res.loc[df_ind_s.index]["Close"], c="red", s=50)

        ema_small = moving_average(df_res["Close"], self.smaller_window, type="simple")
        ema_large = moving_average(df_res["Close"], self.larger_window, type="simple")
        plt.plot(df_res["Date"], ema_small, c='orange')
        plt.plot(df_res["Date"], ema_large, c='red')

        plt.show()
