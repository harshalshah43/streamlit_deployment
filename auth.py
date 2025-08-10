import streamlit as st
from creds import *

def init_session():
    """Initialize session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

def login():
    """Render login UI and handle authentication."""
    init_session()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {USER_CREDENTIALS[username]['name']}!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    """Logout the current user."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out!")
    st.rerun()

def is_authenticated():
    """Check if user is logged in."""
    init_session()
    return st.session_state.logged_in

def get_current_user():
    """Get current logged-in user details."""
    if is_authenticated():
        return USER_CREDENTIALS[st.session_state.username]
    return None
