import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plotly_render(run_info: dict, html_save_path: str):
    df = pd.DataFrame(run_info).set_index("Date")
    df["Holding"] = df['Holding'].replace(to_replace=False, value=0)
    df["Holding"] = df['Holding'].replace(to_replace=True, value=1)
    print("About to save!")
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True, vertical_spacing=0.02
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Net_worth'], name="Net worth"), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Price'], name="Asset price"), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=np.repeat(df.index, 2)[1:], y=np.repeat(df['Holding'], 2)[:-1], name="Holding", 
                   marker={"color": "green"}, fill='tonexty'), row=3, col=1
    )
    fig.add_trace(
        go.Bar(x=df.index, y=df['Volume'], marker={"color": "black"}, name="Volume"), row=4, col=1
    )
    print("Saving!")
    fig.write_html(html_save_path)
