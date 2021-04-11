import gym
from gym import spaces
import pandas as pd
import numpy as np
from .bitcoin_trading_graph import BitcoinTradingGraph
"""
Modifying the following code:
https://github.com/fhaynes/Bitcoin-Trader-RL/blob/master/env/BitcoinTradingEnv.py
"""

class BitcoinTradingEnv(gym.Env):

    def __init__(self, data_path, lookback_window_size=40, initial_balance=1000):

        self.df = pd.read_pickle(data_path)
        self.df = self.df.dropna().reset_index()

        start = 10000
        end = 12000
        self.df = self.df.iloc[start:end]

        self.viewer = None

        self.lookback_window_size = lookback_window_size
        self.initial_balance = initial_balance

        self.space = spaces.MultiDiscrete([3, 10])
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(10, lookback_window_size + 1), dtype=np.float16)

        self.holding = False

        keys = ['Holding', 'Net_worth', 'Price', 'Date', 'Volume']
        self.run_info = {key: list() for key in keys}


    def _next_observation(self):
        end = self.current_step + self.lookback_window_size + 1
        scaled_df = self.active_df

        obs = np.array([
            scaled_df['Price'].values[self.current_step:end],
            scaled_df['Volume'].values[self.current_step:end],
        ])
        return obs

    def _reset_session(self):
        self.current_step = 0
        self.steps_left = len(self.df) - self.lookback_window_size - 1
        self.frame_start = self.lookback_window_size
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


    def _get_current_price(self):
        return self.df['Price'].values[self.frame_start + self.current_step]


    def update_net_worth(self, current_price):
        diff = (current_price - self.buy_price)
        gain_prc = diff / self.buy_price
        self.net_worth = self.net_worth * (1 + gain_prc)


    def _take_action(self, action, current_price):
        action_type = action

        if self.holding:
            self.update_net_worth(current_price)

        if action_type == 0:
            if not self.holding:  # If we are already holding, do nothing
                self.buy_price = current_price
                # add buy logic here
                self.holding = True  # We are holding

        elif action_type == 1:
            #add sell logic here
            self.holding = False  # We sold everything :)

        self.run_info['Price'].append(current_price)
        self.run_info['Holding'].append(self.holding)
        self.run_info['Net_worth'].append(self.net_worth)
        self.run_info['Date'].append(self.df['date'].values[self.current_step])
        self.run_info['Volume'].append(self.df['Volume'].values[self.current_step])

    def step(self, action):
        current_price = self._get_current_price() + 0.01
        prev_net_worth = self.net_worth

        self._take_action(action, current_price)

        self.steps_left -= 1
        self.current_step += 1

        obs = self._next_observation()
        reward = self.net_worth - prev_net_worth
        if self.net_worth <= 0:
            print("Net worth < 0 => Done")
            done = True
        elif self.steps_left == 0:
            print("Steps left == 0 => Done")
            done = True
            if self.holding:
                diff = (current_price - self.buy_price)
                gain_prc = diff/self.buy_price
                self.net_worth = self.net_worth * (1 + gain_prc)
        else:
            done = False

        if done:
            import joblib
            joblib.dump(self.run_info, "data/run_info.joblib")

        return obs, reward, done, {"steps_left": self.steps_left, "net_worth": self.net_worth}


    def render(self, mode='human', **kwargs):
        if mode == 'system':
            print('Price: ' + str(self._get_current_price()))
            print(
                'Bought: ' + str(self.account_history[2][self.current_step + self.frame_start]))
            print(
                'Sold: ' + str(self.account_history[4][self.current_step + self.frame_start]))
            print('Net worth: ' + str(self.net_worth))

        elif mode == 'human':
            if self.viewer is None:
                self.viewer = BitcoinTradingGraph(
                    self.df, kwargs.get('title', None))

            self.viewer.render(self.frame_start + self.current_step,
                               self.net_worth,
                               self.trades,
                               window_size=self.lookback_window_size)

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
