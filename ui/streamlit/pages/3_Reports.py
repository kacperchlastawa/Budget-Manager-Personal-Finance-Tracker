import streamlit as st
from models.budget import Budget
from services.report import Report
from services.data_analyzer import *
from datetime import datetime
from services.visualization import *
import pandas as pd
from reportlab.lib.pagesizes import A4
from calendar import month_name
from ui.streamlit.build_raport import build_raport
today = datetime.today()
st.set_page_config(
    page_title= "Section - Reports",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
if "budget" not in st.session_state:
    st.session_state.budget = Budget()


budget = st.session_state.budget

#===============
#SIDEBAR
#========
st.sidebar.title("Panel informacji")

#1
today = datetime.today()
st.sidebar.write(f"Data:{today.strftime('%Y-%m-%d')}")

#2
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
st.title("Report section📈")
st.markdown("This section allows you to generate raport to summarize your last budget actions.")

st.header("Generate Report")
st.markdown("You can generate a PDF report summarizing your budget activities for a specific month. Select the desired month and year, then click the 'Generate Report' button. The report will include a summary of your income, expenses, and balance for the selected period.")


with st.form(key = "report_form"):
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Year", min_value=2000, max_value=today.year, value=today.year, step=1)
    with col2:
        month_names = list(month_name)[1:]
        selected_month = st.selectbox(
        "Month",
        options=month_names,
        index=today.month - 1,
        format_func=lambda x: x
    )
        month = month_names.index(selected_month) + 1
    generate_button = st.form_submit_button("Generate Report")
if generate_button:
    try:    
        build_raport(filename= "monthly_report.pdf", month=month, year=year)
        with open("monthly_report.pdf", "rb") as file:
            btn = st.download_button(
                label="Download Report",
                data=file,
                file_name=f"budget_report_{year}_{month}.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Failed to generate report: {e}")     

st.divider()
st.header("Export Report to Email")
st.markdown("You can send the generated report directly to your email. Enter your email address below and click 'Send Report'. Make sure to check your inbox for the report attachment.")
email = st.text_input("Email Address", placeholder="@example.com")
email_button = st.button("Send Report")
if email_button:
    if not email or "@" not in email:
        st.error("Please enter a valid email address.")
    else:
        try:
            report = build_raport(filename= "monthly_report.pdf", month=month, year=year)
            report.export_to_email(email)
            st.toast(f"Report sent to {email} successfully!", icon="✅")
        except Exception as e:
            st.error(f"Failed to send report: {e}")


