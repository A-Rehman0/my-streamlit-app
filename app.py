import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Blue Planet", layout="wide")

# ---------------- HIDE DEFAULT UI ----------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[title="View code"] {visibility: hidden !important;}
.block-container {padding: 1rem 2rem;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body { background-color: #f4f9ff; }
.main { background-color: #f4f9ff; }

h2 { color: #0a58ca; }

.stButton>button {
    background-color: #0a58ca;
    color: white;
    border-radius: 8px;
}

.stDataFrame {
    border: 2px solid #0a58ca;
    border-radius: 10px;
}

/* Metric Styling */
[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 2px solid #0a58ca;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("## 🌍 Blue Planet Infosolutions Pvt. Ltd., India")
st.caption("Team Leader: Tade A Rehman")

# ---------------- LOAD DATA ----------------
try:
    df = pickle.load(open("data.pkl", "rb"))
except:
    st.error("❌ Error loading data file")
    st.stop()

# ---------------- VALIDATION ----------------
if 'Date' not in df.columns or 'Intern Name' not in df.columns:
    st.error("❌ Required columns missing (Date / Intern Name)")
    st.stop()

# ---------------- CLEAN DATA ----------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

today = datetime.now().date()

# Remove future dates
df = df[df['Date'].dt.date <= today]

# Sort data
df = df.sort_values("Date")

# ---------------- UI FILTER ----------------
st.markdown("### 🔍 Filter Tasks")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    intern = st.selectbox("👤 Select Intern", df['Intern Name'].unique())

# Filter intern data
intern_df = df[df['Intern Name'] == intern]

# ---------------- TASK COUNT ----------------
tasks_till_today = intern_df[intern_df['Date'].dt.date <= today]
task_count = len(tasks_till_today)

with col3:
    st.metric("📊 Total Tasks", task_count)

# ---------------- DATE LOGIC ----------------
dates = intern_df['Date']

default_date = today
if not dates.empty:
    available_dates = dates.dt.date.unique()
    if today not in available_dates:
        default_date = dates.max().date()

# ---------------- SESSION STATE ----------------
if "init_done" not in st.session_state:
    st.session_state.selected_date = default_date
    st.session_state.last_intern = intern
    st.session_state.init_done = True

if st.session_state.last_intern != intern:
    st.session_state.selected_date = default_date
    st.session_state.last_intern = intern

with col2:
    selected_date = st.date_input(
        "📅 Select Date",
        value=st.session_state.selected_date,
        key="date_widget"
    )

st.session_state.selected_date = selected_date

# ---------------- RESULT ----------------
st.markdown("---")
st.markdown("### 📌 Task Details")

result = intern_df[intern_df['Date'].dt.date == selected_date]

if not result.empty:
    st.dataframe(result, use_container_width=True)
else:
    if selected_date == today:
        st.info("ℹ️ No tasks uploaded for today yet")
    else:
        st.warning("⚠️ No task found for selected date")

# ---------------- FOOTER ----------------
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.link_button(
        "📊 Open Data Sheet",
        "https://docs.google.com/spreadsheets/d/1Y08jTldMTCyUvWUpgNbMb-9WJNbbD-D3/edit?gid=256704825#gid=256704825"
    )

with col2:
    st.link_button(
        "📝 Mark Attendance",
        "https://docs.google.com/forms/d/e/1FAIpQLScHz7fdRGl0RbMTyh_8N5VH9G0K1LDsszsZRqwHMe9CsXcqlA/viewform"
    )

# ---------------- NOTES ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        "<p style='color:#0a58ca; font-weight:500;'>📝 After completing task, report to Team Leader.</p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<p style='color:#0a58ca; font-weight:500;'>📝 Share your task updates in the communication group for HR tracking.</p>",
        unsafe_allow_html=True
    )
