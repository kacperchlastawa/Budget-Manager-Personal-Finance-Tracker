import streamlit as st
from data.user_db import *
from models.user import User

st.set_page_config(
    page_title="Login Page",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)
if not st.session_state.get("logged_in", False):
    st.warning("🔒 You must log in to access this page.")
    st.stop()

#######
#SIDEBAR
#######
# SIDEBAR — widoczny tylko dla zalogowanego użytkownika
if st.session_state.get('logged_in', True):
    with st.sidebar:
        st.title("👤 User Panel")
        st.markdown(f"**Logged in as:** {st.session_state['username']}")
        st.markdown(f"**Name:** {st.session_state['name']}")
        if st.button("🚪 Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['name'] = ""
            st.experimental_rerun()
########
#MAIN PAGE
########
st.title("🔐 Login Page")
st.markdown("Please log in to access the Budget Manager application.")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    user = login_user(username, password)
    if user:
        st.success(f"Welcome back, {user.name}!")
        st.session_state['logged_in'] = True
        st.session_state['username'] = user.username
        st.session_state['name'] = user.name
        st.experimental_rerun()
    else:
        st.error("Invalid username or password. Please try again.")
if st.session_state.get('logged_in', True):
    st.success(f"Welcome back, {st.session_state['name']}!")
    st.markdown("---")
    st.markdown("### ✅ You are logged in.")
    if st.button("➡️ Go to Main App"):
        st.switch_page("ui/streamlit/main_app.py")

st.markdown("----")
st.subheader("Register New Account")
new_username = st.text_input("New Username", key="reg_user")
new_email = st.text_input("Email", key="reg_email")
new_name = st.text_input("Full Name", key="reg_name")
new_password = st.text_input("New Password", type="password", key="reg_pass")
st.markdown("**Password Requirements:**")
st.markdown("""
- At least 8 characters long
- Contains both uppercase and lowercase letters
- Includes at least one number
- Has at least one special character (e.g., !@#$%^&*)
""")
    
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
if st.button("Register"):
    if not agree:
        st.error("You must agree to the Terms and Conditions to register.")
    else:
        try:
            register_user(new_username, new_password, new_email, new_name)
            st.success("Registration successful! You can now log in.")
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            st.error("An error occurred during registration. Please try again later.")
st.markdown("----")
st.subheader("Delete Account")
del_username = st.text_input("Username to Delete", key="del_user")
del_password = st.text_input("Password", type="password", key="del_pass")
if st.button("Delete Account"):
    try:
        user = login_user(del_username, del_password)
        if user:
            delete_user(del_username)
            st.success("Account deleted successfully.")
            if 'logged_in' in st.session_state and st.session_state['username'] == del_username:
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.session_state['name'] = ""
                st.experimental_rerun()
        else:
            st.error("Invalid username or password. Cannot delete account.")
    except Exception as e:
        st.error("An error occurred while deleting the account. Please try again later.")