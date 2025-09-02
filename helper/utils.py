from typing import Tuple
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

def normalize_prices(df: pd.DataFrame) -> pd.DataFrame:
    base = df.iloc[0]
    return df / base

def daily_return(price_df: pd.DataFrame) -> pd.DataFrame:
    dr = price_df.pct_change().dropna()
    return dr

def calc_beta_alpha(returns_df: pd.DataFrame, stock_col: str, market_col: str = 'SP500') -> Tuple[float, float]:
    x = returns_df[market_col].values
    y = returns_df[stock_col].values
    # add guard
    if len(x) < 3 or len(y) < 3:
        return float('nan'), float('nan')
    b, a = np.polyfit(x, y, 1)
    return float(b), float(a)

def line_table(df: pd.DataFrame, height: int | None = 280):
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Date'] + list(df.columns),
                    fill_color='#0ea5e9', font=dict(color='white', size=12), align='left'),
        cells=dict(values=[df.index.strftime('%Y-%m-%d')] + [df[c] for c in df.columns],
                   fill_color='#0b1020', align='left'))
    ])
    if height:
        fig.update_layout(height=height)
    return fig

def metric_card(title: str, value: str, delta: str | None = None):
    with st.container():
        st.markdown(f'<div class="metric-card"><div style="font-size:13px;color:#93c5fd">{title}</div><div style="font-size:22px;font-weight:700;margin-top:4px">{value}</div>{f"<div style=\'color:#94a3b8;margin-top:4px\'>{delta}</div>" if delta else ""}</div>', unsafe_allow_html=True)
