from .bitcoin_simple_env import BitcoinTradingEnv


class PercentageEnv(BitcoinTradingEnv):

    """
    In this environment an action is a float in the closed range [0, 1].
    The action describes the % of the portfolio that should be allocated.
    """

    def reset(self):
        self.holding = 0  # Between 0 and 1
        self._reset_session()
        return self._next_observation()

    def _update_net_worth(self, holding, current_price):
        diff = (current_price - self.previous_price)
        gain_prc = diff / self.previous_price

        holding_worth = holding * self.net_worth
        not_holding = self.net_worth - holding_worth
        updated_holding_worth = holding_worth * (1 + gain_prc)
        self.net_worth = not_holding + updated_holding_worth


    def _take_action(self, action, current_price):
        action_type = action

        if self.holding != 0:
            self._update_net_worth(self.holding, current_price)
        self.previous_price = current_price

        self.holding = action

