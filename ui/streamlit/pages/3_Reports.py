import streamlit as st
from models.budget import Budget
from services.report import Report
from services.data_analyzer import *
from datetime import datetime
from services.visualization import *
import pandas as pd
from reportlab.lib.pagesizes import A4
from calendar import month_name

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
        report = Report(filename= "monthly_report.pdf", pagesize=A4)
        report.add_title(f"Budget report — {datetime(year, month, 1).strftime('%B %Y')}")
        report.add_timestamp()
        report.add_paragraph(f"This report shows financial summary of {datetime(year, month, 1).strftime('%B %Y')}, including expenses, incomes and users savings analysis.")
        report.add_title("Data visualisation")
        report.add_paragraph(" Charts below shows the most important personal budget indicators.")
        piechart_category = plot_transactions_by_category(get_transactions_by_category())

        report.add_figure(piechart_category, "Most common expenses", 280, 280)
        report.add_paragraph("The pie chart above illustrates the distribution of expenses across various categories, providing insights into spending habits.")

        balance_chart =balance_over_time(get_balance_over_time(period = 'daily'), period = 'daily')
        balance_chart_2 = balance_over_time(get_balance_over_time(period = 'monthly'), period = 'monthly')
        report.add_figure(balance_chart, "Change in balance - daily", 300, 300)
        report.add_paragraph("The line chart above depicts the daily changes in your account balance over time, highlighting trends and fluctuations.")
        report.add_figure(balance_chart_2, "Change in balance - monthly", 300, 300)
        report.add_paragraph("The line chart above illustrates the monthly changes in your account balance, providing a broader perspective on financial trends.")

        income_vs_expense_chart = plot_incomes_vs_expenses(get_income_vs_expense(limit=5))
        report.add_figure(income_vs_expense_chart, "Incomes and expenses comparison", 300, 300)
        report.add_paragraph("The bar chart above compares your monthly incomes and expenses, allowing you to visualize your financial balance.")

        top_expenses_chart = plot_top_n_expenses(get_top_expenses(limit=5))
        report.add_figure(top_expenses_chart, "Top 5 biggest expenses", 250, 250)
        report.add_paragraph("The horizontal bar chart above highlights your top 5 biggest expenses, helping you identify major spending areas.")

        chart_savings_progress = plot_savings_progress(get_savings_progress())
        report.add_figure(chart_savings_progress, "Saving progress", 300, 300)
        report.add_paragraph("The area chart above illustrates your savings progress over time, showcasing how your savings have accumulated.")

        summary = get_monthly_summary(year, month)
        summary_table = pd.DataFrame([summary])  
        summary2 = get_monthly_summary(year, month-1 if month > 1 else 12)
        summary_table2 = pd.DataFrame([summary2])
        report.add_title("Summary of the month")
        report.add_paragraph("The table below shows key financial statistics for the current month:")
        report.add_table(summary_table, f"Table. {datetime(year, month, 1).strftime('%B %Y')} - summary")
        report.add_paragraph("The table above provides a detailed summary of your financial statistics for the selected month, including total income, expenses, and balance.")
        if summary2 is not None:
            report.add_table(summary_table2, f"Table. {datetime(year, month-1 if month > 1 else 12, 1).strftime('%B %Y')} - summary")
            report.add_paragraph("The table above provides a detailed summary of your financial statistics for the previous month, allowing for comparison with the current month.")
        report.build()

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
            report.export_to_email(email)
            st.toast(f"Report sent to {email} successfully!", icon="✅")
        except Exception as e:
            st.error(f"Failed to send report: {e}")


