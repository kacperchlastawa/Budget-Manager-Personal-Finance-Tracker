import pandas as pd
import streamlit as st
from models.budget import Budget
from models.savings import *
from services.data_analyzer import get_monthly_summary, get_savings_progress
from datetime import datetime
from models.transaction import Income, Expense
from services.visualization import plot_savings_progress
from ui.streamlit.pages.helpers import style_savings_goals

st.set_page_config(
    page_title= "Section - Savings",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)
savings = Savings()
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
st.sidebar.metric(label = "**Current balance** : ", value = f"{balance:.2f} zł")


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
st.title("Savings section💸")
st.markdown("This section allows you to manage your saving goals and save your money.")

tab1 , tab2 = st.tabs(["Add Saving Goal", "Remove Saving Goal"])

with tab1:
    st.header("Add Saving Goal")
    form_goal_values ={
        "name":None,
        "goal_amount" : None
    }
    with st.form(key = "saving_goal_form"):
        form_goal_values["name"] = st.text_input("Goal name")
        form_goal_values["goal_amount"] = st.number_input("Goal amount", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label="Add Goal")
        if submit_button:
            if not form_goal_values["name"]:
                st.warning("Please enter a goal name.")
            if form_goal_values["goal_amount"] <= 0:
                st.warning("Please enter a valid goal amount greater than zero.")
            try:
                savings.add_goal(form_goal_values["name"], form_goal_values["goal_amount"])
                st.toast(f"Goal '{form_goal_values['name']}' added successfully!", icon="✅")
            except ValueError as e:
                st.error(str(e))
with tab2:
    st.header("Remove Saving Goal")
    goal_name_to_remove = st.text_input("Enter the name of the goal to remove")
    remove_button = st.button("Remove Goal")
    if remove_button:
        if not goal_name_to_remove:
            st.warning("Please enter a goal name to remove.")
        else:
            goal = savings.get_goal(goal_name_to_remove)
            if goal:
                remaining = goal.amount
                if remaining > 0:
                    income = Income(
                        remaining,
                        date.today().isoformat(), 
                        "Savings return",
                        f"Funds returned from goal '{goal_name_to_remove}'"
                    )
                    budget.add_transaction(income)
                    st.write(f"Returned {remaining:.2f} to budget from goal '{goal_name_to_remove}'.")
                savings.remove_goal(goal_name_to_remove)
                st.toast(f"Goal '{goal_name_to_remove}' removed successfully!", icon="✅")
            else:
                st.error(f"Goal '{goal_name_to_remove}' not found.")

st.divider()
#========================
#SHOW SAVINGS GOALS
#========================
st.header("Your Saving Goals")
goals = st.button("SHOW GOALS")
if goals:
    saving_goals = savings.show_goals()
    if not saving_goals:
        st.info("No saving goals found. Please add a goal.")
    else:
        df = pd.DataFrame(saving_goals)
        styled_df = style_savings_goals(df)
        st.dataframe(styled_df, use_container_width=True)
st.divider()
#========================
#MANAGE SAVINGS GOALS
#========================
st.header("Manage Your Saving Goals")

tab1, tab2 = st.tabs(["Add Money to Goal", "Withdraw Money from Goal"])
with tab1:
    saving_goals = savings.show_goals()
    if not saving_goals:
        st.info("No saving goals found. Please add a goal.")
    form_goal_values = {
        "goal_name": None,
        "amount": None,
        "description": None,
        "date": None
    }
    st.subheader("Add Money to a Saving Goal")
    with st.form(key = "add money form"):
        form_goal_values["goal_name"] = st.selectbox("Select Goal", options = [goal["Goal Name"] for goal in saving_goals])
        form_goal_values["amount"] = st.number_input("Amount to add", min_value=0.01, step=0.01, format="%.2f")
        form_goal_values["description"] = st.text_area("Description")
        form_goal_values["date"] = st.date_input("Date", max_value=datetime.today())
        submit_button = st.form_submit_button(label="Add Money")
        if submit_button:
            if form_goal_values["amount"] <= 0:
                st.warning("Please enter a valid amount greater than zero.")
            elif budget.get_balance() < form_goal_values["amount"]:
                st.error("Not enough balance in the budget.")
            else:
                if form_goal_values["date"] is None:
                    st.warning("Please select a date.")
                else:
                    success = savings.add_to_goal(
                        form_goal_values["goal_name"],
                        form_goal_values["amount"],
                        form_goal_values["description"],
                        form_goal_values["date"].strftime("%Y-%m-%d")
                    )
                    if success:
                        expense = Expense(
                            form_goal_values["amount"],
                            form_goal_values["date"].strftime("%Y-%m-%d"),
                            f"Savings: {form_goal_values['goal_name']}",
                            form_goal_values["description"]
                        )
                        budget.add_transaction(expense)
                        st.toast(f"Added {form_goal_values['amount']:.2f} to goal '{form_goal_values['goal_name']}' successfully!", icon="✅")
                        st.rerun()
                    else:
                        st.error("Failed to add money to the goal.")
with tab2:
    saving_goals = savings.show_goals()
    if not saving_goals:
        st.info("No saving goals found. Please add a goal.")
    form_goal_values = {
        "goal_name": None,
        "amount": None,
        "description": None,
        "date": None
    }
    st.subheader("Withdraw Money from a Saving Goal")
    with st.form(key = "withdraw money form"):
        form_goal_values["goal_name"] = st.selectbox("Select Goal", options = [goal["Goal Name"] for goal in saving_goals])
        form_goal_values["amount"] = st.number_input("Amount to withdraw", min_value=0.01, step=0.01, format="%.2f")
        form_goal_values["description"] = st.text_area("Description")
        form_goal_values["date"] = st.date_input("Date", max_value=datetime.today())
        submit_button = st.form_submit_button(label="Withdraw Money")
        if submit_button:
            if form_goal_values["amount"] <= 0:
                st.warning("Please enter a valid amount greater than zero.")
            else:
                if form_goal_values["date"] is None:
                    st.warning("Please select a date.")
                else:
                    success = savings.withdraw_from_goal(
                        form_goal_values["goal_name"],
                        form_goal_values["amount"],
                        form_goal_values["description"],
                        form_goal_values["date"].strftime("%Y-%m-%d")
                    )
                    if success:
                        income = Income(
                            form_goal_values["amount"],
                            form_goal_values["date"].strftime("%Y-%m-%d"),
                            f"Savings: {form_goal_values['goal_name']}",
                            form_goal_values["description"]
                        )
                        budget.add_transaction(income)
                        st.toast(f"Withdrew {form_goal_values['amount']:.2f} from goal '{form_goal_values['goal_name']}' successfully!", icon="✅")
                        st.rerun()
                    else:
                        st.error("Failed to withdraw money from the goal.")

#=======================
#Show goal progress
#=======================
st.divider()
st.header("Check Saving Goal Progress")
check_progress = st.button("SHOW PROGRESS")
if check_progress:
    fig = plot_savings_progress(get_savings_progress())
    st.pyplot(fig)
