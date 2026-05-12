"""Authentication utilities for the Streamlit app."""
import streamlit as st


def check_authentication():
    """Check if user is authenticated and return status."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated


def set_authenticated(authenticated: bool, user_email: str = None):
    """Set authentication status and optionally store user email."""
    st.session_state.authenticated = authenticated
    if user_email:
        st.session_state.user_email = user_email


def get_user_email():
    """Get authenticated user's email if available."""
    return st.session_state.get('user_email', None)


def logout():
    """Clear authentication status."""
    st.session_state.authenticated = False
    if 'user_email' in st.session_state:
        del st.session_state.user_email