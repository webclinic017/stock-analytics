import pandas as pd
from policies.baselines import RoundRobin
from env.bitcoin_simple_env import BitcoinTradingEnv

data_path = "data/kaggle_bitcoin_preprocessed.pkl"
env = BitcoinTradingEnv(data_path, html_save_path="data/result.html")
obs = env.reset()

policy = RoundRobin()

while True:
    #print("RUN")
    action = policy(obs)
    obs, reward, done, d = env.step(action)
    print(d["steps_left"], done, d["net_worth"])
    if done:
        break

env.render()