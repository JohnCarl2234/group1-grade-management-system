"""
This file contains the Role Selection screen, 
whether you choose to use the app as Admin or Student.

This is the first thing that the user will see upon running the app.
Once they choose any of the roles,
they will be redirected to their corresponding pages.

Admin    ->        pages/1_Login.py     (Firebase login)
Student  ->        pages/2_Student_Form_Matching    (identity form)    *not yet created
"""

import streamlit as st

st.set_page_config(
    page_title="Grade Management System"
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Sidebar - contains the information about the app
with st.sidebar:
    st.title("ℹ️ About")
    st.write("Grade Management System")
    st.write("A streamlined platform for educators to manage student records and grades.")
    st.write("📌 How to use:")
    st.write("👨‍🏫 Admin   — log in to manage students and grades")
    st.write("👨‍🎓 Student — enter your info to view your grades")
    st.divider()
    st.caption("© 2025 Grade Management System")