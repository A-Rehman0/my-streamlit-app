import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Page config (WIDE)
st.set_page_config(page_title="Blue Planet", layout="wide")

# Custom CSS for colors
st.markdown("""
    <style>
    body {
        background-color: #f4f9ff;
    }
    .main {
        background-color: #f4f9ff;
    }
    h2 {
        color: #0a58ca;
    }
    .stButton>button {
        background-color: #0a58ca;
        color: white;
        border-radius: 8px;
    }
    .stDataFrame {
        border: 2px solid #0a58ca;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("## Blue Planet Infosolutions Pvt. Ltd., India")
st.caption("Team Leader: Tade A Rehman")

# Load data
try:
    df = pickle.load(open("data.pkl", "rb"))
except:
    st.error("Error loading file")
    st.stop()

# Basic checks
if 'Date' not in df.columns or 'Intern Name' not in df.columns:
    st.error("Required columns missing")
    st.stop()

# Date cleaning
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

# Remove future dates
today = pd.Timestamp(datetime.today().date())
df = df[df['Date'] <= today]

# Sort
df = df.sort_values("Date")

# ---------------- UI SECTION ----------------
st.markdown("### 🔍 Filter Tasks")

col1, col2 = st.columns(2)

with col1:
    intern = st.selectbox("👤 Select Intern", df['Intern Name'].unique())

intern_df = df[df['Intern Name'] == intern]
dates = intern_df['Date']

with col2:
    selected_date = st.date_input(
        "📅 Select Date",
        value=dates.max().date() if not dates.empty else today.date()
    )

# ---------------- RESULT ----------------
st.markdown("---")
st.markdown("### 📌 Task Details")

result = intern_df[intern_df['Date'] == pd.Timestamp(selected_date)]

if not result.empty:
    st.dataframe(result, use_container_width=True)
else:
    st.warning("No task found for selected date")

# ---------------- FOOTER ----------------
st.markdown("---")

st.link_button(
    "📊 Open Data Collection File",
    "https://docs.google.com/spreadsheets/d/1Y08jTldMTCyUvWUpgNbMb-9WJNbbD-D3/edit?gid=256704825#gid=256704825"
)

st.caption("After completing task, report to Team Leader.")
