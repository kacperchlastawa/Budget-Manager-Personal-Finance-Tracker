import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))) # - bez tego nie widzi mi modułów

import streamlit as st
from models.budget import Budget
from models.savings import *
from services.report import Report
from models.transaction import *
from services.data_analyzer import get_monthly_summary
from datetime import datetime

st.set_page_config(
    page_title= "Budget Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("💰Budget Manager")
st.subheader("Manage your budget, savings and get your account raport")
st.markdown("----")

#===============
#SIDEBAR
#========
st.sidebar.title("Panel informacji")

#1
today = datetime.today()
st.sidebar.write(f"Data:{today.strftime('%Y-%m-%d')}")

#2
budget = Budget()
try:
    balance = budget.get_balance()
except Exception:
    balance = 0.0
st.sidebar.metric(label = "Current balance : ", value = f"{balance:.2f} zł")


#3 
try:
    summary = get_monthly_summary(today.year, today.month)
    if summary:
        st.sidebar.markdown("### Month Summary")
        st.sidebar.write(f"**Incomes:** {summary['total_income']:.2f} zł")
        st.sidebar.write(f"**Expenses:** {summary['total_exp']:.2f} zł")
        st.sidebar.write(f"**Balance:** {summary['balance']:.2f} zł")
    else:
        st.sidebar.info("No data to summary")
except Exception:
    st.sidebar.warning("Failed to download the data")


#=============
#MAIN MENU
#=============

st.markdown("### Choose section you want to manage")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("pages/1_Budget.py", label = "Budget", icon = "💰")
with col2:
    st.page_link("pages/2_Savings.py", label = "Savings", icon  = "💸")
with col3:
    st.page_link("pages/3_Reports.py", label = "Report", icon = "📈")
with col4:
    st.page_link("pages/4_About.py", label = "About", icon = "📘")


#Footer

st.markdown("---")
st.caption("© 2025 Budget Manager | Powered by Streamlit & Python")



