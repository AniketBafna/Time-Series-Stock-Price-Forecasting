import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import ta
from datetime import datetime
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go


def page_capm_dashboard():
    st.markdown(
        """
        <h1 style='text-align: center;'>📊 CAPM Dashboard & Analysis</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("Enter a stock ticker, select a benchmark index, and set a risk-free rate to compute CAPM metrics and visualize returns.")

    # --- Inputs ---
    ticker = st.text_input("Enter Stock Ticker", "AAPL", key="capm_dash_stock").upper().strip()
    benchmark_map = {
        "S&P 500 (US)": "^GSPC",
        "Nasdaq 100 (US)": "^NDX",
        "Dow Jones (US)": "^DJI",
        "Nifty 50 (India)": "^NSEI",
        "Sensex (India)": "^BSESN",
    }
    benchmark_choice = st.selectbox("Select Benchmark Index", list(benchmark_map.keys()), index=0)
    benchmark_symbol = benchmark_map[benchmark_choice]
    rf_rate = st.number_input("Risk-free Rate (%)", value=2.0, step=0.1, key="capm_dash_rf") / 100

    run_analysis = st.button("📊 Run CAPM Analysis")

    if run_analysis and ticker:
        try:
            stock_data = yf.download(ticker, period="5y", progress=False)
            bench_data = yf.download(benchmark_symbol, period="5y", progress=False)
        except Exception as e:
            st.error(f"⚠️ Error fetching data: {e}")
            return

        def get_price_column(data, name):
            if isinstance(data, pd.DataFrame) and not data.empty:
                if "Adj Close" in data.columns:
                    return data["Adj Close"]
                elif "Close" in data.columns:
                    return data["Close"]
            st.error(f"{name}: No valid price column found.")
            return pd.Series([], dtype=float)

        stock = get_price_column(stock_data, ticker)
        bench = get_price_column(bench_data, benchmark_symbol)

        if stock.empty or bench.empty:
            st.warning("⚠️ One of the datasets is empty. Cannot compute CAPM.")
            return

        # --- Align and compute returns ---
        df = pd.concat([stock, bench], axis=1)
        df.columns = ["Stock", "Benchmark"]
        df.dropna(inplace=True)
        df["Stock_Return"] = df["Stock"].pct_change()
        df["Benchmark_Return"] = df["Benchmark"].pct_change()
        df.dropna(inplace=True)

        if df.empty:
            st.error("⚠️ Not enough data to compute CAPM.")
            return

        # --- Regression ---
        X = sm.add_constant(df["Benchmark_Return"])
        y = df["Stock_Return"]
        model = sm.OLS(y, X).fit()

        alpha = model.params["const"]
        beta = model.params["Benchmark_Return"]
        expected_return = rf_rate + beta * (df["Benchmark_Return"].mean() * 252)

        # --- Metrics ---
        st.subheader(f"CAPM Metrics for {ticker} vs {benchmark_choice}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Alpha (α)", f"{alpha:.4f}")
        col2.metric("Beta (β)", f"{beta:.4f}")
        col3.metric("Expected Return", f"{expected_return*100:.2f}%")
        col4.metric("R²", f"{model.rsquared:.4f}")
        st.write(f"**p-value (Beta):** {model.pvalues['Benchmark_Return']:.4f}")

        st.info(
            "📌 **Beta Interpretation:**\n"
            "- Beta > 1 → Stock is more volatile than the market\n"
            "- Beta < 1 → Stock is less volatile than the market\n"
            "- Beta < 0 → Stock moves inversely to the market"
        )

        # --- Tabs ---
        tab1, tab2 = st.tabs(["📉 Regression Scatter", "📊 Historical Daily Returns"])

        with tab1:
            fig = px.scatter(df, x="Benchmark_Return", y="Stock_Return", opacity=0.6,
                             title=f"CAPM Regression: {ticker} vs {benchmark_choice}")
            fig.add_trace(go.Scatter(x=df["Benchmark_Return"], y=model.predict(X),
                                     mode="lines", name="Regression Line", line=dict(color="red")))
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df["Stock_Return"], mode="lines", name=f"{ticker} Returns"))
            fig2.add_trace(go.Scatter(x=df.index, y=df["Benchmark_Return"], mode="lines", name=f"{benchmark_choice} Returns"))
            fig2.update_layout(title="Stock vs Benchmark Returns (Daily %)",
                               xaxis_title="Date", yaxis_title="Daily Return",
                               template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

        with st.expander("📄 Regression Summary"):
            st.text(model.summary())
