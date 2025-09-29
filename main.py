from models.transaction import  Income, Expense
from models.budget import Budget
from models.savings import Savings, SavingGoal
import json 
from datetime import date
from ui.console import *

budget = Budget()
budget.load_data('transactions.json')
savings = Savings()
savings.load_from_file('savings.json')

menu(budget, savings)

