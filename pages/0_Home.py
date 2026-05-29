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
    page_title="Grade Management System",
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

st.markdown("""
            <style>

            div.container {padding-top: 5rem;}

            div[data-testid="column"] button {
            height: 160px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            border-radius: 16px !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
            }

            div[data-testid="column"] button:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 12px 28px rgba(0,0,0,0.12) !important;
            }

            </style>
""",
unsafe_allow_html=True
)

# Header - Just like the title and its corresponding subheaders
st.markdown(
    "<h1 style='text-align:center; margin-bottom:1px'>🎓 Grade Management System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray; margin-bottom:2rem'>Eastern Visayas State University</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align:center; margin-bottom:1.5rem; font-weight: bold; font-size: 2rem'>Who are you?</h3>",
    unsafe_allow_html=True
)

# Role selection buttons - the Admin and Student
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        "<p style='text-align:center; font-size:2.5rem; margin-bottom:0'>🛡️</p>"
        "<p style='text-align:center; color:gray; font-size:0.83rem; margin-bottom:8px'>"
        "Manage students, grades,<br>and records</p>",
        unsafe_allow_html=True
    )
    if st.button("Admin", use_container_width=True, type="primary", key="btn_admin"):
        # Clear any leftover state from a previous session
        st.session_state.pop("current_student", None)
        st.session_state.pop("authenticated", None)
        st.session_state.role = "admin"
        st.switch_page("pages/3_Login.py")

with col2:
    st.markdown(
        "<p style='text-align:center; font-size:2.5rem; margin-bottom:0'>👨‍🎓</p>"
        "<p style='text-align:center; color:gray; font-size:0.83rem; margin-bottom:8px'>"
        "View your grades<br>and academic record</p>",
        unsafe_allow_html=True
    )
    if st.button("Student", use_container_width=True, type="primary", key="btn_student"):
        # Clear any leftover state from a previous session
        st.session_state.pop("current_student", None)
        st.session_state.pop("authenticated", None)
        st.session_state.role = "student"
        st.switch_page("pages/2_Student_Lookup.py")
 
# Footer - contains the copyright text
st.markdown(
    "<br><hr><p style='text-align:center; color:lightgray; font-size:0.75rem'>"
    "© 2025 Grade Management System · Group 1</p>",
    unsafe_allow_html=True
)