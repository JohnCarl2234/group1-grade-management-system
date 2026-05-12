from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

STUDENT_REQUIRED_COLUMNS = ["id", "name", "course", "status"]
GRADE_REQUIRED_COLUMNS = ["id", "grade_value"]

# Mapping from internal dataframe column name -> user-facing header used in the UI.
# Keep internal names stable (used in code and storage) and change the display
# strings here to customize table headers without touching business logic.
DASHBOARD_DISPLAY_COLUMNS = {
    "id": ":material/id_card: ID Number",
    "name": ":material/school: Students",
    "grade_value": ":material/grading: GWA",
    "status": ":material/info: Enrollment Status",
    "course": ":material/book_5: Course",
}


def _resolve_csv_path(file_path: str | Path) -> Path:
    path = Path(file_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


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
    """Return a merged dataframe used by the dashboard.

    The returned dataframe uses the canonical internal column names
    `id`, `name`, `grade_value`, `status`, `course` so views and
    services can rely on a stable schema.
    """
    students_df = load_students_dataframe(students_csv)
    grades_df = load_grades_dataframe(grades_csv)

    merged = students_df.merge(grades_df, on="id", how="left")
    desired_columns = ["id", "name", "grade_value", "status", "course"]

    # Ensure all expected columns exist
    for column in desired_columns:
        if column not in merged.columns:
            merged[column] = pd.NA

    return merged[desired_columns]


def get_student_record(students_csv: str | Path, grades_csv: str | Path, student_id: str) -> dict[str, object] | None:
    """Return a single student record (merged with grade) or None."""
    dashboard_df = load_dashboard_dataframe(students_csv, grades_csv)
    matches = dashboard_df[dashboard_df["id"].astype(str) == str(student_id)]
    if matches.empty:
        return None

    return matches.iloc[0].to_dict()


def upsert_student_record(
    students_csv: str | Path,
    grades_csv: str | Path,
    *,
    student_id: str,
    name: str,
    course: str,
    status: str,
    grade_value: str | float | None = None,
) -> None:
    # Basic validation and normalization
    student_id = str(student_id).strip()
    if not student_id:
        raise ValueError("student_id is required")

    students_df = load_students_dataframe(students_csv)
    grades_df = load_grades_dataframe(grades_csv)

    # Build canonical rows to insert/update
    student_row = pd.DataFrame(
        [{"id": student_id, "name": name.strip(), "course": course.strip(), "status": status.strip()}]
    )
    grade_row = pd.DataFrame([{"id": student_id, "grade_value": grade_value}])

    # Remove any existing rows for this id then append the new one
    students_df = students_df[students_df["id"].astype(str) != student_id]
    grades_df = grades_df[grades_df["id"].astype(str) != student_id]

    students_df = pd.concat([students_df, student_row], ignore_index=True)
    grades_df = pd.concat([grades_df, grade_row], ignore_index=True)

    # Atomic write to avoid corruption on failure
    _write_csv_dataframe(students_csv, students_df)
    _write_csv_dataframe(grades_csv, grades_df)


def delete_student_record(students_csv: str | Path, grades_csv: str | Path, student_id: str) -> None:
    """Delete a student (and their grade) from both CSVs by id."""
    student_id = str(student_id).strip()
    if not student_id:
        raise ValueError("student_id is required")

    students_df = load_students_dataframe(students_csv)
    grades_df = load_grades_dataframe(grades_csv)

    students_df = students_df[students_df["id"].astype(str) != student_id]
    grades_df = grades_df[grades_df["id"].astype(str) != student_id]

    _write_csv_dataframe(students_csv, students_df)
    _write_csv_dataframe(grades_csv, grades_df)