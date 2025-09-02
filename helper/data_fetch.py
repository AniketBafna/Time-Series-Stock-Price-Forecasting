from datetime import date
from typing import Tuple
import yfinance as yf
from pandas_datareader import data as web
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data(show_spinner=False)
def get_history(ticker: str, period: str = "5y", start: date | None = None, end: date | None = None) -> pd.DataFrame:
    try:
        if start is not None and end is not None:
            df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        else:
            df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        df = df[['Open','High','Low','Close','Volume']]
        return df.dropna()
    except Exception as e:
        raise RuntimeError(f"yfinance error for {ticker}: {e}")

@st.cache_data(show_spinner=False)
def get_sp500_fred(start: date, end: date) -> pd.DataFrame:
    df = web.DataReader(['sp500'], 'fred', start, end)
    df = df.rename(columns={'sp500':'SP500'}).dropna()
    df.index = pd.to_datetime(df.index)
    return df