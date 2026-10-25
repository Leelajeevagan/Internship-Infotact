
import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "cleaned_patient_events.csv"

st.set_page_config(
    page_title="CareFlow Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 CareFlow: Clinical Pathway Dashboard")
st.write("Analyze patient journeys and hospital activity patterns.")

if not DATA_FILE.exists():
    st.error("Dataset not found! Please create cleaned_patient_events.csv first.")
    st.stop()

df = pd.read_csv(DATA_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["case_id", "activity", "timestamp"])
df = df.sort_values(["case_id", "timestamp"])

# Calculate summary metrics
total_patients = df["case_id"].nunique()
total_events = len(df)
total_activities = df["activity"].nunique()

patient_duration = (
    df.groupby("case_id")["timestamp"]
    .agg(["min", "max"])
)
patient_duration["duration_minutes"] = (
    patient_duration["max"] - patient_duration["min"]
).dt.total_seconds() / 60

average_duration = patient_duration["duration_minutes"].mean()

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", total_patients)
col2.metric("Recorded Events", total_events)
col3.metric("Activity Types", total_activities)
col4.metric("Average Journey (min)", round(average_duration, 1))

st.divider()

# Activity chart
st.subheader("📊 Patient Activity Frequency")
activity_counts = df["activity"].value_counts()
st.bar_chart(activity_counts)

# Patient journey table
st.subheader("🧑‍⚕️ Patient Journey Details")

journeys = (
    df.groupby("case_id")
    .agg(
        total_activities=("activity", "count"),
        journey=("activity", lambda x: " → ".join(x)),
        start_time=("timestamp", "min"),
        end_time=("timestamp", "max")
    )
    .reset_index()
)

journeys["duration_minutes"] = (
    journeys["end_time"] - journeys["start_time"]
).dt.total_seconds() / 60

st.dataframe(journeys, use_container_width=True)

# Activity filter
st.subheader("🔎 Filter Patient Events")

selected_activity = st.selectbox(
    "Select an activity",
    ["All Activities"] + sorted(df["activity"].unique().tolist())
)

if selected_activity == "All Activities":
    filtered_df = df
else:
    filtered_df = df[df["activity"] == selected_activity]

st.dataframe(filtered_df, use_container_width=True)

st.caption("CareFlow | Clinical Pathway Process Mining | Sample demonstration data")
