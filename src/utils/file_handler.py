from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.Student import Student
from models.Grades import Grades
from data.Subjects import SUBJECTS

STUDENT_REQUIRED_COLUMNS = ["student_id", "name", "course", "year_level", "status"]
GRADE_REQUIRED_COLUMNS = ["student_id", "semester", "subject", "grade"]

YEAR_LEVELS  = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
SEMESTERS    = ["1st Semester", "2nd Semester"]
VALID_GRADES = Grades.VALID_GRADES

# Mapping from internal dataframe column name -> user-facing header used in the UI.
# Keep internal names stable (used in code and storage) and change the display
# strings here to customize table headers without touching business logic.
DASHBOARD_DISPLAY_COLUMNS = {
    "student_id": "ID Number",
    "name": "Students",
    "status": "Enrollment Status",
    "year_level": "Year Level",
    "course": "Course",
}


def _resolve_csv_path(file_path: str | Path) -> Path:
    path = Path(file_path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def _read_csv_dataframe(file_path: str | Path, required_columns: list[str]) -> pd.DataFrame:
    path = _resolve_csv_path(file_path)
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=required_columns)

    # Read CSV and normalize column names to avoid issues with extra spaces
    dataframe = pd.read_csv(path, skipinitialspace=True)
    dataframe.columns = dataframe.columns.astype(str).str.strip()

    # Drop stray index-like columns such as "Unnamed: 4" that come from malformed CSVs.
    dataframe = dataframe.loc[:, ~dataframe.columns.str.startswith("Unnamed")]

    # Ensure required columns exist so callers can rely on them
    for column in required_columns:
        if column not in dataframe.columns:
            dataframe[column] = pd.NA

    # Return only the canonical schema in the expected order.
    return dataframe[required_columns]


def _write_csv_dataframe(file_path: str | Path, dataframe: pd.DataFrame) -> None:
    path = _resolve_csv_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    dataframe.to_csv(temporary_path, index=False)
    os.replace(temporary_path, path)


def load_students_dataframe(students_csv: str | Path) -> pd.DataFrame:
    """Load students CSV and guarantee student columns exist."""
    return _read_csv_dataframe(students_csv, STUDENT_REQUIRED_COLUMNS)


def load_grades_dataframe(grades_csv: str | Path) -> pd.DataFrame:
    """Load grades CSV and guarantee grade columns exist."""
    return _read_csv_dataframe(grades_csv, GRADE_REQUIRED_COLUMNS)


def load_dashboard_dataframe(students_csv: str | Path, grades_csv: str | Path) -> pd.DataFrame:
    return load_students_dataframe(students_csv)

def get_all_students(students_csv: str | Path) -> list[Student]:
    
    df = load_students_dataframe(students_csv)
 
    # Convert each row into a Student object using Student.from_dict()
    return [Student.from_dict(row.to_dict()) for _, row in df.iterrows()]


def get_student_record(students_csv: str | Path, grades_csv: str | Path, student_id: str) -> dict[str, object] | None:
    dashboard_df = load_students_dataframe(students_csv)
 
    # Filter rows by student ID
    matches = dashboard_df[dashboard_df["student_id"].astype(str).str.strip() == str(student_id).strip()]
 
    if matches.empty:
        return None
 
    # Convert the matched row to a Student object
    return Student.from_dict(matches.iloc[0].to_dict())

def find_student_by_info(
    students_csv: str | Path,
    student_id: str,
    name: str,
    course: str,
    year_level: str,
) -> Student | None:

    # Get all students as Student objects
    all_students = get_all_students(students_csv)
 
    # Use Student.matches() to check each one
    # This is the OOP approach — matching logic lives in the Student class
    for student in all_students:
        if student.does_match(student_id, name, course, year_level):
            return student
 
    return None

def get_student_grades(
    grades_csv: str | Path,
    student_id: str,
) -> list[Grades]:

    df = load_grades_dataframe(grades_csv)
 
    # Filter rows for this student only
    student_rows = df[
        df["student_id"].astype(str).str.strip() == str(student_id).strip()
    ]
 
    if student_rows.empty:
        return []
 
    # Convert each row into a Grade object using Grade.from_dict()
    return [Grades.from_dict(row.to_dict()) for _, row in student_rows.iterrows()]

def get_student_grades_by_semester(
    grades_csv: str | Path,
    student_id: str,
    semester: str,
) -> list[Grades]:

    all_grades = get_student_grades(grades_csv, student_id)
 
    # Filter by semester
    return [g for g in all_grades if g.semester == semester]


def upsert_student_record(
    students_csv: str | Path,
    grades_csv: str | Path,
    *,
    student_id: str,
    name: str,
    course: str,
    year_level: str,
    status: str,
    grades: dict[str, dict[str, str]] | None = None,
) -> None:
    # Basic validation and normalization
    students_df = load_students_dataframe(students_csv)
 
    # Build a Student object to ensure data is clean and consistent
    student = Student(
        student_id=student_id,
        name=name,
        course=course,
        year_level=year_level,
        status=status,
    )
 
    # Remove existing row for this student (if any), then append new row
    students_df = students_df[students_df["student_id"].astype(str) != student_id]
    new_student_row = pd.DataFrame([student.to_dict()])
    students_df = pd.concat([students_df, new_student_row], ignore_index=True)
 
    # Atomically write updated students CSV
    _write_csv_dataframe(students_csv, students_df)
 
    # ── Update grades (only if grades dict was provided) ──────────────────────
    if grades:
        grades_df = load_grades_dataframe(grades_csv)
 
        # Remove all existing grade rows for this student
        grades_df = grades_df[grades_df["student_id"].astype(str) != student_id]
 
        # Build new Grade objects and collect their dicts
        new_grade_rows = []
        for semester, subjects in grades.items():
            for subject, grade_val in subjects.items():
                # Skip empty or placeholder values
                if grade_val and grade_val != "No grade yet":
                    # Build a Grade object — this validates the data
                    grade_obj = Grades(
                        student_id=student_id,
                        semester=semester,
                        subject=subject,
                        grade=grade_val,
                    )
                    new_grade_rows.append(grade_obj.to_dict())
 
        # Append new grade rows if any
        if new_grade_rows:
            grades_df = pd.concat(
                [grades_df, pd.DataFrame(new_grade_rows)],
                ignore_index=True,
            )
 
        # Atomically write updated grades CSV
        _write_csv_dataframe(grades_csv, grades_df)
 

def delete_student_record(students_csv: str | Path, grades_csv: str | Path, student_id: str) -> None:
    """Delete a student (and their grade) from both CSVs by id."""
    student_id = str(student_id).strip()
    if not student_id:
        raise ValueError("student_id is required")

    # Remove from students.csv
    students_df = load_students_dataframe(students_csv)
    students_df = students_df[students_df["student_id"].astype(str) != student_id]
    _write_csv_dataframe(students_csv, students_df)
 
    # Remove all grade rows for this student from grades.csv
    grades_df = load_grades_dataframe(grades_csv)
    grades_df = grades_df[grades_df["student_id"].astype(str) != student_id]
    _write_csv_dataframe(grades_csv, grades_df)


def compute_average(grades: list[Grades]) -> float:

    return Grades.compute_average(grades)
 
 
def get_remarks(grade: float) -> str:

    return Grades.average_remarks(grade)
 
 
def get_grade_description(grade: float) -> str:

    return Grades.average_description(grade)