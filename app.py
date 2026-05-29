import streamlit as st
from auth import check_authentication

st.set_page_config(
    page_title="Grade Management System",
    layout="centered",
    initial_sidebar_state="collapsed",
)


role = st.session_state.get("role")           # "admin" | "student" | None
is_authenticated = check_authentication()                 # True if admin logged in via Firebase
has_student = "current_student" in st.session_state  # True if student passed lookup

# Define all pages
home_page = st.Page(
    "pages/0_Home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)
 
login_page = st.Page(
    "pages/3_Login.py",
    title="Admin Login",
    icon=":material/login:",
)
 
admin_dashboard_page = st.Page(
    "pages/1_Admin_Dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
)
 
student_lookup_page = st.Page(
    "pages/2_Student_Lookup.py",
    title="Student Lookup",
    icon=":material/search:",
)
 
student_dashboard_page = st.Page(
    "pages/4_Student_Dashboard.py",
    title="My Grades",
    icon=":material/school:",
)

if role == "admin":
    pages = [home_page, admin_dashboard_page] if is_authenticated else [home_page, login_page]
 
elif role == "student":
    pages = [home_page, student_dashboard_page] if has_student else [home_page, student_lookup_page]
 
else:
    pages = [home_page]

pg = st.navigation(pages, position="hidden")  # hidden = no sidebar nav shown
pg.run()
