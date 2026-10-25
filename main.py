
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "cleaned_patient_events.csv"

EXPECTED_PATHWAY = [
    "Registration",
    "Consultation",
    "Laboratory Test",
    "Treatment",
    "Discharge"
]


def main():
    if not DATA_FILE.exists():
        print("Dataset not found!")
        return

    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["case_id", "activity", "timestamp"])
    df = df.sort_values(["case_id", "timestamp"])

    results = []

    for case_id, patient in df.groupby("case_id"):
        actual = patient["activity"].tolist()

        matches = actual == EXPECTED_PATHWAY

        results.append({
            "case_id": case_id,
            "expected_pathway": " -> ".join(EXPECTED_PATHWAY),
            "actual_pathway": " -> ".join(actual),
            "pathway_status": "Matches" if matches else "Deviation"
        })

    result_df = pd.DataFrame(results)

    print("\n--- EXPECTED VS ACTUAL PATHWAY ---")
    print(result_df.to_string(index=False))

    output_file = BASE_DIR / "pathway_comparison.csv"
    result_df.to_csv(output_file, index=False)

    print("\nSaved results:", output_file.name)


if __name__ == "__main__":
    main()
