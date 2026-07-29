import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Sagar2July",
    database="student_management"
)

query = """
SELECT d.Department_Name, ROUND(AVG(g.Marks / ex.Max_Marks * 100), 2) AS Avg_Percentage
FROM Grades g
JOIN Exams ex ON g.Exam_ID = ex.Exam_ID
JOIN Students s ON g.Student_ID = s.Student_ID
JOIN Departments d ON s.Department_ID = d.Department_ID
GROUP BY d.Department_ID
ORDER BY Avg_Percentage DESC;
"""

df = pd.read_sql(query, conn)
print(df)

df.dropna(inplace=True)
df["Avg_Percentage"] = df["Avg_Percentage"].astype(float)

df.to_csv("department_performance_report.csv", index=False)
print("Report exported.")

conn.close()