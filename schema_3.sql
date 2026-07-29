CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

CREATE TABLE Departments (
    Department_ID INT AUTO_INCREMENT PRIMARY KEY,
    Department_Name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Faculty (
    Faculty_ID INT AUTO_INCREMENT PRIMARY KEY,
    Faculty_Name VARCHAR(100) NOT NULL,
    Designation VARCHAR(50),
    Department_ID INT NOT NULL,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
);

CREATE TABLE Students (
    Student_ID INT AUTO_INCREMENT PRIMARY KEY,
    Roll_Number VARCHAR(20) NOT NULL UNIQUE,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Gender VARCHAR(10),
    Date_of_Birth DATE,
    Email VARCHAR(100) UNIQUE,
    Phone_Number VARCHAR(15),
    Department_ID INT NOT NULL,
    Current_Semester INT NOT NULL,
    Admission_Year INT NOT NULL,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
);

CREATE TABLE Subjects (
    Subject_ID INT AUTO_INCREMENT PRIMARY KEY,
    Subject_Name VARCHAR(100) NOT NULL,
    Department_ID INT NOT NULL,
    Faculty_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID),
    FOREIGN KEY (Faculty_ID) REFERENCES Faculty(Faculty_ID)
);

CREATE TABLE Enrollment (
    Enrollment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Subject_ID INT NOT NULL,
    Semester INT NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID),
    FOREIGN KEY (Subject_ID) REFERENCES Subjects(Subject_ID),
    UNIQUE KEY unique_enrollment (Student_ID, Subject_ID, Semester)
);

CREATE TABLE Attendance (
    Attendance_ID INT AUTO_INCREMENT PRIMARY KEY,
    Enrollment_ID INT NOT NULL,
    Attendance_Date DATE NOT NULL,
    Status ENUM('Present','Absent') NOT NULL,
    FOREIGN KEY (Enrollment_ID) REFERENCES Enrollment(Enrollment_ID)
);

CREATE TABLE Exams (
    Exam_ID INT AUTO_INCREMENT PRIMARY KEY,
    Subject_ID INT NOT NULL,
    Exam_Type ENUM('Quiz','Mid','End') NOT NULL,
    Max_Marks INT NOT NULL,
    Exam_Date DATE,
    FOREIGN KEY (Subject_ID) REFERENCES Subjects(Subject_ID)
);

CREATE TABLE Grades (
    Grade_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Exam_ID INT NOT NULL,
    Marks DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID),
    FOREIGN KEY (Exam_ID) REFERENCES Exams(Exam_ID)
);
