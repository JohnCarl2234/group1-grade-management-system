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

if st.session.get("role") != "student":
    st.switch_page("pages/0_Home.py")

with st.sidebar:
    st.title("ℹ️ About")
    st.write("Grade Management System")
    st.write("A streamlined platform for educators to manage student records and grades.")
    st.divider()
    st.caption("© 2025 Grade Management System · Group 1")

