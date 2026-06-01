"""Login page for the Grade Management System."""
import streamlit as st
import sys
import time
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Login - Grade Management System",
    layout="centered"
)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import check_authentication, set_authenticated, sign_in_with_firebase

# If the user is already authenticated, redirect to the admin dashboard
if check_authentication():
    st.switch_page("pages/1_Admin_Dashboard.py")

def main():
    """Render login form."""
    # Sidebar for login page
    with st.sidebar:
        st.title("ℹ️ About")
        st.write("Grade Management System")
        st.write("A streamlined platform for educators to manage student records and grades.")
        st.divider()
        st.caption("© 2026 Grade Management System")

        st.markdown("""
 <style>
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0F1E3C 0%, #1B3468 60%, #22407A 100%) !important;
}
[data-testid="stSidebar"] * { color: #C8D8F0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }
 
hr { border-color: #D0D9E8 !important; }
</style>
""", unsafe_allow_html=True)
    
    # Page title
    st.title("Grade Management System")

    # Back button
    if st.button("← Back", type="tertiary"):
        st.session_state.pop("role", None)
        st.session_state.pop("authenticated", None)
        st.switch_page("pages/0_Home.py")
    
    # Login form
    with st.form("login_view", clear_on_submit=False, enter_to_submit=True, border=True):
        st.subheader("Hello there 👋")
        st.write("Login with your school account to continue.")
        username = st.text_input(
            "Email",
            placeholder="@evsu.edu.ph",
            help="EVSU emails are only recognized"
        )
        password = st.text_input(
            "Password",
            placeholder="Enter your password here",
            type="password",
            help="If you're having trouble logging in, contact the administrator for assistance."
        )
        submit_button = st.form_submit_button(label='Login')
        
        if submit_button:
            # Basic validation to check for empty fields before attempting Firebase authentication
            if not username.strip() or not password.strip():
                st.error("Empty fields, please try again.", icon="🫠")
                return False

            # Attempt to authenticate with Firebase
            auth_result = sign_in_with_firebase(username.strip(), password.strip())

            if auth_result.get("success"):
                st.success("Logging in...", icon="🪵")
                set_authenticated(True, auth_result.get("email", username))
                st.session_state.firebase_user = {
                    "email": auth_result.get("email"),
                    "id_token": auth_result.get("id_token"),
                    "refresh_token": auth_result.get("refresh_token"),
                    "local_id": auth_result.get("local_id"),
                    "display_name": auth_result.get("display_name"),
                }
                time.sleep(1.0)
                st.rerun()

            # Show Firebase error message (fallback to generic) and a short auth status.
            st.error(auth_result.get("error", "Credentials are not recognized by Firebase"), icon="😢")

if __name__ == "__main__":
    main()