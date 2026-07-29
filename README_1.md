# Student Management Database Analysis

A normalized relational database modeling a multi-department university system, built from scratch — schema design, synthetic data generation, SQL analysis, and Python-based reporting/visualization.

## Overview

- **8 tables**, normalized to 3NF, with enforced referential integrity (primary keys, foreign keys, composite unique constraints)
- **~68,000 records** across all tables, generated synthetically with Python + Faker
- **12+ analytical SQL queries** covering performance trends, attendance risk, department/semester comparisons, and faculty workload
- **Python reporting pipeline** (MySQL → Pandas → CSV) and **Matplotlib/Seaborn visualizations**

## Database Scale

| Table | Rows | Notes |
|---|---|---|
| Departments | 5 | CSE, ECE, Mechanical, Civil, IT |
| Faculty | 20 | ~4 per department |
| Students | 250 | Spread across 4 semesters |
| Subjects | 45 | ~9 per department (course catalog) |
| Enrollment | 3,290 | Junction table resolving Student↔Subject M:N relationship |
| Attendance | ~55,000 | Daily records, tracked only for each student's current semester |
| Exams | 135 | Quiz/Mid/End per subject |
| Grades | ~9,870 | Marks per student per exam |

## Schema Design Highlights

- **Surrogate keys** (`Student_ID`, etc.) used as primary keys instead of natural keys (`Roll_Number`) since surrogate keys never need to change.
- **`Enrollment`** is a junction table resolving the many-to-many relationship between Students and Subjects; it also carries `Semester`, since a subject can be taken in different semesters by different students (subjects are not semester-locked).
- **`Attendance`** references `Enrollment_ID` rather than `Student_ID` + `Subject_ID` directly, so the database structurally guarantees a student can't have attendance for a subject they were never enrolled in.
- **Derived data is deliberately excluded** — e.g., letter grades are computed on the fly in queries (via `CASE`), never stored, to avoid data going stale relative to its source values.

## Project Structure

```
schema.sql                        -- table definitions (DDL)
generate_data.py                  -- synthetic data generation (Faker), outputs CSVs
analysis_queries.sql               -- 12+ analytical SQL queries
generate_reports.py                -- Python: MySQL -> Pandas -> CSV reports
generate_charts.py                 -- Python: CSV reports -> Matplotlib/Seaborn charts
```

## Setup

1. Run `schema.sql` in MySQL to create the database and tables.
2. Run `generate_data.py` to produce CSVs, then import them into MySQL (Table Data Import Wizard) in this order: departments → faculty → students → subjects → enrollment → attendance → exams → grades.
3. Set your MySQL password as an environment variable (never hardcoded):
   ```bash
   export DB_PASSWORD="your_password"
   ```
4. Run `generate_reports.py` to produce CSV analytical reports.
5. Run `generate_charts.py` to produce PNG chart visualizations.

## Sample Insights

- Department-wise average performance ranges ~67–68% across all 5 departments.
- Grade distribution across ~9,870 exam results: A (1557), B (2297), C (2299), D (2958), F (759).

## Tech Stack

MySQL · Python · Pandas · mysql-connector-python · Matplotlib · Seaborn · Faker
