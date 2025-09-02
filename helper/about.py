import streamlit as st

def page_about():
    st.markdown(
        """
        <h1 style='text-align: center;'>
            ℹ️ About this Project
        </h1>
        """,
        unsafe_allow_html=True
    )
    

    st.write("""
    **Stock Forecasting & Analysis** is a portfolio-ready application that combines
    **financial data analytics** 📊 with **machine learning forecasting** 🤖.

    ### 🔑 Features
    - 📥 Data ingestion from **Yahoo Finance** & **FRED**
    - 📈 Technical & fundamental **stock analysis**
    - 📊 CAPM analytics (**Beta & Expected Return**)
    - ⏳ Time-series forecasting with **ARIMA, Holt-Winters, Moving Average & Prophet**
    - 📉 Backtesting with **RMSE & R2**
    - 🎨 Modern, interactive dashboard with **Plotly + Streamlit**
    """)

    st.markdown("### 🛠 Tech Stack")
    st.markdown("""
    - **Frontend/UI:** Streamlit 🚀  
    - **Visualization:** Plotly 📊  
    - **Data Sources:** yfinance, FRED API  
    - **ML/Stats:** pandas, numpy, statsmodels  
    """)

    st.markdown("---")
    #st.success("👨‍💻 Built by **Aniket Bafna**")

    # Author Footer
    st.markdown(
        """
        <div style="text-align: center; font-size: 16px; margin-top: 20px;">
            Built with ❤️ by <b>Aniket Bafna</b>  
            <br>
            <a href="https://github.com/AniketBafna" target="_blank">GitHub</a> • 
            <a href="https://linkedin.com/in/aniket-bafna/" target="_blank">LinkedIn</a> • 
            <a href="https://www.datascienceportfol.io/aniketbafna" target="_blank">Portfolio</a>
        </div>
        """,
        unsafe_allow_html=True
    )