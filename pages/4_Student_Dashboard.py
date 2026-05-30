from pathlib import Path
import sys
import time
 
import pandas as pd
import streamlit as st
 

st.set_page_config(
    page_title="Student Dashboard - Grade Management System",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.Subjects import SUBJECTS
from src.utils.file_handler import (
    SEMESTERS,
    compute_average,
    get_grade_description,
    get_remarks,
    get_student_grades_by_semester
)


if st.session_state.get("role") != "student" or "current_student" not in st.session_state:
    st.switch_page("page/2_Student_Lookup.py")


GRADES_CSV = PROJECT_ROOT / "data" / "grades.csv"

student = st.session_state.current_student

with st.sidebar:
    st.title("ℹ️ About")
    st.write("A streamlined platform for educators to manage student records and grades.")
    st.divider()
    st.caption("© 2025 Grade Management System · Group 1")

if st.button("← Back", type="tertiary"):
    st.session_state.pop("current_student", None)
    st.switch_page("pages/2_Student_Lookup.py")

st.markdown(
    "<h2 style='text-align:center'>📋 My Grade Report</h2>",
    unsafe_allow_html=True
)

st.divider()


c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
c1.metric("Student ID", student.student_id, width="stretch")
c2.metric("Name", student.name)
c3.metric("Course", student.course)
c4.metric("Year Level", student.year_level)

st.divider()

course_subjects = SUBJECTS.get(student.course, {}).get(student.year_level, {})

all_averages = []

for sem in SEMESTERS:
    st.subheader(f"📅 {sem}")

    subjects_for_sem = course_subjects.get(sem, [])

    recorded_grades = get_student_grades_by_semester(GRADES_CSV, student.student_id, sem)

    grades_lookup = {g.subject: g for g in recorded_grades}

    if not subjects_for_sem:
        st.caption(f"No subjects defined for the course {student.course} {student.year_level} {sem} yet")

        continue

    display_rows = []

    for subject in subjects_for_sem:
        grade_obj = grades_lookup.get(subject)

        if grade_obj:
            display_rows.append({
                "Subject": subject,
                "Grade": grade_obj.grade,
                "Description": grade_obj.description,
                "Remarks": grade_obj.remarks
            })
        else:
            display_rows.append({
                "Subject": subject, 
                "Grade": "-",
                "Description": "-",
                "Remarks": "-"
            })
    
    st.dataframe(
        pd.DataFrame(display_rows),
        hide_index=True,
        use_container_width=True
    )

    graded_subjects = [g for g in recorded_grades]
    if graded_subjects:
        average = compute_average(graded_subjects)
        all_averages.append(average)
        st.info(f"**{sem} Average: {average} - {get_remarks(average)}**")
    else:
        st.warning(f"No grades recorded for {sem} yet.")

    st.divider()


if all_averages:
    overall = round(sum(all_averages) / len(all_averages), 2)
    overall_desc = get_grade_description(overall)

    st.markdown("### 🎓 Overall Academic Standing")

    cl1, cl2, cl3 = st.columns(3)
    cl1.metric("Overall Average", overall)
    cl2.metric("Description", overall_desc)
    cl3.metric("Standing", "Passed" if overall <= 3.0 else "FAILED")

    if overall <= 3.0:
        st.success("🎉 Congratulations! You are passing all your subjects.")
    else:
        st.error("❗ You are currently failing. Please coordinate with your adviser.")
else:
    st.info("No grades have been recorded for your account yet. Please contact your professor for further instructions.")


st.caption("📌 This is a read-only view. If you believe there is an error in your grades, please contact your teacher.")