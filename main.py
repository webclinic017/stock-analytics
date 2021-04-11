import pandas as pd
from policies.baselines import RoundRobin
from env.bitcoin_simple_env import BitcoinTradingEnv
from tqdm import tqdm


data_path = "data/kaggle_bitcoin_preprocessed.pkl"
env = BitcoinTradingEnv(data_path, html_save_path="data/result.html", debug=False)
obs = env.reset()

policy = RoundRobin()
n_steps = len(env.df)

for i in tqdm(range(n_steps)):
    action = policy(obs)
    obs, reward, done, d = env.step(action)
    if done:
        break


env.render()