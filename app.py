import streamlit as st
from auth import check_authentication

st.set_page_config(
    page_title="Grade Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global blur effect for modals
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

# Check authentication status
is_authenticated = check_authentication()

# Define public pages (always visible)
public_pages = [
    st.Page("pages/3_Login View.py", title="Login", icon=":material/login:"),
]

# Define protected pages (only visible when authenticated)
protected_pages = [
    st.Page("pages/1_Dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("pages/2_Students.py", title="Students", icon=":material/group:"),
]

# Build navigation based on authentication
pages = protected_pages if is_authenticated else public_pages

# Render the multi-page app
pg = st.navigation(pages, position="sidebar")
pg.run()
