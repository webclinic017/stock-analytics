import pandas as pd
from policies.rsi import BasicRSIAgent
from policies.ema import EMA
from policies.sandbox_env import SandboxAgent

from env.bitcoin_simple_env import BitcoinTradingEnv
from env.percentage_env import PercentageEnv
from tqdm import tqdm
from datetime import datetime


df = pd.read_csv("./data/kaggle_bitcoin.csv")
df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")
start_date = datetime(year=2020, month=2, day=1)
steps = 2000
df["Date"] = df.Date.values.astype(dtype="datetime64[h]")
df = df.drop_duplicates(subset="Date")
# df.set_index("Date", inplace=True)

# env = BitcoinTradingEnv(df, start_date, steps=steps)
env = PercentageEnv(df, start_date, steps=steps)
obs = env.reset()
policy = SandboxAgent()

# policy = EMA()
# policy = BasicRSIAgent()
n_steps = len(env.df)

for i in tqdm(range(n_steps)):
    action = policy(obs)
    obs, reward, done, d = env.step(action)
    if done:
        break

df_res = obs.dropna()
max_gain = df_res['Close'].iloc[-1] / df_res['Close'].iloc[0] * 100
gain = (df_res['net_worth'].iloc[-1]/df_res['net_worth'].iloc[0]) * 100
print("% Capital from start: ", gain)
print("% Bitcoin price: ", max_gain)

# policy.render(df_res)
