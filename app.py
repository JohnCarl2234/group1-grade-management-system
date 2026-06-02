import streamlit as st
from auth import check_authentication

st.set_page_config(
    page_title="Grade Management System",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,opsz,wght@0,17..18,400..700;1,17..18,400..700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Google Sans', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

from src.config import MASCOT_PATH

logo = MASCOT_PATH

pages = [
    st.Page("pages/0_Home.py",              title="Home",           icon=":material/home:",     default=True),
    st.Page("pages/3_Login.py",             title="Admin Login",    icon=":material/login:"),
    st.Page("pages/1_Admin_Dashboard.py",   title="Dashboard",      icon=":material/dashboard:"),
    st.Page("pages/2_Student_Lookup.py",    title="Student Lookup", icon=":material/search:"),
    st.Page("pages/4_Student_Dashboard.py", title="My Grades",      icon=":material/school:"),
]

pg = st.navigation(pages, position="hidden")  # hidden = no sidebar nav shown
pg.run()