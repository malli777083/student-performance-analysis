from pathlib import Path
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "skillorbit-matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "students.csv"
CHART_FILE = BASE_DIR / "student_performance_chart.png"
REPORT_FILE = BASE_DIR / "student_analysis_report.txt"
SUBJECTS = ["math", "science", "english"]
SUPPORT_THRESHOLD = 60

students = pd.read_csv(DATA_FILE)
required_columns = {"name", *SUBJECTS}
missing_columns = required_columns.difference(students.columns)
if missing_columns:
    raise ValueError(f"students.csv is missing columns: {', '.join(sorted(missing_columns))}")
if students.empty:
    raise ValueError("students.csv has no student rows to analyze.")

students[SUBJECTS] = students[SUBJECTS].apply(pd.to_numeric, errors="raise")
students["average"] = students[SUBJECTS].mean(axis=1).round(1)
students["status"] = students["average"].apply(
    lambda mark: "Needs support" if mark < SUPPORT_THRESHOLD else "On track"
)

subject_averages = students[SUBJECTS].mean().round(1)
top_student = students.loc[students["average"].idxmax()]
support_students = students.loc[students["status"] == "Needs support", "name"].tolist()

print("STUDENT PERFORMANCE ANALYSIS")
print("-" * 32)
for subject, average in subject_averages.items():
    print(f"Average {subject.title()} mark: {average:.1f}")
print(f"\nTop student: {top_student['name']} ({top_student['average']:.1f})")
print(f"Students needing support (average below {SUPPORT_THRESHOLD}): "
      f"{', '.join(support_students) if support_students else 'None'}")
print("\nSTUDENT-WISE SUMMARY")
for _, student in students.iterrows():
    print(f"{student['name']}: average {student['average']:.1f} - {student['status']}")

bar_colors = ["seagreen" if status == "On track" else "tomato"
              for status in students["status"]]
figure, axis = plt.subplots(figsize=(9, 5))
bars = axis.bar(students["name"], students["average"], color=bar_colors)
axis.bar_label(bars, fmt="%.1f", padding=3)
axis.axhline(SUPPORT_THRESHOLD, color="darkorange", linestyle="--",
             label=f"Support threshold: {SUPPORT_THRESHOLD}")
axis.set_title("Student Average Marks by Student")
axis.set_xlabel("Student")
axis.set_ylabel("Average mark")
axis.set_ylim(0, 105)
axis.grid(axis="y", alpha=0.2)
axis.legend()
figure.tight_layout()
figure.savefig(CHART_FILE, dpi=160)
plt.close(figure)

report_lines = [
    "STUDENT PERFORMANCE ANALYSIS REPORT",
    "====================================",
    "Sample data is used for this project demonstration.",
    "",
    "Average marks by subject:",
]
report_lines.extend(f"- {subject.title()}: {average:.1f}" for subject, average in subject_averages.items())
report_lines.extend([
    "",
    f"Top student by average: {top_student['name']} ({top_student['average']:.1f})",
    f"Support threshold: average below {SUPPORT_THRESHOLD}",
    f"Students needing support: {', '.join(support_students) if support_students else 'None'}",
    "",
    "Student-wise results:",
])
report_lines.extend(
    f"- {row['name']}: average {row['average']:.1f} - {row['status']}"
    for _, row in students.iterrows()
)
REPORT_FILE.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

print(f"\nChart saved: {CHART_FILE.name}")
print(f"Report saved: {REPORT_FILE.name}")
