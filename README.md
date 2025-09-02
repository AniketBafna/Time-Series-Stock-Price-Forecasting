# 📈 Stock Forecasting & Analysis

An interactive **Streamlit dashboard** for **stock analysis, forecasting, and CAPM-based evaluation**.  
This project combines **financial data analytics** 📊, **machine learning forecasting** 🤖, and **risk-return modeling** to help investors and analysts make informed decisions.  

---

## 🚀 Features

- 📥 **Data Ingestion**: Fetch historical data from **Yahoo Finance** & **FRED API**  
- 📊 **Stock Analysis**: Technical indicators (SMA, EMA, RSI, Bollinger Bands)  
- 📑 **Fundamentals Snapshot**: Market Cap, PE Ratio, EPS, Dividend, etc.  
- 📈 **Forecasting**: Time series models (ARIMA, Holt-Winters, Prophet, Moving Average)  
- 🧮 **CAPM Analysis**: Beta, Alpha, and Expected Return with regression plots  
- 📉 **CAPM Dashboard**: Compare stock vs benchmark with scatter & return plots  
- 🎨 **Modern UI**: Built with Streamlit + Plotly, styled for a professional look  

---

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/) 🚀  
- **Visualization**: [Plotly](https://plotly.com/python/) 📊  
- **Data Sources**: [yfinance](https://pypi.org/project/yfinance/), [FRED API](https://fred.stlouisfed.org/)  
- **ML/Stats**: pandas, numpy, statsmodels, Prophet, scikit-learn  
- **Others**: TA-Lib (technical indicators), matplotlib  

---

## 📂 Project Structure

```
├── app.py                # Main Streamlit app
├── assets/               # Logos, static images
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/stock-forecasting-analysis.git
   cd stock-forecasting-analysis
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

This will open the dashboard in your browser at **http://localhost:8501/** 🌐  

---

## 📊 Usage

1. **🏠 Home** → Overview of the app  
2. **🔍 Stock Analysis** → Enter ticker, view charts, indicators, and fundamentals  
3. **📉 Prediction** → Forecast stock prices with ARIMA, Holt-Winters, Prophet  
4. **📈 CAPM Return** → Compute expected return with CAPM formula  
5. **β CAPM Beta** → Estimate Beta & Alpha relative to benchmark indices  
6. **📊 CAPM Dashboard** → Regression scatter + historical returns visualization  
7. **ℹ️ About** → Project info & credits  

---

## 📸 Screenshots

| Stock Analysis | Prediction | CAPM Dashboard |
|----------------|------------|----------------|
| ![Stock Analysis](assets/stock_analysis.png) | ![Prediction](assets/prediction.png) | ![CAPM Dashboard](assets/capm_dashboard.png) |

---

## 🧮 Example

- **Ticker**: `AAPL`  
- **Model**: ARIMA (5,1,0)  
- **Forecast Horizon**: 30 days  
- **CAPM**: Beta = 1.2, Expected Return ≈ 12% annually  

---

## 📌 Future Enhancements

- ✅ Add LSTM/Deep Learning models for forecasting  
- ✅ Portfolio optimization module  
- ✅ More benchmarks (global indices, crypto)  
- ✅ Dockerize for deployment  

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to fork this repo and submit a **pull request** with improvements.  


---

## 👨‍💻 Author

**Aniket Bafna**  
- [GitHub](https://github.com/AniketBafna)  
- [LinkedIn](https://linkedin.com/in/aniket-bafna/)  
- [Portfolio](https://www.datascienceportfol.io/aniketbafna)  

---

⭐ If you like this project, consider giving it a **star** on GitHub! ⭐
