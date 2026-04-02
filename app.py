import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Blue Planet Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding: 1rem 2rem;
    background-color: #eef5ff;
}

/* HEADER */
.topbar {
    background-color: #0a58ca;
    padding: 14px 20px;
    border-radius: 10px;
    color: white;
    margin-bottom: 20px;
}

/* CARD */
.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}

/* KPI */
.kpi {
    text-align: center;
    padding: 6px 8px;
    border-radius: 10px;
    background: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.kpi h1 {
    color: #0a58ca;
    margin: 0;
    font-size: 20px;
}

.kpi p {
    color: gray;
    font-size: 12px;
    margin: 0;
}

/* SECTION */
.section {
    font-size: 18px;
    font-weight: 600;
    margin: 10px 0;
    color: #0a58ca;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="topbar">
    <h2>🌍 Blue Planet Infosolutions Pvt. Ltd.</h2>
    <p>Intern Task Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
try:
    df = pickle.load(open("data.pkl", "rb"))
except:
    st.error("Error loading file")
    st.stop()

if 'Date' not in df.columns or 'Intern Name' not in df.columns:
    st.error("Missing required columns")
    st.stop()

# ---------------- CLEAN ----------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

today = datetime.now().date()
df = df[df['Date'].dt.date <= today]
df = df.sort_values("Date")

# ---------------- FILTER CARD ----------------
st.markdown('<div class="section">🔍 Filters</div>', unsafe_allow_html=True)

f1, f2 = st.columns([2, 2])

with f1:
    intern = st.selectbox("Select Intern", df['Intern Name'].unique())

intern_df = df[df['Intern Name'] == intern]

# ---------------- DATE (FIXED) ----------------
# Always use today's real-time date
default_date = datetime.now().date()

with f2:
    selected_date = st.date_input("Select Date", value=default_date)

# ---------------- KPI SECTION ----------------
st.markdown('<div class="section">📊 Overview</div>', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)

task_count = len(intern_df)
today_tasks = len(intern_df[intern_df['Date'].dt.date == today])
active_days = intern_df['Date'].dt.date.nunique()

with k1:
    st.markdown(f"""
    <div class="kpi">
        <h1>{task_count}</h1>
        <p>Total Tasks</p>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi">
        <h1>{today_tasks}</h1>
        <p>Today's Tasks</p>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi">
        <h1>{active_days}</h1>
        <p>Active Days</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.markdown('<div class="section">📋 Task Details</div>', unsafe_allow_html=True)

result = intern_df[intern_df['Date'].dt.date == selected_date]

if not result.empty:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(result, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("No tasks found")

# ---------------- FOOTER ----------------
st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    st.link_button(
        "📊 Open Data Sheet",
        "https://docs.google.com/spreadsheets/d/1Y08jTldMTCyUvWUpgNbMb-9WJNbbD-D3/edit?gid=256704825#gid=256704825"
    )

with c2:
    st.link_button(
        "📝 Mark Attendance",
        "https://docs.google.com/forms/d/e/1FAIpQLScHz7fdRGl0RbMTyh_8N5VH9G0K1LDsszsZRqwHMe9CsXcqlA/viewform"
    )

# ---------------- NOTES ----------------
st.markdown("""
<div style='margin-top:10px; color:#0a58ca;'>
✔ After completing tasks, report to Team Leader<br>
✔ Share updates in communication group for HR tracking
</div>
""", unsafe_allow_html=True)
