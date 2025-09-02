# Time-Series-Stock-Price-Forecasting
📈 An interactive Streamlit-based dashboard for stock market analysis, CAPM insights, and time-series forecasting.
This project demonstrates financial analytics, forecasting models, and visualization in a modern and intuitive UI.

🚀 Features

Stock Analysis

Fetch live historical data from Yahoo Finance

Interactive Line & Candlestick charts

Add Technical Indicators (SMA, EMA, RSI, Bollinger Bands)

Fundamentals snapshot (Market Cap, P/E, Dividend Yield, etc.)

Forecasting

Multiple models: ARIMA, Holt-Winters, Prophet, Moving Average

Forecast future stock prices with confidence intervals

Compare historical vs forecasted trends

CAPM Analysis

Compute Alpha, Beta, and Expected Return

Regression scatter with trendline

Stock vs Benchmark return comparison

Regression summary for deeper insights

Modern UI

Built with Streamlit & Plotly

Sidebar navigation for quick access

Dark/Light mode support (optional)

🛠️ Tech Stack

Frontend / Dashboard: Streamlit
, Plotly

Data Sources: yfinance
, FRED

Analytics & Models: pandas, numpy, statsmodels, Prophet, ta (Technical Analysis Library)

Visualization: Plotly, Streamlit native components

📂 Project Structure
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── assets/               # (Optional) Images, screenshots

⚙️ Installation & Setup

Clone the repository:

git clone https://github.com/yourusername/stock-forecasting-analysis.git
cd stock-forecasting-analysis


Create virtual environment & install dependencies:

pip install -r requirements.txt


Run the Streamlit app:

streamlit run app.py

📊 Example Workflow

Enter a stock ticker (e.g., AAPL)

Explore historical performance with charts + indicators

Forecast future prices using time-series models

Evaluate risk-return metrics with CAPM

👨‍💻 Author

Aniket Bafna
📌 GitHub
 | LinkedIn
 | Portfolio
