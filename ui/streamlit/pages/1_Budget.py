import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from models.budget import Budget
from services.data_analyzer import get_monthly_summary
from datetime import datetime
from models.transaction import Income, Expense
import pandas as pd
from ui.streamlit.helpers import style_dataframe
from data.budget_db import get_categories
budget = Budget()

st.set_page_config(
    page_title= "Section - Budget",
    page_icon="💰",
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
st.sidebar.write(f"Data:{today.strftime('%Y-%m-%d %H:%M')}")

#2
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

st.title("💰Budget Section")
st.markdown("This section allows you to manage your incomes and expenses.")

form_values ={
    "type":None,
    "amount" : None,
    "date": None,
    "category": None,
    "description": None
}
st.header("Add Income/Expense form ")
with st.form(key = 'add_income_expense_form'):
    form_values["type"] = st.selectbox("Select type of transaction", options = ["Income","Expense"])
    form_values["amount"] = st.number_input("Enter amount", min_value=0.01, step=0.01, format="%.2f")
    form_values["date"] = st.date_input("Select date", max_value=datetime.today())
    #Categories
    existing_categories = get_categories()
    selected_category = st.selectbox("Select category", options = existing_categories + ["Add new category"])
    if selected_category == "Add new category":
        new_category = st.text_input("Enter new category name").strip()
        if new_category:
            form_values["category"] = new_category.capitalize()
    else:
        form_values["category"] = selected_category
    form_values["description"] = st.text_area("Enter description")
    submitted = st.form_submit_button("Add Transaction", on_click=None)
    if submitted:
        if form_values["amount"] <= 0:
            st.error("Amount must be greater than 0.")
        elif not form_values["category"]:
            st.error("Category cannot be empty.")
        elif not form_values["date"]:
            st.error("Date cannot be empty.")
        else:
            if form_values["type"] == "Income":
                income = Income(
                    amount=form_values["amount"],
                    t_date=form_values["date"].strftime("%Y-%m-%d"),
                    category=form_values["category"],
                    description=form_values["description"]
                )
                budget.add_transaction(income)
                st.toast("✅ Income added successfully!", icon="💰")
                st.rerun()
            else:
                expense = Expense(
                    amount=form_values["amount"],
                    t_date=form_values["date"].strftime("%Y-%m-%d"),
                    category=form_values["category"],
                    description=form_values["description"]
                )
                budget.add_transaction(expense)
                st.toast("✅ Expense added successfully!", icon="💰")
                st.rerun()
st.divider()
#========================
#SHOW TRANSACTIONS
#========================
tab1, tab2, tab3 = st.tabs(["All Transactions", "Filter by Category", "Filter by Type"])
with tab1:
    st.header("All Transactions")
    st.slider("Number of transactions to display", min_value=1, max_value=100, value=10, step=1, key="num_transactions")
    st.selectbox("From beginning or the end", options = ["From beginning","From the end"], key ="from_beginning_or_end")
    transaction_button = st.button("Show Transactions")
    if transaction_button:
        transactions = budget.get_transactions()
        if not transactions:
            st.info("No transactions found.")
        else:
            num_to_display = st.session_state.num_transactions
            if st.session_state.from_beginning_or_end == "From beginning":
                df = pd.DataFrame([t.__dict__ for t in transactions[:num_to_display]])
                st.table(style_dataframe(df))
            else:
                df = pd.DataFrame([t.__dict__ for t in transactions[-num_to_display:]])
                st.table(style_dataframe(df))

#========================
#FILTER BY CATEGORY
#========================
with tab2:
    st.header("Filter Transactions by Category")
    existing_categories = get_categories()
    category_input = st.selectbox("Select category to filter", options = existing_categories)
    filter_button = st.button("Filter by Category")
    if filter_button:
        if not category_input:
            st.error("Category cannot be empty.")
        else:
            filtered = budget.filter_by_category(category_input)
            if not filtered:
                st.info(f"No transactions found in category '{category_input}'.")
            else:
                df = pd.DataFrame([t.__dict__ for t in filtered])
                st.table(style_dataframe(df))

#========================
#TRANSACTIONS BY TYPE
#========================
with tab3:
    st.header("Filter Transactions by Type")
    st.slider("Number of transactions to display", min_value=1, max_value=100, value=10, step=1, key="type_num_transactions")
    st.selectbox("From beginning or the end", options = ["From beginning","From the end"], key ="from_beginning_end")
    type_input = st.selectbox("Select transaction type", options = ["Income","Expense"])
    type_button = st.button("Filter by Transaction Type")
    if type_button:
        transaction_type = type_input.lower()
        filtered = budget.transactions_by_type(transaction_type)
        if not filtered:
            st.info(f"No transactions found of type '{transaction_type}'.")
        else:                       
            num_to_display = st.session_state.type_num_transactions
            if st.session_state.from_beginning_end == "From beginning":
                df = pd.DataFrame([t.__dict__ for t in filtered[:num_to_display]])
                st.table(style_dataframe(df))
            else:
                df = pd.DataFrame([t.__dict__ for t in filtered[-num_to_display:]])
                st.table(style_dataframe(df))

#========================
#TOTAL BY TYPE
#========================
st.divider()
st.header("Total Amount by Transaction Type")
total_type_input = st.selectbox("Select transaction type for total", options = ["Income","Expense"], key="total_type_input")
total_button = st.button("Show Total by Transaction Type")
if total_button:
    transaction_type = st.session_state.total_type_input.lower()
    total = budget.total_by_type(transaction_type)
    st.markdown(f"#### Total {transaction_type}: {total:.2f} zł")