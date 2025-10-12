import streamlit as st
from models.budget import Budget
from services.data_analyzer import get_monthly_summary
from datetime import datetime


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

#========================
#MAIN MENU
#========================

st.title("Budget section")
st.markdown("This section allows you to manage your incomes and expenses.")








