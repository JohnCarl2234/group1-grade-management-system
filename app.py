import streamlit as st
from streamlit_navigation_bar import st_navbar

# local executables
from auth import check_authentication
# from src.models.admin import rd_admin

# Global blur effect for modals using pure CSS + simple JS detection
st.markdown(
    """
    <style>
    /* Global blur for any visible modal/dialog */
    [role="dialog"]:not([style*="display: none"]),
    .stModal:not([style*="display: none"]),
    .stModalContainer:not([style*="display: none"]),
    [data-testid*="modal"]:not([style*="display: none"]) {
        position: relative;
        z-index: 99999;
    }
    
    /* Apply dark overlay and blur when modal is visible */
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

    """,
    unsafe_allow_html=True,
)

# back to top controller 



# # top navigation
# nav_options = ["Account", "About"]
# options = {
#     "show_menu": False,
#     "show_sidebar": False,
# }
# page = st_navbar(nav_options, options=options)


# # # side bar handle
# # with st.sidebar:
# #     st.title("Grad")
# #     st.text("Grad is designed to help our educators in managing their students’ class records, creating reports and summaries to minimize their burden on administrative tasks.")

# # Login page logic starter  
# login_logic()

# if __name__ == "__main__":
#     student_dashboard_core()

# pages = {
#     ":material/settings: Login on Grad": [
#     st.Page(login_logic, title="Create your account", icon=":material/login:"),
#     st.Page("views/report_view.py", title="About", icon=":material/info: ")
#     ]
# }
# pg = st.navigation(pages, position="sidebar")
# pg.run()


if __name__ == "__main__":
    # Check authentication and redirect to login if needed
    if not check_authentication():
        st.switch_page("pages/3_login_view.py")