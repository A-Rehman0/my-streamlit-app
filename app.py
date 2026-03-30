import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

st.title("Intern Schedule Lookup")

# Load Pickle file
file_path = "data.pkl"  # replace with your actual path
try:
    with open(file_path, 'rb') as f:
        obj = pickle.load(f)
except FileNotFoundError:
    st.error("Pickle file not found. Please check the path.")
    st.stop()
except Exception as e:
    st.error(f"Error loading Pickle file: {e}")
    st.stop()

# Ensure the loaded object is a DataFrame
if isinstance(obj, pd.DataFrame):
    df = obj
else:
    st.error("Loaded object is not a pandas DataFrame.")
    st.stop()

# Ensure 'Date' column exists and convert to datetime
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows with invalid dates
else:
    st.error("No 'Date' column found in the DataFrame.")
    st.stop()

# Ensure 'Intern Name' column exists
if 'Intern Name' not in df.columns:
    st.error("No 'Intern Name' column found in the DataFrame.")
    st.stop()

# Filter out future dates
today = pd.Timestamp(datetime.today().date())
df = df[df['Date'] <= today]

# Dropdown for Intern Name
selected_intern = st.selectbox("Select Intern Name", df['Intern Name'].unique())

# Calendar for Date (only past & today)
# Get available dates for selected intern
available_dates = df[df['Intern Name'] == selected_intern]['Date']
if not available_dates.empty:
    # Default date is the latest available date
    default_date = available_dates.max().date()
else:
    default_date = today.date()

selected_date = st.date_input(
    "Select Date",
    value=default_date,
    min_value=min(available_dates).date() if not available_dates.empty else None,
    max_value=today.date()
)

# Filter DataFrame
filtered_df = df[
    (df['Intern Name'] == selected_intern) &
    (df['Date'] == pd.Timestamp(selected_date))
]

st.subheader("Matching Row(s):")
if not filtered_df.empty:
    st.table(filtered_df)
else:
    st.write("No matching records found.")