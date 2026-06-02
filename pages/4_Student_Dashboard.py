"""Student Dashboard page for the Grade Management System."""

from pathlib import Path
import sys
import time

import pandas as pd
import streamlit as st

# Resolve project root and import shared asset paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MASCOT_PATH, MASCOT_IMAGE

# Page configuration
st.set_page_config(
    page_title="Student Dashboard - Grade Management System",
    layout="wide",
    page_icon=MASCOT_IMAGE if MASCOT_IMAGE is not None else MASCOT_PATH,
    initial_sidebar_state="collapsed",
)

# Imports after path setup
from data.Subjects import SUBJECTS
from src.utils.file_handler import (
    SEMESTERS,
    compute_average,
    get_grade_description,
    get_remarks,
    get_student_grades_by_semester
)

# Prevent students from navigating here directly via the URL without first
if st.session_state.get("role") != "student" or "current_student" not in st.session_state:
    st.switch_page("pages/2_Student_Lookup.py")

# Paths to data files
GRADES_CSV = PROJECT_ROOT / "data" / "grades.csv"

# Get the current student record from session state
student = st.session_state.current_student

# CSS styles for the dashboard
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

*:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) { 
    font-family: 'DM Sans', sans-serif !important; 

[data-testid="stAppViewContainer"] {
    background: #EEF2F7;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0F1E3C 0%, #1B3468 60%, #22407A 100%) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18);
}
[data-testid="stSidebar"] * { color: #C8D8F0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }

/* ── Headings ── */
h1 { color: #0F1E3C !important; font-weight: 700 !important; font-size: 2rem !important; }
h2 { color: #0F1E3C !important; font-weight: 700 !important; font-size: 1.4rem !important; }
h3 { color: #1B3468 !important; font-weight: 600 !important; }

/* ── Student Info Cards ── */
.info-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F2;
    border-top: 4px solid #1B3468;
}
.info-card .label {
    color: #7A8BA8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.info-card .value {
    color: #0F1E3C;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.2;
}

/* ── Metric Cards ── */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 26px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F2;
    border-top: 4px solid #1B3468;
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
    font-size: 32px;
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
}

/* ── Alert Boxes ── */
[data-testid="stAlert"] { border-radius: 10px !important; font-weight: 500 !important; }

/* ── Back button ── */
[data-testid="stBaseButton-tertiary"] {
    color: #1B3468 !important;
    font-weight: 600 !important;
}

/* ── Metrics (st.metric) ── */
[data-testid="stMetric"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #E2E8F2;
    border-top: 3px solid #1B3468;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
[data-testid="stMetricLabel"] {
    color: #7A8BA8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="stMetricValue"] {
    color: #0F1E3C !important;
    font-weight: 700 !important;
}

hr { border-color: #E2E8F0 !important; }

[data-testid="stCaptionContainer"] p {
    color: #7A8BA8 !important;
    font-size: 13px !important;
}

[data-testid="stExpandSidebarButton"] span[data-testid="stIconMaterial"] {
    visibility: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.write("A streamlined platform for educators to manage student records and grades.")
    st.divider()
    st.caption("© 2026 Grade Management System · Group 1")

# Back button 
if st.button("← Back", type="tertiary"):
    st.session_state.pop("current_student", None)
    st.switch_page("pages/2_Student_Lookup.py")

# Page Title 
st.title("📋 My Grade Report")

# Student Info Cards 
c1, c2, c3, c4, c5= st.columns(5)
with c1:
    st.markdown(f"""
        <div class="info-card">
            <div class="label">Student ID</div>
            <div class="value">{student.student_id}</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="info-card" style="border-top-color:#3B82F6">
            <div class="label">Full Name</div>
            <div class="value" style="font-size:15px">{student.name}</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="info-card" style="border-top-color:#8B5CF6">
            <div class="label">Course</div>
            <div class="value">{student.course}</div>
        </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
        <div class="info-card" style="border-top-color:#10B981">
            <div class="label">Year Level</div>
            <div class="value">{student.year_level}</div>
        </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
        <div class="info-card" style="border-top-color:#10B981">
            <div class="label">Enrollment Status</div>
            <div class="value">{student.status}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# Grade Tables 
course_subjects = SUBJECTS.get(student.course, {}).get(student.year_level, {})
all_averages = []

for sem in SEMESTERS:
    st.subheader(f"📅 {sem}")

    subjects_for_sem = course_subjects.get(sem, [])
    recorded_grades  = get_student_grades_by_semester(GRADES_CSV, student.student_id, sem)
    grades_lookup    = {g.subject: g for g in recorded_grades}

    if not subjects_for_sem:
        st.caption(f"No subjects defined for {student.course} {student.year_level} {sem} yet.")
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
        width='stretch',
    )

    graded_subjects = [g for g in recorded_grades]
    if graded_subjects:
        average = compute_average(graded_subjects)
        all_averages.append(average)
        st.info(f"**{sem} Average: {average} — {get_remarks(average)}**")
    else:
        st.warning(f"No grades recorded for {sem} yet.")

    st.divider()

# Overall Standing
if all_averages:
    overall      = round(sum(all_averages) / len(all_averages), 2)
    overall_desc = get_grade_description(overall)
    passed       = overall <= 3.0

    st.subheader("🎓 Overall Academic Standing")
    st.markdown("<br>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card blue">
                <div class="label">Overall Average</div>
                <div class="value">{overall}</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="label">Description</div>
                <div class="value" style="font-size:18px">{overall_desc}</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        # Color the standing card green if passing, red if failing
        color = "green" if passed else "red"
        standing = "Passed ✓" if passed else "Failed ✗"
        st.markdown(f"""
            <div class="metric-card {color}">
                <div class="label">Standing</div>
                <div class="value" style="font-size:22px">{standing}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Final remarks based on overall standing
    if passed:
        st.success("🎉 Congratulations! You are passing all your subjects.")
    else:
        st.error("❗ You are currently failing. Please coordinate with your adviser.")

else:
    # No grades recorded at all
    st.info("No grades have been recorded for your account yet. Please contact your professor for further instructions.")

# Footer note
st.markdown("<br>", unsafe_allow_html=True)
st.caption("📌 This is a read-only view. If you believe there is an error in your grades, please contact your teacher.")