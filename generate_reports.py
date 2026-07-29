"""
Runs multiple analytical queries against the Student Management DB,
exports each result as its own CSV report.
"""
import mysql.connector
import pandas as pd
import os

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("DB_PASSWORD"),
    database="student_management"
)

# Each entry: (report_name, query)
reports = {
    "department_performance": """
        SELECT d.Department_Name, ROUND(AVG(g.Marks / ex.Max_Marks * 100), 2) AS Avg_Percentage
        FROM Grades g
        JOIN Exams ex ON g.Exam_ID = ex.Exam_ID
        JOIN Students s ON g.Student_ID = s.Student_ID
        JOIN Departments d ON s.Department_ID = d.Department_ID
        GROUP BY d.Department_ID
        ORDER BY Avg_Percentage DESC;
    """,
    "top_10_students": """
        SELECT s.Student_ID, s.First_Name, s.Last_Name,
               ROUND(AVG(g.Marks / e.Max_Marks * 100), 2) AS Avg_Percentage
        FROM Grades g
        JOIN Exams e ON g.Exam_ID = e.Exam_ID
        JOIN Students s ON g.Student_ID = s.Student_ID
        GROUP BY s.Student_ID
        ORDER BY Avg_Percentage DESC
        LIMIT 10;
    """,
    "grade_distribution": """
        SELECT
          CASE
            WHEN (g.Marks / e.Max_Marks * 100) >= 90 THEN 'A'
            WHEN (g.Marks / e.Max_Marks * 100) >= 75 THEN 'B'
            WHEN (g.Marks / e.Max_Marks * 100) >= 60 THEN 'C'
            WHEN (g.Marks / e.Max_Marks * 100) >= 40 THEN 'D'
            ELSE 'F'
          END AS Grade_Letter,
          COUNT(*) AS Total
        FROM Grades g
        JOIN Exams e ON g.Exam_ID = e.Exam_ID
        GROUP BY Grade_Letter
        ORDER BY Grade_Letter;
    """,
    "low_attendance_students": """
        SELECT s.Student_ID, s.First_Name, s.Last_Name,
               ROUND(SUM(CASE WHEN a.Status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attendance_Pct
        FROM Attendance a
        JOIN Enrollment en ON a.Enrollment_ID = en.Enrollment_ID
        JOIN Students s ON en.Student_ID = s.Student_ID
        GROUP BY s.Student_ID
        HAVING Attendance_Pct < 75
        ORDER BY Attendance_Pct;
    """,
    "subject_wise_average": """
        SELECT sub.Subject_Name, ROUND(AVG(g.Marks / e.Max_Marks * 100), 2) AS Avg_Percentage
        FROM Grades g
        JOIN Exams e ON g.Exam_ID = e.Exam_ID
        JOIN Subjects sub ON e.Subject_ID = sub.Subject_ID
        GROUP BY sub.Subject_ID
        ORDER BY Avg_Percentage DESC;
    """,
}

# Store DataFrames in a dict so the visualization script (Phase 8) can reuse them directly
dataframes = {}

for name, query in reports.items():
    df = pd.read_sql(query, conn)
    dataframes[name] = df
    df.to_csv(f"{name}.csv", index=False)
    print(f"[OK] {name}: {len(df)} rows -> {name}.csv")

conn.close()
print("\nAll reports generated.")