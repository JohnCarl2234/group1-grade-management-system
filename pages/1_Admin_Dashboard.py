# # Main Dashboard view
# from pathlib import Path
# import sys

# import pandas as pd
# import streamlit as st
# import time

# # Set page config
# st.set_page_config(
#     page_title="Admin Dashboard - Grade Management System",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Ensure project root is on sys.path so `utils` package imports work
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(0, str(PROJECT_ROOT))

# # Import authentication
# from auth import check_authentication, logout
# from data.Subjects import SUBJECTS
# from src.utils.file_handler import (
#     DASHBOARD_DISPLAY_COLUMNS,
#     SEMESTERS,
#     YEAR_LEVELS,
#     compute_average,
#     delete_student_record,
#     get_grade_description,
#     get_remarks,
#     get_student_grades,
#     get_student_grades_by_semester,
#     get_student_record,
#     load_dashboard_dataframe,
#     upsert_student_record
# )

# # Check authentication - redirect to login if not authenticated
# if not check_authentication():
#     st.switch_page("pages/3_Login View.py")

# # Global blur effect for modals using pure CSS + simple JS detection
# blur_effect_function()

# from src.utils.file_handler import (
#     DASHBOARD_DISPLAY_COLUMNS,
#     delete_student_record,
#     get_student_record,
#     load_dashboard_dataframe,
#     upsert_student_record,
# )


# STUDENTS_CSV = PROJECT_ROOT / "data" / "students.csv"
# GRADES_CSV = PROJECT_ROOT / "data" / "grades.csv"


# def main():
#     """Render dashboard and provide simple CRUD forms.

#     - Loads a canonical internal dataframe from CSVs using the service layer.
#     - Renames internal columns to user-facing headers using
#       `DASHBOARD_DISPLAY_COLUMNS` (internal -> display mapping).
#     - Presents forms to create/update (upsert) and delete by student id.
#     """
    
#     # Sidebar with logout button
#     with st.sidebar:
#         st.header("Hello there, welcome!")
#         st.write(f"Logged in as: {st.session_state.get('user_email', 'Unknown')}")
#         if st.button("🚪 Logout", use_container_width=True):
#             st.toast("Logging out...", icon="👋")
#             time.sleep(2.0)
#             logout()
#             st.rerun()
    
#     st.title("📊 Student Grade Dashboard")
    
#     students_table, student_manager = st.tabs([":material/table: Students Table", ":material/manage_accounts: Students Manager"])

#     # Load canonical dataframe and convert internal column names to display headers.
#     data = load_dashboard_dataframe(STUDENTS_CSV, GRADES_CSV)
#     display_data = data.rename(columns=DASHBOARD_DISPLAY_COLUMNS)

#     with students_table:
#         st.header("Track their progress")
#         st.selectbox(
#             ":material/search: Find enrolled students",
#             [""] + data["name"].dropna().astype(str).tolist(),
#             filter_mode="fuzzy",
#             key="student_search"
#         )
#         st.table(display_data)

#     with student_manager:
#         st.header("Manage students")
#         existing_ids = data["id"].dropna().astype(str).tolist()
#         selected_id = st.selectbox("Search existing student by ID to edit :material/edit:", [""] + existing_ids)
#         current_record = get_student_record(STUDENTS_CSV, GRADES_CSV, selected_id) if selected_id else None

#         # Upsert form: create or update a student record.
#         with st.form("student_upsert_form"):
#             student_id = st.text_input("ID Number", value=current_record["id"] if current_record is not None else "")
#             name = st.text_input("Student Name", value=current_record["name"] if current_record is not None else "")
#             course = st.text_input("Course", value=current_record["course"] if current_record is not None else "")
#             status = st.selectbox(
#                 "Enrollment Status",
#                 ("Enrolled", "Not Enrolled"),
#                 index=0 if (current_record is None or current_record.get("status") == "Enrolled") else 1,
#             )
#             grade_value = st.text_input(
#                 "Grade Value",
#                 value="" if current_record is None or pd.isna(current_record["grade_value"]) else str(current_record["grade_value"]),
#             )
            
