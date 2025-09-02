import streamlit as st
from PIL import Image

def page_home():
    # Hero Section
    st.markdown(
    """
    <div style="text-align: center; padding: 25px 0;">
        <h1 style="font-size: 50px; margin-bottom: 0;">📈 Stock Forecasting & Analysis</h1>
        <p style="font-size: 20px; color: #9ca3af; margin-top: 8px;">
            Interactive dashboard for stock insights, CAPM analysis, and AI-powered forecasting.
        </p>
        <hr style="margin-top:20px; margin-bottom:20px; border:none; height:1px; 
                   background: linear-gradient(90deg, transparent, #38bdf8, transparent);">
    </div>
    """,
    unsafe_allow_html=True
    )

    image = Image.open("assets/bull.png")
    resized_image = image.resize((1000, 400))

    # Display in Streamlit
    st.image(resized_image,use_container_width=True)

    # Project Summary
    st.markdown(
        """
        ### ✨ What this App Does
        - Explore **historical stock performance** with interactive charts  
        - Analyze **technical indicators** (SMA, EMA, RSI, Bollinger Bands)  
        - Perform **CAPM analysis** (Beta & Expected Return)  
        - Forecast **future stock prices** with ARIMA & Holt-Winters models  
        - Visualize results with **Plotly** in an intuitive **Streamlit UI**
        """
    )

    st.markdown("---")

    # Author Footer
    st.markdown(
        """
        <div style="text-align: center; font-size: 16px; margin-top: 20px;">
            Built with ❤️ by <b>Aniket Bafna</b>  
            <br>
            <a href="https://github.com/yourusername" target="_blank">GitHub</a> • 
            <a href="https://www.linkedin.com/in/yourprofile/" target="_blank">LinkedIn</a> • 
            <a href="https://yourportfolio.com" target="_blank">Portfolio</a>
        </div>
        """,
        unsafe_allow_html=True
    )
