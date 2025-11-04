import sys
import os
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import threading
from services.automation import run_scheduler

import streamlit as st
from data.user_db import register_user, login_user, delete_user
from models.user import User

st.set_page_config(
    page_title="Login Page",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)
if st.session_state.get("logged_in", False):
    st.switch_page("pages/main_app.py")

st.title("Welcome to Budget Manager 💰")
st.markdown("Please log in or register to continue.")

tab1 , tab2 = st.tabs(["🔐 Login", "📝 Register"])
#Login Tab
with tab1:
    st.subheader("Login to Your Account")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_user_button = st.form_submit_button("Login")
        if login_user_button:
            user = login_user(username, password)
            if user:
                st.success(f"Welcome back, {user.name}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = user.username
                st.session_state['name'] = user.name
                st.success(f"Welcome back, {st.session_state['name']}!")
                try:
                    threading.Thread(target=run_scheduler, args=(user.email,), daemon=True).start()
                    print(f"📅 Scheduler started for {user.email}")
                except Exception as e:
                    print(f"⚠️ Failed to start scheduler: {e}")
                st.markdown("### ✅ You are logged in.")
                st.switch_page("pages/main_app.py")
            else:
                st.error("Invalid username or password. Please try again.")

# Registration Tab
with tab2:
    st.subheader("Register New Account")
    with st.form("register_form"):
        new_username = st.text_input("Username", key="reg_user")
        new_email = st.text_input("Email", key="reg_email")
        new_name = st.text_input("Name", key="reg_name")
        new_password = st.text_input("New Password", type="password", key="reg_pass")
        st.markdown("**Password Requirements:**")
        st.markdown("""
        <small>Password must contain:
        - At least 8 characters
        - Uppercase and lowercase letters
        - At least one number and one special character</small>
        """, unsafe_allow_html=True)
        if new_password:
            requirements = [
                len(new_password) >= 8,
                any(c.islower() for c in new_password),
                any(c.isupper() for c in new_password),
                any(c.isdigit() for c in new_password),
                any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in new_password)
            ]
            if all(requirements):
                st.success("Password meets all requirements.")
            else:
                st.error("Password does not meet all requirements.")
        agree = st.checkbox("I agree to the Terms and Conditions", key="reg_agree")
        reg_button = st.form_submit_button("Register")
        if reg_button:
            if not agree:
                st.error("You must agree to the Terms and Conditions to register.")
            else:
                try:
                    register_user(new_username, new_password, new_email, new_name)
                    st.success("Registration successful! You can now log in.")

                    user = login_user(new_username, new_password)
                    if user:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = user.username
                        st.session_state['name'] = user.name
                        st.success(f"Welcome, {st.session_state['name']}!")
                        st.markdown("### ✅ You are logged in.")
                        st.switch_page("pages/main_app.py")
                except ValueError as ve:
                    st.error(str(ve))
                except Exception as e:
                    st.error("An error occurred during registration. Please try again.")
