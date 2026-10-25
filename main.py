
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "cleaned_patient_events.csv"


def main():
    if not DATA_FILE.exists():
        print("Dataset not found!")
        return

    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=["case_id", "activity"])

    activity_counts = df["activity"].value_counts()

    print("\n--- PATIENT ACTIVITY SUMMARY ---")
    print(activity_counts.to_string())

    activity_counts.to_csv(
        BASE_DIR / "activity_summary.csv",
        header=["patient_count"]
    )

    plt.figure(figsize=(9, 5))
    activity_counts.plot(kind="bar")
    plt.title("Patient Activity Frequency")
    plt.xlabel("Hospital Activity")
    plt.ylabel("Number of Recorded Events")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(BASE_DIR / "activity_chart.png")
    plt.show()

    print("\nSaved: activity_summary.csv")
    print("Saved: activity_chart.png")


if __name__ == "__main__":
    main()
