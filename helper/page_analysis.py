import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import ta
from datetime import datetime

# ---------------- Utils ----------------
def format_market_cap(value, symbol="$"):
    """Format market cap with 2 decimals and unit suffix."""
    if value is None or (isinstance(value, float) and np.isnan(value)) or value == 0:
        return "—"
    trillion = 1_000_000_000_000
    billion = 1_000_000_000
    million = 1_000_000
    if value >= trillion:
        return f"{symbol}{value/trillion:.2f} T"
    if value >= billion:
        return f"{symbol}{value/billion:.2f} B"
    if value >= million:
        return f"{symbol}{value/million:.2f} M"
    return f"{symbol}{value:,.2f}"

def to_human_date(ts):
    """Handle yfinance returning int timestamp or list-like."""
    if ts is None:
        return "—"
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts).strftime("%b %d, %Y")
        if isinstance(ts, (list, tuple)) and ts:
            v = ts[0]
            if isinstance(v, (int, float)):
                return datetime.fromtimestamp(v).strftime("%b %d, %Y")
            return str(v)
        return str(ts)
    except Exception:
        return str(ts)

# -------------- Page -------------------
def page_analysis():
    
    st.markdown(
        """
        <h1 style='text-align: center;'>
            📊 Stock Analysis
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Inputs
    ticker = st.text_input("Ticker", "AAPL", key="analysis_ticker").upper().strip()
    period = st.selectbox("Select Period", ["1y", "5y", "10y", "max"], index=1, key="analysis_period")

    # Indicator selection
    indicators = st.multiselect(
        "Add Technical Indicators",
        ["SMA (20)", "SMA (50)", "EMA (20)", "Bollinger Bands", "RSI"],
        default=[]
    )

    # Trigger
    search_clicked = st.button("🔍 Search Stock", key="analysis_search")

    if not search_clicked:
        st.info("Enter a ticker, choose period/indicators, then click **Search Stock**.")
        return

    if not ticker:
        st.warning("Please enter a ticker symbol.")
        return

    # Download + info
    with st.spinner("Fetching market data..."):
        try:
            data = yf.download(ticker, period=period, progress=False)
            stock = yf.Ticker(ticker)
            try:
                info = stock.get_info()  # new yfinance
            except Exception:
                info = stock.info       # fallback
                if not isinstance(info, dict):
                    info = {}
        except Exception as e:
            st.error(f"⚠️ Error downloading data for {ticker}: {e}")
            return

    if data.empty:
        st.warning("⚠️ No data found for this ticker.")
        return

    # Handle MultiIndex (if user accidentally passed multi-ticker)
    if isinstance(data.columns, pd.MultiIndex):
        try:
            data = data.xs(ticker, axis=1, level=1)
        except Exception:
            data.columns = data.columns.get_level_values(0)

    # Ensure essential columns
    required_cols = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in data.columns for col in required_cols):
        st.error("Downloaded data is missing one or more required columns.")
        return

    # Numeric coercion
    for col in ["Open", "High", "Low", "Close"]:
        data[col] = pd.to_numeric(data[col], errors="coerce").round(2)
    data["Volume"] = pd.to_numeric(data["Volume"], errors="coerce")

    # Add indicators
    if "SMA (20)" in indicators:
        data["SMA20"] = data["Close"].rolling(20).mean()
    if "SMA (50)" in indicators:
        data["SMA50"] = data["Close"].rolling(50).mean()
    if "EMA (20)" in indicators:
        data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()
    if "Bollinger Bands" in indicators:
        mid = data["Close"].rolling(20).mean()
        std = data["Close"].rolling(20).std()
        data["BB_MID"] = mid
        data["BB_UPPER"] = mid + 2 * std
        data["BB_LOWER"] = mid - 2 * std
    if "RSI" in indicators:
        data["RSI"] = ta.momentum.RSIIndicator(data["Close"], window=14).rsi()

    # ===== Metrics row =====
    last_close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2] if len(data) > 1 else np.nan
    delta = last_close - prev_close if pd.notna(prev_close) else 0.0
    delta_pct = (delta / prev_close * 100) if pd.notna(prev_close) else 0.0

    m1, m2, m3 = st.columns(3)
    with m1:
        color = "🟢" if delta >= 0 else "🔴"
        st.metric("Last Close", f"{last_close:,.2f}", f"{color} {delta:+.2f} ({delta_pct:+.2f}%)")
    with m2:
        h52 = data["Close"].rolling(252).max().iloc[-1]
        st.metric("52W High (from price series)", f"{h52:,.2f}" if pd.notna(h52) else "—")
    with m3:
        l52 = data["Close"].rolling(252).min().iloc[-1]
        st.metric("52W Low (from price series)", f"{l52:,.2f}" if pd.notna(l52) else "—")

    # ===== Fundamentals snapshot =====
    st.subheader("📑 Stock Fundamentals")

    # Currency detection for symbols
    currency = info.get("currency", "USD")
    is_india = (currency == "INR") or ticker.endswith(".NS") or ticker.endswith(".BO")
    symbol = "₹" if is_india else "$"

    div_yield = info.get("dividendYield", 0)  # 0-1
    div_rate = info.get("dividendRate", None)
    ex_div = info.get("exDividendDate", None)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.metric("Market Cap", format_market_cap(info.get("marketCap"), symbol))
        st.metric("P/E Ratio (TTM)", f"{info.get('trailingPE', 0):.2f}" if info.get("trailingPE") else "—")
        st.metric("EPS (TTM)", f"{info.get('trailingEps', 0):.2f}" if info.get("trailingEps") else "—")

    with f2:
        st.metric("Beta (5Y Monthly)", f"{info.get('beta', 0):.2f}" if info.get("beta") is not None else "—")
        if div_yield:
            if div_rate is None:
                st.metric("Forward Dividend & Yield", f"— ({div_yield:.2f}%)")
            else:
                st.metric("Forward Dividend & Yield", f"{div_rate:.2f} ({div_yield:.2f}%)")
        else:
            st.metric("Forward Dividend & Yield", "—")
        st.metric("Ex-Dividend Date", to_human_date(ex_div))

    with f3:
        st.metric("52 Week High", f"{info.get('fiftyTwoWeekHigh', 0):.2f}" if info.get("fiftyTwoWeekHigh") else "—")
        st.metric("52 Week Low", f"{info.get('fiftyTwoWeekLow', 0):.2f}" if info.get("fiftyTwoWeekLow") else "—")
        st.metric("1y Target Est", f"{info.get('targetMeanPrice', 0):.2f}" if info.get("targetMeanPrice") else "—")

    st.markdown("---")

    # ===== Chart =====
    chart_type = st.radio("Select Chart Type", ["Line", "Candlestick"], index=0, horizontal=True)

    if chart_type == "Line":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close"))
        if "SMA (20)" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data["SMA20"], mode="lines", name="SMA 20"))
        if "SMA (50)" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data["SMA50"], mode="lines", name="SMA 50"))
        if "EMA (20)" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], mode="lines", name="EMA 20"))
        if "Bollinger Bands" in indicators:
            fig.add_trace(go.Scatter(x=data.index, y=data["BB_UPPER"], mode="lines", name="BB Upper", line=dict(dash="dot")))
            fig.add_trace(go.Scatter(x=data.index, y=data["BB_LOWER"], mode="lines", name="BB Lower", line=dict(dash="dot")))
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name="Candlestick"
        )])
        st.plotly_chart(fig, use_container_width=True)

    # ===== RSI =====
    if "RSI" in indicators:
        st.subheader("RSI (Relative Strength Index)")
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI"))
        fig_rsi.add_hline(y=70, line_dash="dot")
        fig_rsi.add_hline(y=30, line_dash="dot")
        st.plotly_chart(fig_rsi, use_container_width=True)

    # ===== Recent Data =====
    st.subheader("Recent Data")
    st.dataframe(data.tail(10))