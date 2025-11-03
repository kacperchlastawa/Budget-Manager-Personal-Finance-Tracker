import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))) # - bez tego nie widzi mi modułów

import streamlit as st
from models.budget import Budget
from models.savings import *
from services.report import Report
from models.transaction import *
from services.data_analyzer import get_monthly_summary
from datetime import datetime
from data.user_db import login_user

st.set_page_config(
    page_title= "Budget Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)
#########
#Safety
#########
if not st.session_state.get("logged_in", False):
    st.warning("You must be logged in to access this page.")
    st.stop()                                                                                                                                                                                                                       

st.title("💰Budget Manager")
st.subheader("Manage your budget, savings and get your account raport")
st.markdown("----")

#==============
#Functions
#==============

@st.cache_data
def load_balance():
    try:
        budget = Budget()
        return budget.get_balance()
    except Exception:
        return 0.0
def load_summary(year, month):
    try:
        summary = get_monthly_summary(year, month)
        return summary
    except Exception:
        return None
    
#SIDEBAR
#========
with st.sidebar:
    st.title(f"Hello, {st.session_state.get('name', 'User')}!")
    st.markdown("----")

    st.sidebar.title("Panel informacji")

    #1
    today = datetime.today()
    st.write(f"Data:{today.strftime('%Y-%m-%d %H:%M')}")

    #2
    balance = load_balance()
    st.metric(label = "**Current balance** : ", value = f"{balance:.2f} zł")


    #3 
    try:
        summary = load_summary(today.year, today.month)
        if summary:
            st.markdown("### Month Summary")
            st.write(f"**Incomes:** {summary['total_income']:.2f} zł")
            st.write(f"**Expenses:** {summary['total_exp']:.2f} zł")
            st.write(f"**Balance:** {summary['balance']:.2f} zł")
        else:
            st.info("No data to summary")
    except Exception:
        st.warning("Failed to download the data")


    st.markdown("---")
    if st.button("🚪 Wyloguj"):
        st.session_state['logged_in'] = False
        st.rerun()
    
    st.markdown("----")
    if st.button("❌ Delete Account"):
        try:
            from data.user_db import delete_user
            delete_user(st.session_state['username'])
            st.success("Account deleted successfully.")
            st.session_state['logged_in'] = False
            st.rerun()
        except Exception as e:
            st.error(f"Failed to delete account: {str(e)}")
#=============
#MAIN MENU
#=============

st.markdown("### Choose section you want to manage")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_Budget.py", label = "Budget", icon = "💰")
with col2:
    st.page_link("pages/2_Savings.py", label = "Savings", icon  = "💸")
with col3:
    st.page_link("pages/3_Reports.py", label = "Report", icon = "📈")


#Footer

st.markdown("---")
st.caption("© 2025 Budget Manager | Powered by Streamlit & Python")



