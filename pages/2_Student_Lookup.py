"""
This is the Student Lookup page 

This will only appear when choosing the 'Student' role
The student will need to fill in the needed information 
and the system will look at the database if there is any match;
if so, they will proceed to their corresponding dashboard.
"""

import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="Student Lookup - Grade Management System", 
    layout="centered",
    initial_sidebar_state="expanded"
)

from data.Subjects import SUBJECTS
from models.Student import Student
from src.utils.file_handler import (YEAR_LEVELS, load_students_dataframe)

STUDENTS_CSV = PROJECT_ROOT /"data"/"students.csv"

if st.session_state.get("role") != "student":
    st.switch_page("pages/0_Home.py")

with st.sidebar:
    st.title("ℹ️ About")
    st.write("Grade Management System")
    st.write("A streamlined platform for educators to manage student records and grades.")
    st.divider()
    st.caption("© 2025 Grade Management System · Group 1")

    st.markdown("""
 <style>
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0F1E3C 0%, #1B3468 60%, #22407A 100%) !important;
}
[data-testid="stSidebar"] * { color: #C8D8F0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }
 
hr { border-color: #D0D9E8 !important; }
</style>
""", unsafe_allow_html=True)

def find_student(student_id: str, name: str, course: str, year_level: str) -> Student | None:
    df = load_students_dataframe(STUDENTS_CSV)

    for _, row in df.iterrows():
        student = Student.from_dict(row.to_dict())

        if student.does_match(student_id, name, course, year_level):
            return student
        
    return None

if st.button("Back", type="tertiary"):
    st.session_state.pop("role", None)
    st.switch_page("pages/0_Home.py")

st.markdown(
    "<h2 style='text-align:center'>👨‍🎓 Student Record Lookup</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray; margin-bottom:2rem'>"
    "Fill in your information exactly as registered to access your grades."
    "</p>",
    unsafe_allow_html=True
)

with st.form("student_lookup_form", border=True):
    student_id = st.text_input(
        "Student ID", 
        placeholder="e.g. 2025-01234",
        help="Enter your student ID exactly as registered"
    )

    name = st.text_input(
        "Full Name",
        placeholder="e.g. Arizo, Rishelvin C.",
        help="Enter your full name, surname first then first name and middle initial"
    )

    col1, col2 = st.columns(2)

    course = col1.selectbox(
        "Course",
        options=list(SUBJECTS.keys()),
        help="Select your course"
    )

    year_level = col2.selectbox(
        "Year Level",
        options=YEAR_LEVELS,
        help="Select your current year level"
    )

    submitted = st.form_submit_button(
        "🔍 Find My Record",
        use_container_width=True,
        type="primary"
    )

if submitted:
    if not student_id.strip() or not name.strip():
        st.error("Please fill in all fields.", icon="⚠️")

    else:
        with st.spinner("Searching for your record..."):
            matched_student = find_student(student_id, name, course, year_level)
        
        if matched_student:
            st.session_state.current_student = matched_student

            st.success("✅ Record found! Loading your dashboard...")

            st.switch_page("pages/4_Student_Dashboard.py")
        
        else:
            st.error(
                "❌ No record found matching your details. "
                "Please double-check your information or contact your teacher."
            )