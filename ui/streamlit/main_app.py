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

with st.sidebar:
    st.title("Budget Manager")
    st.markdown(f"**{datetime.today().strftime('%Y-%m-%d')}**")










