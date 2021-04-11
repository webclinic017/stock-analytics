import pandas as pd
from policies.baselines import RoundRobin
from env.bitcoin_simple_env import BitcoinTradingEnv

data_path = "data/kaggle_bitcoin_preprocessed.pkl"
env = BitcoinTradingEnv(data_path)
obs = env.reset()

policy = RoundRobin()

while True:
    #print("RUN")
    action = policy(obs)
    obs, reward, done, _, steps_left, net_worth = env.step(action)
    print(steps_left, done, net_worth)
    if done:
        break

