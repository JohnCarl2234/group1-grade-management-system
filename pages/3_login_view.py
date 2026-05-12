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

from auth import set_authenticated


class vdt_main():
    def __init__(self, email, passphrase):
        self.email = email 
        self.passphrase = passphrase

    def validate(self):
        if self.email == "acostajohncarl33@evsu.edu.ph" and self.passphrase == "carleaux":
            st.success("Logging in...", icon="🪵")
            return True
        elif self.email == "" or self.passphrase == "":
            st.error("Empty fields, please try again.", icon="🫠")
        else:
            st.error("Incorrect credentials, please try again.", icon="😢")


def main():
    """Render login form."""
    st.title("Grade Management System")
    
    with st.form("login_view", clear_on_submit=False, enter_to_submit=True, border=True):
        st.subheader("Hello there 👋")
        st.write("Login with your school account to continue.")
        username = st.text_input(
            "Email",
            placeholder="@evsu.edu.ph",
            help="In the meantime, EVSU emails are only recognized"
        )
        password = st.text_input(
            "Password",
            placeholder="Enter your password here",
            type="password",
            max_chars=13,
            help="Should be 13 characters long"
        )
        submit_button = st.form_submit_button(label='Login')
        
        if submit_button:
            auth_instance = vdt_main(username, password).validate()
            time.sleep(2.0)
            
            if auth_instance:
                # Mark session as authenticated and rerun app so main shows dashboard
                set_authenticated(True, username)
                st.switch_page("pages/1_Dashboard.py")
            else:
                # Keep user on login page and show errors from validate()
                return False


if __name__ == "__main__":
    main()