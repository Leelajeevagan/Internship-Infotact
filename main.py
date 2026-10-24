
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "cleaned_patient_events.csv"

def main():
    if not DATA_FILE.exists():
        print("Dataset not found! Run previous steps first.")
        return

    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["case_id", "activity", "timestamp"])
    df = df.sort_values(["case_id", "timestamp"])

    df["next_activity"] = df.groupby("case_id")["activity"].shift(-1)

    transitions = df.dropna(subset=["next_activity"])

    process_map = (
        transitions.groupby(["activity", "next_activity"])
        .size()
        .reset_index(name="frequency")
        .sort_values("frequency", ascending=False)
    )

    print("\n--- PROCESS MINING ANALYSIS ---")
    print("\nActivity Transitions:")
    print(process_map.to_string(index=False))

    output_file = BASE_DIR / "process_mining_results.csv"
    process_map.to_csv(output_file, index=False)

    print("\nResults saved to:", output_file.name)

if __name__ == "__main__":
    main()
