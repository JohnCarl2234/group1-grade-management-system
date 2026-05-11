import streamlit as st

def login_logic():
    class vdt_main():
        def __init__(self, email, passphrase):
            self.email = email 
            self.passphrase = passphrase

        def validate(self):
            if self.email == "acostajohncarl33@evsu.edu.ph" and self.passphrase == "carleaux":
                st.success("Logging in...", icon="🪵")
            elif self.email == "" or self.passphrase == "":
                st.error("Empty fields, please try again.", icon="🫠")
            else:
                st.error("Incorrect credentials, please try again.", icon="😢")

    with st.form("login_view", clear_on_submit=False, enter_to_submit=True, border=True):
            st.subheader("Hello there 👋")
            st.write("Login with your school account to continue.")
            username = st.text_input("Email", placeholder="@evsu.edu.ph", help="In the meantime, EVSU emails are only recognized")
            password = st.text_input("Password", placeholder="Enter your password here", type="password", max_chars=13, help="Should be 13 characters long")
            submit_button = st.form_submit_button(label='Login')
            if submit_button:
                validator_start = vdt_main(username, password)
                validator_start.validate()