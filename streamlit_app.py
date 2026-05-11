import streamlit as st
from streamlit_navigation_bar import st_navbar
from views.login_view import login_logic

# top navigation
nav_options = ["Account", "About"]
options = {
    "show_menu": False,
    "show_sidebar": False,
}
page = st_navbar(nav_options, options=options)


# # side bar handle
# with st.sidebar:
#     st.title("Grad")
#     st.text("Grad is designed to help our educators in managing their students’ class records, creating reports and summaries to minimize their burden on administrative tasks.")

# Login page logic starter  
login_logic()