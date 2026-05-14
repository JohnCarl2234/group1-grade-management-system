from hashlib import sha256
import json
import os
import urllib.error
import urllib.request

import streamlit as st


AUTH_TOKEN_KEY = "auth_token"
AUTH_USER_KEY = "auth_user"
AUTH_SECRET = "group1-grade-management-system-auth"


def get_firebase_api_key() -> str | None:
    """Return the Firebase Web API key from secrets or environment variables."""
    try:
        api_key = st.secrets.get("FIREBASE_API_KEY")
        if api_key:
            return str(api_key).strip()
    except Exception:
        pass

    api_key = os.getenv("FIREBASE_API_KEY")
    return api_key.strip() if api_key else None


def _build_auth_token(user_email: str) -> str:
    """Build a stable token for the current user."""
    normalized_email = str(user_email).strip().lower()
    return sha256(f"{normalized_email}:{AUTH_SECRET}".encode("utf-8")).hexdigest()


def _restore_auth_from_query_params() -> bool:
    """Restore authentication from persistent query parameters."""
    user_email = st.query_params.get(AUTH_USER_KEY)
    token = st.query_params.get(AUTH_TOKEN_KEY)

    if not user_email or not token:
        return False

    if token != _build_auth_token(user_email):
        return False

    st.session_state.authenticated = True
    st.session_state.user_email = user_email
    return True


def sign_in_with_firebase(email: str, password: str) -> dict[str, object]:
    """Sign in a user with Firebase Authentication via REST API."""
    api_key = get_firebase_api_key()
    if not api_key:
        return {
            "success": False,
            "error": "Firebase API key is not configured. Set FIREBASE_API_KEY in Streamlit secrets or the environment.",
        }

    endpoint = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = json.dumps(
        {
            "email": str(email).strip(),
            "password": str(password),
            "returnSecureToken": True,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        return {
            "success": True,
            "email": response_data.get("email", str(email).strip()),
            "id_token": response_data.get("idToken"),
            "refresh_token": response_data.get("refreshToken"),
            "local_id": response_data.get("localId"),
            "display_name": response_data.get("displayName"),
        }
    except urllib.error.HTTPError as exc:
        try:
            error_payload = json.loads(exc.read().decode("utf-8"))
            message = error_payload["error"]["message"]
        except Exception:
            message = f"HTTP {exc.code}"

        friendly_messages = {
            "INVALID_PASSWORD": "Incorrect password.",
            "EMAIL_NOT_FOUND": "No account found for that email.",
            "USER_DISABLED": "This account has been disabled.",
            "INVALID_EMAIL": "Please enter a valid email address.",
        }

        return {
            "success": False,
            "error": friendly_messages.get(message, f"Firebase login failed: {message}"),
        }
    except urllib.error.URLError as exc:
        return {
            "success": False,
            "error": f"Could not reach Firebase: {exc.reason}",
        }


def check_authentication():
    """Check if user is authenticated and return status."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    return _restore_auth_from_query_params()


def set_authenticated(authenticated: bool, user_email: str = None):
    """Set authentication status and optionally store user email."""
    st.session_state.authenticated = authenticated

    if authenticated and user_email:
        st.session_state.user_email = user_email
        st.query_params[AUTH_USER_KEY] = user_email
        st.query_params[AUTH_TOKEN_KEY] = _build_auth_token(user_email)
        return

    if "user_email" in st.session_state:
        del st.session_state.user_email

    st.query_params.pop(AUTH_USER_KEY, None)
    st.query_params.pop(AUTH_TOKEN_KEY, None)


def get_user_email():
    """Get authenticated user's email if available."""
    return st.session_state.get("user_email", None)


def logout():
    """Clear authentication status."""
    set_authenticated(False)