
# CareFlow: Clinical Pathway Process Mining

import pandas as pd
from pathlib import Path


def load_patient_dataset():
    file_path = Path(__file__).parent / "patient_events.csv"

    if not file_path.exists():
        print("Error: patient_events.csv file not found!")
        return None

    df = pd.read_csv(file_path)

    required_columns = ["case_id", "activity", "timestamp"]

    if not all(column in df.columns for column in required_columns):
        print("Error: Required columns are missing!")
        return None

    return df


def clean_patient_dataset(df):
    print("\n--- DATA CLEANING REPORT ---")
    print("Original records:", len(df))

    # Check missing values
    print("\nMissing values before cleaning:")
    print(df[["case_id", "activity", "timestamp"]].isnull().sum())

    # Remove duplicate records
    duplicate_count = df.duplicated().sum()
    print("\nDuplicate records found:", duplicate_count)
    df = df.drop_duplicates().copy()

    # Remove records missing essential information
    df = df.dropna(subset=["case_id", "activity", "timestamp"]).copy()

    # Convert timestamps and identify invalid values
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    invalid_count = df["timestamp"].isna().sum()
    print("Invalid timestamps found:", invalid_count)

    # Remove records with invalid timestamps
    df = df.dropna(subset=["timestamp"]).copy()

    # Arrange patient activities in chronological order
    df = df.sort_values(
        by=["case_id", "timestamp"]
    ).reset_index(drop=True)

    print("\nRecords after cleaning:", len(df))
    print("Patients remaining:", df["case_id"].nunique())
    print("\nCleaned dataset preview:")
    print(df.head(10).to_string(index=False))

    # Save cleaned dataset
    output_path = Path(__file__).parent / "cleaned_patient_events.csv"
    df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path.name)
    return df


def main():
    df = load_patient_dataset()

    if df is not None:
        clean_patient_dataset(df)


if __name__ == "__main__":
    main()



