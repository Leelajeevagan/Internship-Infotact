
# CareFlow: Clinical Pathway Process Mining

import pandas as pd
from pathlib import Path


def load_patient_dataset():
    file_path = Path(__file__).parent / "patient_events.csv"

    if not file_path.exists():
        print("Error: patient_events.csv file not found!")
        print("Please keep the CSV file in the same folder as main.py.")
        return

    df = pd.read_csv(file_path)

    required_columns = ["case_id", "activity", "timestamp"]

    if not all(column in df.columns for column in required_columns):
        print("Error: Required columns are missing from the dataset.")
        print("Required columns:", required_columns)
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    print("=" * 50)
    print(" CAREFLOW: CLINICAL PATHWAY PROCESS MINING")
    print("=" * 50)
    print("\nDataset loaded successfully!")
    print("Total events:", len(df))
    print("Total patients:", df["case_id"].nunique())
    print("Unique activities:", df["activity"].nunique())
    print("\nPatient activities:")
    print(df[["case_id", "activity", "timestamp"]].head(10).to_string(index=False))
    print("\nMissing timestamps:", df["timestamp"].isna().sum())
    print("\nDataset loading completed!")


def main():
    load_patient_dataset()


if __name__ == "__main__":
    main()


