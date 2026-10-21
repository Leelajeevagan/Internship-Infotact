
# CareFlow: Clinical Pathway Process Mining


from datetime import datetime


def display_project_info():
    print("=" * 50)
    print(" CAREFLOW: CLINICAL PATHWAY PROCESS MINING")
    print("=" * 50)
    print("Purpose: Analyze patient journeys in hospitals")
    print("Goal: Identify waiting times and pathway delays")
    print("Status: Project initialized")
    print("Date:", datetime.now().strftime("%Y-%m-%d"))
    print("=" * 50)


def main():
    display_project_info()


if __name__ == "__main__":
    main()

