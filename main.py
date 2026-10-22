

# CareFlow: Clinical Pathway Process Mining

import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "patient_events.csv"
CLEAN_FILE = BASE_DIR / "cleaned_patient_events.csv"


def load_patient_dataset():
    if CLEAN_FILE.exists():
        df = pd.read_csv(CLEAN_FILE)
        print("Loaded cleaned patient dataset.")
    elif DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        print("Loaded original patient dataset.")
    else:
        print("Error: Patient dataset not found!")
        return None

    required = ["case_id", "activity", "timestamp"]

    if not all(column in df.columns for column in required):
        print("Error: Required columns are missing!")
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=required)
    df = df.sort_values(["case_id", "timestamp"]).copy()

    return df


def analyze_waiting_time(df):
    print("\n--- PATIENT WAITING-TIME ANALYSIS ---")

    # Find the previous activity and timestamp for each patient
    df["previous_activity"] = df.groupby("case_id")["activity"].shift(1)
    df["previous_timestamp"] = df.groupby("case_id")["timestamp"].shift(1)

    # Calculate time between consecutive recorded activities
    df["time_minutes"] = (
        df["timestamp"] - df["previous_timestamp"]
    ).dt.total_seconds() / 60

    transitions = df.dropna(subset=["previous_activity"]).copy()

    print("\nWaiting time for each patient:")
    print(
        transitions[
            ["case_id", "previous_activity", "activity", "time_minutes"]
        ].to_string(index=False)
    )

    print("\nAverage time between activities:")
    summary = (
        transitions.groupby(
            ["previous_activity", "activity"]
        )["time_minutes"]
        .mean()
        .reset_index()
        .rename(columns={"time_minutes": "average_minutes"})
    )

    print(summary.to_string(index=False))

    output_file = BASE_DIR / "waiting_time_analysis.csv"
    transitions.to_csv(output_file, index=False)
    summary.to_csv(BASE_DIR / "average_waiting_time.csv", index=False)

    print("\nSaved detailed results:", output_file.name)
    print("Saved summary: average_waiting_time.csv")


def main():
    df = load_patient_dataset()

    if df is not None:
        analyze_waiting_time(df)


if __name__ == "__main__":
    main()
