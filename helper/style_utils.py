# style_utils.py
import streamlit as st

def load_global_css():
    GLOBAL_CSS = """
    <style>
    :root { --primary:#0ea5e9; --bg:#0b1020; --card:#111827; --text:#e5e7eb; --muted:#94a3b8; }
    html, body, [data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0b1020 0%, #0f172a 100%); }
    h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }
    p, li, label, span, div { color: #dbeafe; }
    .sidebar .sidebar-content { background-color:#0b1020 !important; }
    .block-container { padding-top:2rem; padding-bottom:2rem; }
    .metric-card {
      background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
      border-radius:18px; padding:18px; box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    }
    hr { border:none; height:1px; background: linear-gradient(90deg, transparent, #38bdf8, transparent); }
    .footer { color:#94a3b8; font-size:12px; text-align:center; margin-top:32px; }
    .link { color:#38bdf8; text-decoration:none; }
    .info-chip {
      display:inline-block; padding:6px 10px; border-radius:999px; border:1px solid rgba(255,255,255,0.12);
      background: rgba(14,165,233,0.12); color:#e0f2fe; font-size:12px; margin-right:8px;
    }
    </style>
    """
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
