"""
Generates synthetic but relationally-consistent data for the
Student Management Database. Outputs CSVs ready for MySQL LOAD DATA / import.
"""
import random
import pandas as pd
from faker import Faker
from datetime import date, timedelta

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

# ---------- 1. Departments ----------
dept_names = ["CSE", "ECE", "Mechanical", "Civil", "Information Technology"]
departments = [{"Department_ID": i + 1, "Department_Name": name}
               for i, name in enumerate(dept_names)]
pd.DataFrame(departments).to_csv("departments.csv", index=False)

# ---------- 2. Faculty (~4 per department) ----------
designations = ["Assistant Professor", "Associate Professor", "Professor"]
faculty = []
fid = 1
for dept in departments:
    for _ in range(4):
        faculty.append({
            "Faculty_ID": fid,
            "Faculty_Name": fake.name(),
            "Designation": random.choice(designations),
            "Department_ID": dept["Department_ID"]
        })
        fid += 1
pd.DataFrame(faculty).to_csv("faculty.csv", index=False)

# ---------- 3. Students (~250, spread across depts) ----------
students = []
for sid in range(1, 251):
    dept = random.choice(departments)
    students.append({
        "Student_ID": sid,
        "Roll_Number": f"{dept['Department_Name'][:2].upper()}{2022 + sid % 4}{sid:04d}",
        "First_Name": fake.first_name(),
        "Last_Name": fake.last_name(),
        "Gender": random.choice(["Male", "Female"]),
        "Date_of_Birth": fake.date_of_birth(minimum_age=18, maximum_age=23),
        "Email": fake.unique.email(),
        "Phone_Number": fake.msisdn()[:10],
        "Department_ID": dept["Department_ID"],
        "Current_Semester": random.choice([1, 2, 3, 4]),
        "Admission_Year": 2026 - random.choice([0, 1, 1, 2])
    })
pd.DataFrame(students).to_csv("students.csv", index=False)

# ---------- 4. Subjects (~9 per department) ----------
subjects = []
subj_id = 1
dept_faculty = {}
for f in faculty:
    dept_faculty.setdefault(f["Department_ID"], []).append(f["Faculty_ID"])

for dept in departments:
    for n in range(9):
        subjects.append({
            "Subject_ID": subj_id,
            "Subject_Name": f"{dept['Department_Name']} Subject {n + 1}",
            "Department_ID": dept["Department_ID"],
            "Faculty_ID": random.choice(dept_faculty[dept["Department_ID"]])
        })
        subj_id += 1
pd.DataFrame(subjects).to_csv("subjects.csv", index=False)

# ---------- 5. Enrollment (each student: 5 subjects x each completed semester) ----------
dept_subjects = {}
for s in subjects:
    dept_subjects.setdefault(s["Department_ID"], []).append(s["Subject_ID"])

enrollment = []
eid = 1
for stu in students:
    max_sem = stu["Current_Semester"]  # student has completed up to this semester
    available_subjects = dept_subjects[stu["Department_ID"]]
    for sem in range(1, max_sem + 1):
        chosen = random.sample(available_subjects, 5)
        for subj_id_chosen in chosen:
            enrollment.append({
                "Enrollment_ID": eid,
                "Student_ID": stu["Student_ID"],
                "Subject_ID": subj_id_chosen,
                "Semester": sem
            })
            eid += 1
pd.DataFrame(enrollment).to_csv("enrollment.csv", index=False)

# ---------- 6. Attendance (only for CURRENT semester enrollments, ~60 class days) ----------
attendance = []
aid = 1
current_sem_enrollments = [e for e in enrollment
                            if e["Semester"] == next(s["Current_Semester"]
                                                      for s in students if s["Student_ID"] == e["Student_ID"])]

start_date = date(2026, 1, 5)
for enr in current_sem_enrollments:
    for day_offset in range(60):
        att_date = start_date + timedelta(days=day_offset)
        if att_date.weekday() >= 5:  # skip weekends
            continue
        attendance.append({
            "Attendance_ID": aid,
            "Enrollment_ID": enr["Enrollment_ID"],
            "Attendance_Date": att_date,
            "Status": random.choices(["Present", "Absent"], weights=[85, 15])[0]
        })
        aid += 1
pd.DataFrame(attendance).to_csv("attendance.csv", index=False)

# ---------- 7. Exams (3 per subject: Quiz, Mid, End) ----------
exams = []
exam_id = 1
exam_types = [("Quiz", 20), ("Mid", 30), ("End", 100)]
for subj in subjects:
    for etype, maxm in exam_types:
        exams.append({
            "Exam_ID": exam_id,
            "Subject_ID": subj["Subject_ID"],
            "Exam_Type": etype,
            "Max_Marks": maxm,
            "Exam_Date": fake.date_between(start_date="-4mo", end_date="today")
        })
        exam_id += 1
pd.DataFrame(exams).to_csv("exams.csv", index=False)

# ---------- 8. Grades (each student gets marks for exams of subjects they enrolled in) ----------
grades = []
gid = 1
subj_exams = {}
for ex in exams:
    subj_exams.setdefault(ex["Subject_ID"], []).append(ex)

for enr in enrollment:
    for ex in subj_exams[enr["Subject_ID"]]:
        mark = round(random.uniform(0.35, 1.0) * ex["Max_Marks"], 2)
        grades.append({
            "Grade_ID": gid,
            "Student_ID": enr["Student_ID"],
            "Exam_ID": ex["Exam_ID"],
            "Marks": mark
        })
        gid += 1
pd.DataFrame(grades).to_csv("grades.csv", index=False)

print("Done. Row counts:")
for name, df in [("departments", departments), ("faculty", faculty), ("students", students),
                  ("subjects", subjects), ("enrollment", enrollment),
                  ("attendance", attendance), ("exams", exams), ("grades", grades)]:
    print(f"  {name}: {len(df)}")