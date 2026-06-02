""""
Admin Dashboard page for the Grade Management System.
This is the main admin interface for managing student records and grades.
"""

from pathlib import Path
import sys
import time

import pandas as pd
import streamlit as st

# Resolve project root early so we can import shared config
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import shared config for asset paths
from src.config import MASCOT_PATH, MASCOT_IMAGE

#Page Configuration
st.set_page_config(
    page_title="Admin Dashboard - Grade Management System",
    layout="wide",
    page_icon=MASCOT_IMAGE if MASCOT_IMAGE is not None else MASCOT_PATH,
    initial_sidebar_state="expanded",
)

#Imports
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

# Access Control: Only allow admins who are authenticated to view this page
if st.session_state.get("role") != "admin" or not check_authentication():
    st.switch_page("pages/0_Home.py")

#CVS file paths
STUDENTS_CSV = PROJECT_ROOT / "data" / "students.csv"
GRADES_CSV   = PROJECT_ROOT / "data" / "grades.csv"


# Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) { 
    font-family: 'DM Sans', sans-serif !important; 
}

/* ── Background ── */
[data-testid="stAppViewContainer"] {
    background: #EEF2F7;
}
[data-testid="stHeader"] {
    background: transparent;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0F1E3C 0%, #1B3468 60%, #22407A 100%) !important;
    border-right: none;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18);
}
[data-testid="stSidebar"] * {
    color: #C8D8F0 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
}
[data-testid="stSidebar"] button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.18) !important;
    border-color: rgba(255,255,255,0.35) !important;
}

/* ── Main Title ── */
h1 {
    color: #0F1E3C !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    letter-spacing: -0.5px !important;
}

/* ── Section headers ── */
h2 {
    color: #0F1E3C !important;
    font-weight: 700 !important;
    font-size: 1.4rem !important;
}
h3 {
    color: #1B3468 !important;
    font-weight: 600 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 5px;
    gap: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border: 1px solid #DDE3EE;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    color: #64748B !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0F1E3C, #1B3468) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(15,30,60,0.3) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] p {
    color: #ffffff !important;
}

