"""
Generates charts from the CSV reports produced by generate_reports.py.
Run generate_reports.py first.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ---------- 1. Department-wise performance (bar chart) ----------
df = pd.read_csv("department_performance.csv")
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Department_Name", y="Avg_Percentage", palette="viridis")
plt.title("Department-wise Average Performance")
plt.ylabel("Average Percentage")
plt.xlabel("Department")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("chart_department_performance.png")
plt.close()

# ---------- 2. Top 10 students (horizontal bar) ----------
df = pd.read_csv("top_10_students.csv")
df["Full_Name"] = df["First_Name"] + " " + df["Last_Name"]
plt.figure(figsize=(8, 6))
sns.barplot(data=df, y="Full_Name", x="Avg_Percentage", palette="mako")
plt.title("Top 10 Students by Average Percentage")
plt.xlabel("Average Percentage")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart_top_10_students.png")
plt.close()

# ---------- 3. Grade distribution (bar chart) ----------
df = pd.read_csv("grade_distribution.csv")
plt.figure(figsize=(6, 5))
sns.barplot(data=df, x="Grade_Letter", y="Total", palette="rocket")
plt.title("Grade Distribution (All Exams)")
plt.xlabel("Grade")
plt.ylabel("Number of Exam Results")
plt.tight_layout()
plt.savefig("chart_grade_distribution.png")
plt.close()

# ---------- 4. Subject-wise average (horizontal bar, top 15 for readability) ----------
df = pd.read_csv("subject_wise_average.csv").head(15)
plt.figure(figsize=(8, 8))
sns.barplot(data=df, y="Subject_Name", x="Avg_Percentage", palette="crest")
plt.title("Top 15 Subjects by Average Percentage")
plt.xlabel("Average Percentage")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart_subject_wise_average.png")
plt.close()

# ---------- 5. Low attendance students (histogram of attendance %) ----------
df = pd.read_csv("low_attendance_students.csv")
plt.figure(figsize=(7, 5))
sns.histplot(df["Attendance_Pct"], bins=10, kde=True, color="crimson")
plt.title("Distribution of Attendance % (Students Below 75%)")
plt.xlabel("Attendance Percentage")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig("chart_low_attendance.png")
plt.close()

print("5 charts saved as PNG files in the current folder.")
