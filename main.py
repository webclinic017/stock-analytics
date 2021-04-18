import pandas as pd
from policies.Scalping import scalpingAgent
from policies.rsi import BasicRSIAgent
from env.bitcoin_simple_env import BitcoinTradingEnv
from tqdm import tqdm
from datetime import datetime

df = pd.read_csv("./data/kaggle_bitcoin.csv")
df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")
start_date = datetime(year=2015, month=2, day=1)
steps = 45000


env = BitcoinTradingEnv(df, start_date, steps=steps)
obs = env.reset()
policy = BasicRSIAgent()
policy2 = scalpingAgent()
n_steps = len(env.df)

for i in tqdm(range(n_steps)):
    #action = policy(obs)
    action = policy2(obs)
    obs, reward, done, d = env.step(action)
    if done:
        break

df_res = obs.dropna()
max_gain = df_res['Close'].iloc[-1]/df_res['Close'].iloc[0] * 100
gain = df_res['net_worth'].iloc[-1]/ df_res['net_worth'].iloc[0] * 100
print("% Capital from start: ", df_res['net_worth'].iloc[0])
print("% Capital at end: ", df_res['net_worth'].iloc[-1])
print("% Bitcoin trading yield in : ", gain)
print("% Bitcoin no actions %: ", max_gain)


policy.render(df_res)
