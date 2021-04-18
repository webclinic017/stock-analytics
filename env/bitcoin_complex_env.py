from abc import ABC

import gym
from env.bitcoin_simple_env import BitcoinTradingEnv

from gym import spaces
import pandas as pd
import numpy as np
from datetime import datetime
"""
Actions: Make a bet between 0 and 1.
"""


class ComplexBTCEnv(BitcoinTradingEnv, ABC):

    def _take_action(self, action, current_price):

        action = float(action)
        action_type = action  # action = size

        if self.holding:
            self.update_net_worth(current_price)

        self.previous_price = current_price

        if action_type == 2:
            self.holding = True  # We are holding

        elif action_type == 0:
            assert 0 < action < 1 or round(action) == action
            #self.holding = False  # We sold everything :)