#             @st.dialog("Are you sure?")
#             def prompt_save():
#                 st.write("Saving your changes will modify the saved data")
#                 if st.button("Save", type="primary"):
#                     if not student_id.strip():
#                         st.error("Student ID is not found or has no inputs.")
#                     else:
#                         grade_input = grade_value.strip()
#                         upsert_student_record(
#                             STUDENTS_CSV,
#                             GRADES_CSV,
#                             student_id=student_id.strip(),
#                             name=name.strip(),
#                             course=course.strip(),
#                             status=status.strip(),
#                             grade_value=grade_input if grade_input else None,
#                         )
#                         st.success(f"Student {name.strip() or student_id.strip()} saved.")
#                         with st.spinner("Refreshing database...", show_time=True):
#                             time.sleep(1.0)
#                         st.rerun()

#             save_submitted = st.form_submit_button("Save Student")
#             if save_submitted:
#                 prompt_save()

#         # Delete form: remove a student by id.
#         with st.form("student_delete_form"):
#             delete_id = st.selectbox("Select or find an ID number", [""] + data["id"].dropna().astype(str).tolist(), key="delete_select")
#             delete_submitted = st.form_submit_button("Delete Student")
#             if delete_submitted:
#                 if not delete_id.strip():
#                     st.error("😢 Invalid input, please try again.")
#                 elif not delete_id.strip().startswith("20"):
#                     st.error('😢 Student ID should have this format: "20xx-xxxxx"')
#                 else:
#                     delete_record = get_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
#                     delete_name = delete_record["name"] if delete_record is not None else delete_id.strip()
#                     st.success(f"Student {delete_name} deleted.")
#                     delete_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
#                     with st.toast("Applying changes...", icon="✅"):
#                         time.sleep(3.0)
#                     st.rerun()


# if __name__ == "__main__":
#     main()

 
from pathlib import Path
import sys
import time
 
import pandas as pd
import streamlit as st
 

st.set_page_config(
    page_title="Admin Dashboard - Grade Management System",
    layout="wide",
    initial_sidebar_state="expanded",
)
 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
 

from auth import check_authentication, logout
from data.Subjects import SUBJECTS
from src.utils.file_handler import (
    DASHBOARD_DISPLAY_COLUMNS,
    SEMESTERS,
    VALID_GRADES,
    YEAR_LEVELS,
    compute_average,
    delete_student_record,
    get_grade_description,
    get_remarks,
    get_student_grades,
    get_student_grades_by_semester,
    get_student_record,
    load_dashboard_dataframe,
    upsert_student_record,
)
 

if st.session_state.get("role") != "admin" or not check_authentication():
    st.switch_page("pages/0_Home.py")
 

STUDENTS_CSV = PROJECT_ROOT / "data" / "students.csv"
GRADES_CSV   = PROJECT_ROOT / "data" / "grades.csv"
 
# Blur effect
st.markdown("""
<style>
[role="dialog"]:not([style*="display: none"]),
.stModal:not([style*="display: none"]),
.stModalContainer:not([style*="display: none"]),
[data-testid*="modal"]:not([style*="display: none"]) {
    position: relative;
    z-index: 99999;
}
body:has([role="dialog"]:not([style*="display: none"])),
body:has(.stModal:not([style*="display: none"])),
body:has(.stModalContainer:not([style*="display: none"])) {
    overflow: hidden;
}
body:has([role="dialog"]:not([style*="display: none"])) div[data-testid="stAppViewContainer"],
body:has(.stModal:not([style*="display: none"])) div[data-testid="stAppViewContainer"],
body:has(.stModalContainer:not([style*="display: none"])) div[data-testid="stAppViewContainer"] {
    filter: blur(5px);
    pointer-events: none;
}
body:has([role="dialog"]:not([style*="display: none"]))::before,
body:has(.stModal:not([style*="display: none"]))::before,
body:has(.stModalContainer:not([style*="display: none"]))::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.2);
    z-index: 99998;
}
</style>
""", unsafe_allow_html=True)
 

