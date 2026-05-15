# Main Dashboard view
from pathlib import Path
import sys
from app import blur_effect_function

import pandas as pd
import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="Dashboard - Grade Management System",
    layout="wide"
)

# Ensure project root is on sys.path so `utils` package imports work
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import authentication
from auth import check_authentication, logout

# Check authentication - redirect to login if not authenticated
if not check_authentication():
    st.switch_page("pages/3_Login View.py")

# Global blur effect for modals using pure CSS + simple JS detection
blur_effect_function()

from src.utils.file_handler import (
    DASHBOARD_DISPLAY_COLUMNS,
    delete_student_record,
    get_student_record,
    load_dashboard_dataframe,
    upsert_student_record,
)


STUDENTS_CSV = PROJECT_ROOT / "data" / "students.csv"
GRADES_CSV = PROJECT_ROOT / "data" / "grades.csv"


def main():
    """Render dashboard and provide simple CRUD forms.

    - Loads a canonical internal dataframe from CSVs using the service layer.
    - Renames internal columns to user-facing headers using
      `DASHBOARD_DISPLAY_COLUMNS` (internal -> display mapping).
    - Presents forms to create/update (upsert) and delete by student id.
    """
    
    # Sidebar with logout button
    with st.sidebar:
        st.header("Hello there, welcome!")
        st.write(f"Logged in as: {st.session_state.get('user_email', 'Unknown')}")
        if st.button("🚪 Logout", use_container_width=True):
            st.toast("Logging out...", icon="👋")
            time.sleep(2.0)
            logout()
            st.rerun()
    
    st.title("📊 Student Grade Dashboard")
    
    students_table, student_manager = st.tabs([":material/table: Students Table", ":material/manage_accounts: Students Manager"])

    # Load canonical dataframe and convert internal column names to display headers.
    data = load_dashboard_dataframe(STUDENTS_CSV, GRADES_CSV)
    display_data = data.rename(columns=DASHBOARD_DISPLAY_COLUMNS)

    with students_table:
        st.header("Track their progress")
        st.selectbox(
            ":material/search: Find enrolled students",
            [""] + data["name"].dropna().astype(str).tolist(),
            filter_mode="fuzzy",
            key="student_search"
        )
        st.table(display_data)

    with student_manager:
        st.header("Manage students")
        existing_ids = data["id"].dropna().astype(str).tolist()
        selected_id = st.selectbox("Search existing student by ID to edit :material/edit:", [""] + existing_ids)
        current_record = get_student_record(STUDENTS_CSV, GRADES_CSV, selected_id) if selected_id else None

        # Upsert form: create or update a student record.
        with st.form("student_upsert_form"):
            student_id = st.text_input("ID Number", value=current_record["id"] if current_record is not None else "")
            name = st.text_input("Student Name", value=current_record["name"] if current_record is not None else "")
            course = st.text_input("Course", value=current_record["course"] if current_record is not None else "")
            status = st.selectbox(
                "Enrollment Status",
                ("Enrolled", "Not Enrolled"),
                index=0 if (current_record is None or current_record.get("status") == "Enrolled") else 1,
            )
            grade_value = st.text_input(
                "Grade Value",
                value="" if current_record is None or pd.isna(current_record["grade_value"]) else str(current_record["grade_value"]),
            )
            
            @st.dialog("Are you sure?")
            def prompt_save():
                st.write("Saving your changes will modify the saved data")
                if st.button("Save", type="primary"):
                    if not student_id.strip():
                        st.error("Student ID is not found or has no inputs.")
                    else:
                        grade_input = grade_value.strip()
                        upsert_student_record(
                            STUDENTS_CSV,
                            GRADES_CSV,
                            student_id=student_id.strip(),
                            name=name.strip(),
                            course=course.strip(),
                            status=status.strip(),
                            grade_value=grade_input if grade_input else None,
                        )
                        st.success(f"Student {name.strip() or student_id.strip()} saved.")
                        with st.spinner("Refreshing database...", show_time=True):
                            time.sleep(1.0)
                        st.rerun()

            save_submitted = st.form_submit_button("Save Student")
            if save_submitted:
                prompt_save()

        # Delete form: remove a student by id.
        with st.form("student_delete_form"):
            delete_id = st.selectbox("Select or find an ID number", [""] + data["id"].dropna().astype(str).tolist(), key="delete_select")
            delete_submitted = st.form_submit_button("Delete Student")
            if delete_submitted:
                if not delete_id.strip():
                    st.error("😢 Invalid input, please try again.")
                elif not delete_id.strip().startswith("20"):
                    st.error('😢 Student ID should have this format: "20xx-xxxxx"')
                else:
                    delete_record = get_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
                    delete_name = delete_record["name"] if delete_record is not None else delete_id.strip()
                    st.success(f"Student {delete_name} deleted.")
                    delete_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
                    with st.toast("Applying changes...", icon="✅"):
                        time.sleep(3.0)
                    st.rerun()


if __name__ == "__main__":
    main()