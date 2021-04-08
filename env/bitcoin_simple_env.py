import gym
from gym import spaces
import pandas as pd
import numpy as np


"""
Modifying the following code:
https://github.com/fhaynes/Bitcoin-Trader-RL/blob/master/env/BitcoinTradingEnv.py
"""

class BitcoinTradingEnv(gym.Env):

    def __init__(self, data_path, lookback_window_size=40, initial_balance=1000):

        self.df = pd.read_pickle(data_path)

        self.df = self.df.dropna().reset_index()

        start = 10000
        end = 11000
        self.df = self.df.iloc[start:end]

        self.lookback_window_size = lookback_window_size
        self.initial_balance = initial_balance

        self.space = spaces.MultiDiscrete([3, 10])
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(10, lookback_window_size + 1), dtype=np.float16)

    def _next_observation(self):
        end = self.current_step + self.lookback_window_size + 1

        scaled_df = self.active_df.values[:end].astype('float64')
        # scaled_df = self.scaler.fit_transform(scaled_df)
        # scaled_df = pd.DataFrame(scaled_df, columns=self.df.columns)

        obs = np.array([
            # scaled_df['Open'].values[self.current_step:end],
            # scaled_df['High'].values[self.current_step:end],
            # scaled_df['Low'].values[self.current_step:end],
            scaled_df['Price'].values[self.current_step:end],
            scaled_df['Volume'].values[self.current_step:end],
        ])

        scaled_history = self.scaler.fit_transform(self.account_history)

        obs = np.append(
            obs, scaled_history[:, -(self.lookback_window_size + 1):], axis=0)

        return obs


    def _reset_session(self):
        self.current_step = 0

        # if self.serial:
        self.steps_left = len(self.df) - self.lookback_window_size - 1
        self.frame_start = self.lookback_window_size
        # else:
        #     self.steps_left = np.random.randint(1, MAX_TRADING_SESSION)
        #     self.frame_start = np.random.randint(
        #         self.lookback_window_size, len(self.df) - self.steps_left)

        self.active_df = self.df[self.frame_start - self.lookback_window_size:
                                 self.frame_start + self.steps_left]


    def reset(self):
        self.balance = self.initial_balance
        self.net_worth = self.initial_balance
        self.btc_held = 0

        self._reset_session()

        self.account_history = np.repeat([
            [self.balance],
            [0],
            [0],
            [0],
            [0]
        ], self.lookback_window_size + 1, axis=1)
        self.trades = []

        return self._next_observation()
