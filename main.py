
# CareFlow: Clinical Pathway Process Mining

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
CLEAN_FILE = BASE_DIR / "cleaned_patient_events.csv"
DATA_FILE = BASE_DIR / "patient_events.csv"


def load_patient_dataset():
    file_path = CLEAN_FILE if CLEAN_FILE.exists() else DATA_FILE

    if not file_path.exists():
        print("Error: Patient dataset not found!")
        return None

    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["case_id", "activity", "timestamp"])
    df = df.sort_values(["case_id", "timestamp"])

    print("Dataset loaded successfully!")
    return df


def analyze_patient_journeys(df):
    print("\n--- PATIENT JOURNEY ANALYSIS ---")

    journeys = (
        df.groupby("case_id")
        .agg(
            total_activities=("activity", "count"),
            journey=("activity", lambda activities: " -> ".join(activities)),
            start_time=("timestamp", "min"),
            end_time=("timestamp", "max")
        )
        .reset_index()
    )

    journeys["total_duration_minutes"] = (
        journeys["end_time"] - journeys["start_time"]
    ).dt.total_seconds() / 60

    print("\nIndividual Patient Journeys:")
    print(journeys.to_string(index=False))

    pathway_summary = (
        journeys.groupby("journey")
        .size()
        .reset_index(name="patient_count")
        .sort_values("patient_count", ascending=False)
    )

    print("\nCommon Patient Pathways:")
    print(pathway_summary.to_string(index=False))

    journeys.to_csv(BASE_DIR / "patient_journey_analysis.csv", index=False)
    pathway_summary.to_csv(BASE_DIR / "pathway_summary.csv", index=False)

    print("\nSaved: patient_journey_analysis.csv")
    print("Saved: pathway_summary.csv")


def main():
    df = load_patient_dataset()

    if df is not None:
        analyze_patient_journeys(df)


if __name__ == "__main__":
    main()