with st.sidebar:
    st.header("Hello there, welcome!")
    st.write(f"Logged in as: **{st.session_state.get('user_email', 'Unknown')}**")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.toast("Logging out...", icon="👋")
        time.sleep(2.0)
        logout()
        # Clear role so home page resets properly
        st.session_state.pop("role", None)
        st.switch_page("pages/0_Home.py")
 

st.title("📊 Student Grade Dashboard")
 
students_table, student_manager = st.tabs([
    ":material/table: Students Table",
    ":material/manage_accounts: Students Manager",
])
 

data = load_dashboard_dataframe(STUDENTS_CSV, GRADES_CSV)
 

with students_table:
    st.header("Track their progress")
 
    if data.empty:
        st.info("No students in the database yet. Add one using the Students Manager tab.")
    else:
        
        st.selectbox(
            ":material/search: Find enrolled students",
            [""] + data["name"].dropna().astype(str).tolist(),
            filter_mode="fuzzy",
            key="student_search",
        )
 
  
        st.dataframe(
            data.rename(columns=DASHBOARD_DISPLAY_COLUMNS),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"{len(data)} student(s) in the database")
 
  
        st.divider()
        st.subheader("📊 View Student Grade Report")
 
        selected_name = st.selectbox(
            "Select a student to view grades",
            ["— Select a student —"] + data["name"].dropna().astype(str).tolist(),
            key="grade_view_select",
        )
 
        if selected_name != "— Select a student —":
           
            sid = data[data["name"] == selected_name]["student_id"].values[0]
 
         
            all_grades = get_student_grades(GRADES_CSV, sid)
 
            if not all_grades:
                st.warning("No grades recorded for this student yet.")
            else:
                all_averages = []
 
                for sem in SEMESTERS:
                    # Filter grades by semester
                    sem_grades = get_student_grades_by_semester(GRADES_CSV, sid, sem)
                    st.markdown(f"**📅 {sem}**")
 
                    if not sem_grades:
                        st.caption("No grades for this semester.")
                        continue
 
                    # Build display dataframe from Grade objects
                    # Using Grade object properties: .subject, .grade, .description, .remarks
                    display_rows = [{
                        "Subject":     g.subject,
                        "Grade":       g.grade,
                        "Description": g.description,
                        "Remarks":     g.remarks,
                    } for g in sem_grades]
 
                    st.dataframe(
                        pd.DataFrame(display_rows),
                        hide_index=True,
                        use_container_width=True,
                    )
 
                    # Compute semester average using Grade.compute_average()
                    avg = compute_average(sem_grades)
                    all_averages.append(avg)
                    st.info(f"**{sem} Average: {avg} — {get_remarks(avg)}**")
 
                # Overall average
                if all_averages:
                    overall = round(sum(all_averages) / len(all_averages), 2)
                    st.success(f"🎓 **Overall Average: {overall} — {get_remarks(overall)}**")
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — STUDENTS MANAGER
# Add, edit, and delete student records
# ══════════════════════════════════════════════════════════════════════════════
with student_manager:
    st.header("Manage students")
 
    # ── Select existing student to edit ──────────────────────────────────────
    existing_ids = data["student_id"].dropna().astype(str).tolist()
    selected_id  = st.selectbox(
        "Search existing student by ID to edit :material/edit:",
        [""] + existing_ids,
        key="edit_select",
    )
 
    # If a student is selected, fetch their record as a Student object
    # get_student_record() now returns a Student object, not a dict
    current_record = get_student_record(STUDENTS_CSV, GRADES_CSV, selected_id) if selected_id else None
 
    # Get existing grades if editing
    current_grades = get_student_grades(GRADES_CSV, selected_id) if selected_id else []
 
    # ── Upsert form ───────────────────────────────────────────────────────────
    with st.form("student_upsert_form"):
        st.subheader("Student Information")
 
        c1, c2 = st.columns(2)
 
        # Pre-fill fields if editing an existing student
        # Note: current_record is now a Student object so use .id, .name etc.
        # not current_record["id"] like before
        student_id = c1.text_input(
            "ID Number",
            value=current_record.student_id if current_record is not None else "",
        )
        name = c2.text_input(
            "Student Name",
            value=current_record.name if current_record is not None else "",
        )
        course = c1.selectbox(
            "Course",
            options=list(SUBJECTS.keys()),
            index=list(SUBJECTS.keys()).index(current_record.course)
                  if current_record and current_record.course in SUBJECTS else 0,
        )
        year_level = c2.selectbox(
            "Year Level",
            options=YEAR_LEVELS,
            index=YEAR_LEVELS.index(current_record.year_level)
                  if current_record and current_record.year_level in YEAR_LEVELS else 0,
        )
        status = st.selectbox(
            "Enrollment Status",
            ("Enrolled", "Not Enrolled"),
            index=0 if (current_record is None or current_record.is_enrolled) else 1,
        )
 
        st.divider()
        st.subheader("Grades")
        st.caption("Subjects are loaded automatically based on the selected course and year level.")
 
        # ── Grade inputs ──────────────────────────────────────────────────────
        # Build grade input dict: { semester: { subject: grade_value } }
        grade_inputs: dict[str, dict[str, str]] = {}
 
        # Get subjects for the selected course and year level from subjects.py
        # Falls back to empty dict if course/year combination not found yet
        course_subjects = SUBJECTS.get(course, {}).get(year_level, {})
 
        for sem in SEMESTERS:
            grade_inputs[sem] = {}
            subjects_for_sem  = course_subjects.get(sem, [])
 
            with st.expander(f"📅 {sem}", expanded=True):
                if not subjects_for_sem:
                    st.caption(f"No subjects defined for {course} {year_level} {sem} yet.")
                    continue
 
                for subject in subjects_for_sem:
                    # Check if this student already has a grade for this subject
                    existing_grade = next(
                        (g for g in current_grades
                         if g.semester == sem and g.subject == subject),
                        None
                    )
 
                    # Pre-select current grade if editing, otherwise default to first option
                    grade_options = ["— No grade yet —"] + [str(g) for g in VALID_GRADES]
                    current_val   = str(existing_grade.grade) if existing_grade else "— No grade yet —"
                    default_idx   = grade_options.index(current_val) if current_val in grade_options else 0
 
                    grade_inputs[sem][subject] = st.selectbox(
                        subject,
                        options=grade_options,
                        index=default_idx,
                        key=f"grade_{sem}_{subject}",
                    )
 
        save_submitted = st.form_submit_button("💾 Save Student", use_container_width=True)
    if save_submitted:
    
        if not student_id.strip():
            st.error("Student ID is required.")
        else:
            upsert_student_record(
                STUDENTS_CSV,
                GRADES_CSV,
                student_id=student_id.strip(),
                name=name.strip(),
                course=course,
                year_level=year_level,
                status=status,                    grades=grade_inputs,
            )
            st.success(f"✅ Student **{name.strip() or student_id.strip()}** saved.")
            time.sleep(1.0)
            st.rerun()  
 
    st.divider()
 
    # ── Delete form ───────────────────────────────────────────────────────────
    with st.form("student_delete_form"):
        st.subheader("Delete Student")
        delete_id = st.selectbox(
            "Select a student to delete",
            [""] + data["student_id"].dropna().astype(str).tolist(),
            key="delete_select",
        )
        delete_submitted = st.form_submit_button(
            "🗑️ Delete Student",
            use_container_width=True,
        )
 
    if delete_submitted:
        if not delete_id.strip():
                st.error("😢 Please select a student to delete.")
        elif not delete_id.strip().startswith("20"):
            st.error('😢 Student ID should have this format: "20xx-xxxxx"')
        else:
            # get_student_record() returns a Student object
            # so use .name not ["name"]
            delete_record = get_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
            delete_name   = delete_record.name if delete_record is not None else delete_id.strip()

            delete_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
            st.success(f"✅ Student **{delete_name}** has been deleted.")
            time.sleep(1.0)
            st.rerun()