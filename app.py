import streamlit as st
from helper.data_fetch import get_history, get_sp500_fred
from helper.home import page_home
from helper.page_analysis import page_analysis
from helper.page_prediction import page_prediction
from helper.cpam_dashboard import page_capm_dashboard
from helper.about import page_about
from helper.style_utils import load_global_css

# -------------------------------
# Page Config & Global Styling
# -------------------------------
st.set_page_config(page_title="Stock Forecasting & Analysis", page_icon="📊", layout="wide")
load_global_css()

# -------------------------------
# Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.markdown("## 💼 Aniket’s Stock Dashboard")
    page = st.radio("Navigate", ["🏠 Home", "🔍 Stock Analysis", "📉 Prediction", "📊 CAPM Dashboard", "ℹ️ About"], index=0)
    
# -------------------------------
# Router
# -------------------------------
if page == "🏠 Home":
    page_home()
elif page == "🔍 Stock Analysis":
    page_analysis()
elif page == "📉 Prediction":
    page_prediction()
elif page == "📊 CAPM Dashboard":
    page_capm_dashboard()
else:
    page_about()
