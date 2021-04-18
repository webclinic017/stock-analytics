import pandas as pd
from policies.rsi import BasicRSIAgent
from env.bitcoin_simple_env import BitcoinTradingEnv
from tqdm import tqdm
from datetime import datetime

df = pd.read_csv("./data/kaggle_bitcoin.csv")
df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")
start_date = datetime(year=2019, month=2, day=1)
steps = 2000


env = BitcoinTradingEnv(df, start_date, steps=steps)
obs = env.reset()
policy = BasicRSIAgent()
n_steps = len(env.df)

for i in tqdm(range(n_steps)):
    action = policy(obs)
    obs, reward, done, d = env.step(action)
    if done:
        break

df_res = obs.dropna()
max_gain = df_res['Close'].iloc[0] / df_res['Close'].iloc[-1] * 100
gain = (df_res['net_worth'].iloc[0]/df_res['net_worth'].iloc[-1]) * 100
print("% Capital from start: ", gain)
print("% Bitcoin price: ", max_gain)

policy.render(df_res)
