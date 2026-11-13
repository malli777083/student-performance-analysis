# Student Performance Analysis

A beginner data science project that explores sample student marks, compares subject averages, identifies students who may need support, and generates a chart and text report.

## Features

- Reads student marks from `students.csv` using pandas.
- Calculates average marks for Math, Science, and English.
- Finds the student with the highest overall average.
- Flags a student as `Needs support` when their average is below 60. This threshold is a simple project rule and can be changed.
- Saves `student_performance_chart.png` and `student_analysis_report.txt` when the program runs.

## Files

- `students.csv` — sample dataset
- `analyze_students.py` — analysis and chart-generation program
- `requirements.txt` — Python libraries used

## Run the project

Install Python, then open a terminal in this folder and run:

```powershell
python -m pip install -r requirements.txt
python analyze_students.py
```

The chart and report will be created in this folder.

## Note

The names and marks are sample data created for demonstration. Do not treat the support label as an official academic decision.
