import gym
from gym import spaces
import pandas as pd
import numpy as np
from datetime import datetime
"""
Actions: 0 = sell, 1 = hold, 2 = buy
"""

class BitcoinTradingEnv(gym.Env):

    def __init__(self, df,
                 start_date,
                 html_save_path="result.html",
                 initial_balance=1000,
                 debug=False,
                 start_idx=1000,
                 steps=2000):

        self.df = df.copy()
        self.df = self.df[self.df.Date > start_date]
        self.df = self.df.iloc[:start_idx+steps]
        self.html_save_path = html_save_path
        self.df = self.df.dropna().reset_index()
        self.df = self.df.sort_values('Date')
        self.df["net_worth"] = None
        self.df["action"] = None
        self.df["reward"] = None

        if debug:
            self.df = self.df.iloc[:start_idx+1000]

        self.initial_balance = initial_balance
        self.holding = False
        self.current_step = start_idx
        self.start_idx = start_idx

    def _reset_session(self):
        self.current_step = self.start_idx
        self.steps_left = len(self.df) - self.current_step
        self.net_worth = self.initial_balance

    def reset(self):
        self.holding = False
        self._reset_session()
        return self._next_observation()

    def _next_observation(self):
        return self.df.loc[:self.current_step]

    def _get_current_price(self):
        return self.df['Close'].values[self.current_step]

    def update_net_worth(self, current_price):
        diff = (current_price - self.previous_price)
        gain_prc = diff / self.previous_price
        self.net_worth = self.net_worth * (1 + gain_prc)

    def _take_action(self, action, current_price):
        action_type = action

        if self.holding:
            self.update_net_worth(current_price)

        self.previous_price = current_price

        if action_type == 2:
            self.holding = True  # We are holding

        elif action_type == 0:
            self.holding = False  # We sold everything :)


    def step(self, action):
        current_price = self._get_current_price()
        prev_net_worth = self.net_worth

        self._take_action(action, current_price)
        reward = self.net_worth - prev_net_worth

        self.df.loc[self.current_step, 'action'] = action
        self.df.loc[self.current_step, 'reward'] = reward
        self.df.loc[self.current_step, 'net_worth'] = self.net_worth

        self.steps_left -= 1
        self.current_step += 1

        obs = self._next_observation()
        if self.net_worth <= 0:
            print("Net worth < 0 => Done")
            done = True
        elif self.steps_left == 0:
            print("Steps left == 0 => Done")
            done = True
        else:
            done = False

        return obs, reward, done, {}


    # def render(self, mode='human', **kwargs):
    #     from .simple_renderer import plotly_render
    #     plotly_render(self.df, self.html_save_path, self.time_plot_min)
