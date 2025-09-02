from datetime import date
import yfinance as yf
import pandas as pd
import streamlit as st

# -------------------------------
# Historical Stock Data
# -------------------------------
@st.cache_data(show_spinner=False)
def get_history(ticker: str, period: str = "5y", start: date | None = None, end: date | None = None) -> pd.DataFrame:
    """
    Fetch historical stock data (Open, High, Low, Close, Volume) using Yahoo Finance.
    """
    try:
        if start is not None and end is not None:
            df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        else:
            df = yf.download(ticker, period=period, auto_adjust=True, progress=False)

        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        return df.dropna()
    except Exception as e:
        raise RuntimeError(f"yfinance error for {ticker}: {e}")


# -------------------------------
# Benchmark (S&P500, Nifty, etc.)
# -------------------------------
@st.cache_data(show_spinner=False)
def get_benchmark(ticker: str = "^GSPC", start: date | None = None, end: date | None = None) -> pd.DataFrame:
    """
    Fetch benchmark index data (default: S&P 500 - ^GSPC) using Yahoo Finance.
    """
    try:
        df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

        if not df.empty:
            return df[["Close"]].rename(columns={"Close": "Benchmark"})
        else:
            raise ValueError(f"No data found for benchmark {ticker}")
    except Exception as e:
        raise RuntimeError(f"yfinance error fetching benchmark {ticker}: {e}")
