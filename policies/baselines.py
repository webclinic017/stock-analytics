
class RoundRobin:

    turn = 0

    def __call__(self, obs):
        return self.select_action(obs)

    def select_action(self, obs):
        action = self.turn
        self.turn = 1 - self.turn
        return 0