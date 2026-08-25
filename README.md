# 🎓 Student Management Database Analysis

A SQL-based data analysis project that manages student academic records, attendance, and enrollment data, and uses SQL queries and Python visualizations to surface performance insights.

## 📖 About

This project designs a normalized MySQL database for student records and builds a Python analysis pipeline on top of it. It demonstrates database design, SQL query writing, and data visualization — covering grade distribution, subject-wise performance, attendance trends, and top-performing students.

## ✨ Features

- 🗄️ Normalized MySQL database schema with constraints for data integrity
- 🔍 Multiple SQL queries covering aggregate, filtering, and grouping analysis
- 📊 Pastel-themed data visualizations built with Matplotlib/Seaborn
- 📈 A 6-panel dashboard summarizing key academic metrics
- 🐍 Clean, modular Python pipeline (schema, queries, and visualization kept separate)

## 🛠️ Tech Stack

- **Database:** MySQL
- **Language:** Python 3.9+
- **Libraries:** pandas, numpy, matplotlib, seaborn, mysql-connector-python

## 🗄️ Database Schema

**Students Table**

| Column | Type | Description |
|---|---|---|
| `StudentID` | INT (PK, AUTO_INCREMENT) | Unique identifier |
| `Name` | VARCHAR(100) | Student name |
| `Grade` | INT | Academic grade level (9–12) |
| `Gender` | CHAR(1) | Student gender (M/F) |
| `MathScore` | INT | Mathematics score (0–100) |
| `ScienceScore` | INT | Science score (0–100) |
| `EnglishScore` | INT | English score (0–100) |
| `Attendance` | INT | Attendance percentage |
| `DateEnrolled` | DATE | Enrollment date |

```sql
CREATE TABLE Students (
    StudentID     INT PRIMARY KEY AUTO_INCREMENT,
    Name          VARCHAR(100) NOT NULL,
    Grade         INT NOT NULL CHECK (Grade BETWEEN 9 AND 12),
    Gender        CHAR(1) NOT NULL CHECK (Gender IN ('M', 'F')),
    MathScore     INT NOT NULL CHECK (MathScore BETWEEN 0 AND 100),
    ScienceScore  INT NOT NULL CHECK (ScienceScore BETWEEN 0 AND 100),
    EnglishScore  INT NOT NULL CHECK (EnglishScore BETWEEN 0 AND 100),
    Attendance    INT NOT NULL CHECK (Attendance BETWEEN 0 AND 100),
    DateEnrolled  DATE NOT NULL
);
```

## 🔍 SQL Queries Included

1. **all_students** — Retrieve all student records
2. **average_scores** — Calculate average scores across subjects
3. **top_performer** — Identify the highest-performing student
4. **grade_distribution** — Analyze student distribution and performance by grade
5. **high_math_achievers** — Find students with Math score > 80
6. **gender_analysis** — Compare performance metrics by gender

Full SQL for each query is in [`queries.py`](queries.py).

## 📈 Visualizations

The analysis produces a 6-panel dashboard (`student_dashboard.png`) covering:

- Subject-wise average score comparison
- Score distribution histograms
- Gender performance comparison
- Grade-level average performance
- Attendance vs. overall performance
- Top performers ranking

![Dashboard](student_dashboard.png)

## 📥 Installation

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/saaagar10/student-management-db-analysis.git
   cd student-management-db-analysis
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up the MySQL database**
```sql
   CREATE DATABASE student_management;
```
   Then update your database connection credentials (host, user, password) in `database.py`.

5. **Run the pipeline**
```bash
   python main.py
```

## 🎮 Usage

Running `python main.py` will:
- Connect to MySQL and create the `Students` table if it doesn't exist
- Load data from `students_data.csv` into the database
- Execute all SQL queries and print results to the console
- Generate `student_dashboard.png`

### Customize the data

Edit `students_data.csv` with your own records:
```csv
StudentID,Name,Grade,Gender,MathScore,ScienceScore,EnglishScore,Attendance,DateEnrolled
1,Your Name,10,M,95,92,90,95,2026-06-01
```

## 📊 Project Structure

```
student-management-db-analysis/
├── main.py                 # Entry point — runs the full pipeline
├── database.py              # MySQL connection, schema, and data loading
├── queries.py                # All SQL queries
├── visualizations.py         # Dashboard generation
├── students_data.csv         # Sample data
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