/* ── Metric Cards ── */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 26px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F2;
    border-top: 4px solid #1B3468;
    transition: box-shadow 0.2s; 
    text-align: center;        
}    
.metric-card:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.10);
}
.metric-card .label {
    color: #7A8BA8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.metric-card .value {
    color: #0F1E3C;
    font-size: 34px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-card .sub {
    color: #A0AEC0;
    font-size: 12px;
    font-weight: 500;
}
.metric-card.green  { border-top-color: #10B981; }
.metric-card.red    { border-top-color: #EF4444; }
.metric-card.blue   { border-top-color: #3B82F6; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07) !important;
    border: 1px solid #DDE3EE !important;
    background: #ffffff !important;
}
[data-testid="stDataFrame"] thead tr th {
    background-color: #0F1E3C !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    padding: 14px 18px !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td {
    background-color: #F7FAFF !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background-color: #EBF0FF !important;
}
[data-testid="stDataFrame"] tbody tr td {
    font-size: 14px !important;
    color: #2D3748 !important;
    padding: 11px 18px !important;
    border-bottom: 1px solid #EDF2F7 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Selectboxes & Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input {
    background: #ffffff !important;
    border: 1.5px solid #D0D9E8 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    font-size: 14px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #1B3468 !important;
    box-shadow: 0 0 0 3px rgba(27,52,104,0.12) !important;
}

/* ── Form Submit Buttons ── */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #0F1E3C 0%, #1B3468 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 12px 24px !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 14px rgba(15,30,60,0.25) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    box-shadow: 0 6px 20px rgba(15,30,60,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── Alert Boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #DDE3EE !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #0F1E3C !important;
}
[data-testid="stExpander"] summary svg,
[data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {
    display: none !important;
}
/* ── Hide sidebar toggle icon text bleed ── */
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* ── Divider ── */
hr { border-color: #E2E8F0 !important; }

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    color: #7A8BA8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ── Modal blur ── */
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


# Sidebar 
with st.sidebar:
    st.markdown("### 👋 Welcome back!")
    st.markdown(f"Logged in as:")
    st.markdown(f"**{st.session_state.get('user_email', 'Unknown')}**")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.toast("Logging out...", icon="👋")
        time.sleep(2.0)
        logout()
        st.session_state.pop("role", None)
        st.switch_page("pages/0_Home.py")


logo_path = "./app/static/logo.png"
st.markdown(
    f"""
    <div style="display: flex; align-items: left; gap: 15px; margin-bottom: 20px;">
        <img src="{logo_path}" width="150vw" style="max-height:60px; object-fit: contain;">
    </div>
    """,
    unsafe_allow_html=True
)

#  Title 
st.title("Student Grade Dashboard")

#Main Tabs
students_table, student_manager = st.tabs([
    "Students Table",
    "Students Manager",
])

#Load Student Data
data = load_dashboard_dataframe(STUDENTS_CSV, GRADES_CSV)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — STUDENTS TABLE
# ══════════════════════════════════════════════════════════════════════════════
with students_table:
    st.header("Track their progress")

    if data.empty:
        st.info("No students in the database yet. Add one using the Students Manager tab.")
    else:
        # Enrollment Metric Cards 
        total = len(data)
        enrolled_count = len(data[data["status"] == "Enrolled"]) if "status" in data.columns else 0
        not_enrolled   = total - enrolled_count

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="metric-card blue">
                    <div class="label">Total Students</div>
                    <div class="value">{total}</div>
                    <div class="sub">in the database</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
        <div class="metric-card green">
                <div class="label">Enrolled</div>
                <div class="value">{enrolled_count}</div>
                <div class="sub">currently active</div>
        </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
        <div class="metric-card red">
                <div class="label">Not Enrolled</div>
                <div class="value">{not_enrolled}</div>
                <div class="sub">inactive students</div>
        </div>
            """, unsafe_allow_html=True)
       
        st.markdown("<br>", unsafe_allow_html=True)

        # Search Bar
        st.selectbox(
            "Search Enrolled Students",
            [""] + data["name"].dropna().astype(str).tolist(),
            filter_mode="fuzzy",
            key="student_search",
        )

        #  Student Records Table
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
        )

        # Grade Report 
        st.divider()
        st.subheader("📊 View Student Grade Report")

        # Get student ID from the selected name
        selected_name = st.selectbox(
            "Select a student to view grades",
            ["Select a student"] + data["name"].dropna().astype(str).tolist(),
            key="grade_view_select",
        )

        if selected_name != "Select a student":
            sid = data[data["name"] == selected_name]["student_id"].values[0]

        # Fetch full student record to get course and year level
            selected_record = get_student_record(STUDENTS_CSV, GRADES_CSV, sid)
            course_subjects = SUBJECTS.get(
                selected_record.course     if selected_record else "", {}
            ).get(
                selected_record.year_level if selected_record else "", {}
            )

            all_averages = []

        # Display grades per semester
            for sem in SEMESTERS:
                st.markdown(f"**📅 {sem}**")

                subjects_for_sem = course_subjects.get(sem, [])
                sem_grades       = get_student_grades_by_semester(GRADES_CSV, sid, sem)
                grades_lookup    = {g.subject: g for g in sem_grades}

                if not subjects_for_sem:
                    st.caption("No subjects defined yet.")
                    continue

                display_rows = []
                for subject in subjects_for_sem:
                    grade_obj = grades_lookup.get(subject)
                    if grade_obj:
                        display_rows.append({
                            "Subject":     subject,
                            "Grade":       grade_obj.grade,
                            "Description": grade_obj.description,
                            "Remarks":     grade_obj.remarks,
                        })
                    else:
                        display_rows.append({
                            "Subject":     subject,
                            "Grade":       "—",
                            "Description": "—",
                            "Remarks":     "Not yet graded",
                        })

                st.dataframe(
                    pd.DataFrame(display_rows),
                    hide_index=True,
                    use_container_width=True,
                )

                if sem_grades:
                    avg = compute_average(sem_grades)
                    all_averages.append(avg)
                    st.info(f"**{sem} Average: {avg} — {get_remarks(avg)}**")
                else:
                    st.warning(f"No grades recorded for {sem} yet.")

            if all_averages:
                overall = round(sum(all_averages) / len(all_averages), 2)
                st.success(f"🎓 **Overall Average: {overall} — {get_remarks(overall)}**")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — STUDENTS MANAGER
# ══════════════════════════════════════════════════════════════════════════════
with student_manager:
    st.header("Manage students")

# Select Existing Student to Edit 
    existing_ids = data["student_id"].dropna().astype(str).tolist()
    selected_id  = st.selectbox(
        "Search existing student by ID to edit or add a new student",
        ["Add new student"] + existing_ids,
        key="edit_select",
    )

# Pre-load existing record and grades if editing
    current_record = get_student_record(STUDENTS_CSV, GRADES_CSV, selected_id) if selected_id else None
    current_grades = get_student_grades(GRADES_CSV, selected_id) if selected_id else []

# Student Form (CREATE / UPDATE)
    with st.form("student_upsert_form"):
        st.subheader("Student Information")

        c1, c2 = st.columns(2)

# ID Number, Name, Course, Year Level, Enrollment Status
        student_id = c1.text_input(
            "ID Number",
            value=current_record.student_id if current_record is not None else "",
            placeholder="e.g. 2025-01234",
        )
        name = c2.text_input(
            "Student Name",
            value=current_record.name if current_record is not None else "",
            placeholder="e.g. Arizo, Rishelvin C.",
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

        # Grade Inputs
        grade_inputs: dict[str, dict[str, str]] = {}
        course_subjects = SUBJECTS.get(course, {}).get(year_level, {})

        for sem in SEMESTERS:
            grade_inputs[sem] = {}
            subjects_for_sem  = course_subjects.get(sem, [])

            with st.expander(f"{sem}", expanded=True):
                if not subjects_for_sem:
                    st.caption(f"No subjects defined for {course} {year_level} {sem} yet.")
                    continue

        # Check if a grade already exists for this subject
                for subject in subjects_for_sem:
                    existing_grade = next(
                        (g for g in current_grades
                         if g.semester == sem and g.subject == subject),
                        None
                    )

                    grade_options = ["No grade yet"] + [str(g) for g in VALID_GRADES]
                    current_val   = str(existing_grade.grade) if existing_grade else "No grade yet"
                    default_idx   = grade_options.index(current_val) if current_val in grade_options else 0

                    grade_inputs[sem][subject] = st.selectbox(
                        subject,
                        options=grade_options,
                        index=default_idx,
                        key=f"grade_{selected_id}_{sem}_{subject}",
                    )

        save_submitted = st.form_submit_button("💾 Save Student", use_container_width=True)

        # Save Handler: Validate and upsert student record and grades
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
                status=status,
                grades=grade_inputs,
            )
            st.success(f"✅ Student **{name.strip() or student_id.strip()}** saved.")
            time.sleep(1.0)
            st.rerun()

    st.divider()

        # Delete Student Record
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

        # Delete Handler: Validate and delete student record and grades
    if delete_submitted:
        if not delete_id.strip():
            st.error("😢 Please select a student to delete.")
        elif not delete_id.strip().startswith("20"):
            st.error('😢 Student ID should have this format: "20xx-xxxxx"')
        else:
            delete_record = get_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
            delete_name   = delete_record.name if delete_record is not None else delete_id.strip()

            delete_student_record(STUDENTS_CSV, GRADES_CSV, delete_id.strip())
            st.success(f"✅ Student **{delete_name}** has been deleted.")
            time.sleep(1.0)
            st.rerun()