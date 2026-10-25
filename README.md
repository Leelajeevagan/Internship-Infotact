# Internship-Infotact

# CareFlow: Clinical Pathway Process Mining

## Project Overview
CareFlow is a healthcare analytics project that analyzes patient journeys and hospital activity patterns using process mining concepts and data visualization.

## Objectives
- Analyze patient activity sequences.
- Calculate time between consecutive activities.
- Identify common patient pathways.
- Compare actual pathways with a defined expected pathway.
- Visualize patient data through an interactive dashboard.

## Technologies Used
- Python
- Pandas
- Matplotlib
- Streamlit
- CSV Dataset
- Git and GitHub

## Project Files
- `main.py` - Patient data analysis and processing.
- `app.py` - Interactive Streamlit dashboard.
- `patient_events.csv` - Sample patient event dataset.
- `cleaned_patient_events.csv` - Cleaned dataset.
- `waiting_time_analysis.csv` - Activity transition timing results.
- `average_waiting_time.csv` - Average time between activities.
- `patient_journey_analysis.csv` - Individual patient journeys.
- `pathway_summary.csv` - Common pathway summary.
- `process_mining_results.csv` - Activity transition frequencies.
- `pathway_comparison.csv` - Expected vs actual pathway comparison.
- `activity_summary.csv` - Activity frequency summary.
- `activity_chart.png` - Activity frequency visualization.

## How to Run

1. Install Python.
2. Install required packages:

   ```bash
   python -m pip install pandas matplotlib streamlit
   ```

3. Run the analysis:

   ```bash
   python main.py
   ```

4. Launch the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

## Testing
- Dataset loading and required columns.
- Missing values and invalid timestamps.
- Patient activity ordering.
- Activity transition and pathway analysis.
- Dashboard metrics, charts and filters.

## Limitations
This project uses sample demonstration data, not real hospital records. The expected pathway is predefined for demonstration and does not represent a validated clinical guideline.

## Future Enhancements
- Use anonymized real-world event logs.
- Add more advanced process mining techniques.
- Improve pathway deviation analysis.
- Add more dashboard filters and performance metrics.

## Project Status
Core analysis and interactive dashboard implemented.

