import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import ta
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
from prophet import Prophet
from helper.utils import normalize_prices, daily_return, calc_beta_alpha, line_table, metric_card

def page_prediction():

    st.markdown(
        """
        <h1 style='text-align: center;'>
            📈 Stock Prediction
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Stock ticker input
    ticker = st.text_input("Enter Stock Ticker", "AAPL", key="prediction_ticker").upper().strip()

    # Forecast horizon slider
    horizon = st.slider("Forecast Horizon (days)", 7, 60, 30, step=1, key="prediction_horizon")

    # Model selector
    model_choice = st.selectbox(
        "Choose Forecast Model",
        ["Holt-Winters", "ARIMA", "Moving Average", "Prophet"],
        index=0,
        key="prediction_model_choice"
    )

    # Run Forecast button
    run_forecast = st.button("🚀 Run Forecast", key="run_forecast_button")

    if run_forecast:
        if not ticker:
            st.warning("⚠️ Please enter a stock ticker.")
            return
        ...


        # Download historical data
        data = yf.download(ticker, period="2y")

        if data.empty:
            st.error("⚠️ No data found for this ticker.")
            return

        # Handle MultiIndex from yfinance
        if isinstance(data.columns, pd.MultiIndex):
            try:
                data = data.xs(ticker, axis=1, level=1)
            except Exception:
                data.columns = data.columns.get_level_values(0)

        if "Close" not in data.columns:
            st.error("No 'Close' column found in data.")
            return

        series = data["Close"].dropna()

        forecast, lower_ci, upper_ci = None, None, None

        try:
            # Holt-Winters
            if model_choice == "Holt-Winters":
                model = ExponentialSmoothing(series, trend="add", seasonal=None)
                fit = model.fit()
                forecast = fit.forecast(horizon)
                resid_std = np.std(fit.resid)
                lower_ci = forecast - 1.96 * resid_std
                upper_ci = forecast + 1.96 * resid_std

            # ARIMA
            elif model_choice == "ARIMA":
                model = ARIMA(series, order=(5, 1, 0))
                fit = model.fit()
                res = fit.get_forecast(steps=horizon)
                forecast = res.predicted_mean
                ci = res.conf_int(alpha=0.05)
                lower_ci, upper_ci = ci.iloc[:, 0], ci.iloc[:, 1]

            # Moving Average
            elif model_choice == "Moving Average":
                forecast = pd.Series([series.tail(20).mean()] * horizon)
                lower_ci = forecast * 0.95
                upper_ci = forecast * 1.05

            # Prophet
            elif model_choice == "Prophet":
                df = pd.DataFrame({"ds": series.index, "y": series.values})
                model = Prophet(daily_seasonality=True)
                model.fit(df)

                future = model.make_future_dataframe(periods=horizon, freq="B")
                forecast_df = model.predict(future)

                forecast = forecast_df.set_index("ds")["yhat"].iloc[-horizon:]
                lower_ci = forecast_df.set_index("ds")["yhat_lower"].iloc[-horizon:]
                upper_ci = forecast_df.set_index("ds")["yhat_upper"].iloc[-horizon:]

        except Exception as e:
            st.error(f"⚠️ Forecast model failed: {e}")
            return

        # === Ensure forecast is valid floats ===
        if forecast is None or forecast.empty:
            st.error("⚠️ Forecast is empty. Try another model or ticker.")
            return

        forecast = pd.Series(forecast, dtype="float64")
        if lower_ci is not None and upper_ci is not None:
            lower_ci = pd.Series(lower_ci, index=forecast.index, dtype="float64")
            upper_ci = pd.Series(upper_ci, index=forecast.index, dtype="float64")

        # Assign future business-day index if missing
        if not isinstance(forecast.index, pd.DatetimeIndex):
            last_date = series.index[-1]
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=len(forecast),
                freq="B"
            )
            forecast.index = future_dates
            if lower_ci is not None and upper_ci is not None:
                lower_ci.index = upper_ci.index = future_dates

        # Forecast DataFrame
        fc_df = pd.DataFrame({"Forecast": forecast})
        if lower_ci is not None and upper_ci is not None:
            fc_df["Lower CI"] = lower_ci
            fc_df["Upper CI"] = upper_ci

        # === Forecast Table ===
        st.subheader("📊 Forecast Table")
        st.plotly_chart(line_table(fc_df.round(3)), use_container_width=True)

        # === Historical vs Forecast Chart ===
        st.subheader("📉 Historical vs Forecast")
        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(
            x=series.tail(200).index,
            y=series.tail(200).values,
            mode="lines",
            name="Historical"
        ))

        # Forecast line
        fig.add_trace(go.Scatter(
            x=forecast.index,
            y=forecast.values,
            mode="lines+markers",
            name="Forecast",
            line=dict(dash="dot")
        ))

        # Confidence interval
        if lower_ci is not None and upper_ci is not None:
            fig.add_traces([
                go.Scatter(
                    x=forecast.index,
                    y=upper_ci,
                    mode="lines",
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    x=forecast.index,
                    y=lower_ci,
                    mode="lines",
                    line=dict(width=0),
                    fill="tonexty",
                    fillcolor="rgba(14,165,233,0.2)",
                    name="95% Confidence Interval"
                )
            ])

        fig.update_layout(
            height=420,
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)