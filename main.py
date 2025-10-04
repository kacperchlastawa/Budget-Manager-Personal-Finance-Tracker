from models.budget import Budget
from models.savings import Savings
from data.budget_db import create_tables
from data.savings_db import create_tables as create_savings_tables
from models.transaction import Income, Expense
from ui.console import *

# create_tables()
# create_savings_tables()
# print("Database tables created successfully!")

from ui.console import *

budget = Budget()
savings = Savings()
menu(budget, savings)
# income = Income(2000, "2025-10-01", "Job", "Salary")
# budget.add_transaction(income)

# expense = Expense(300, "2025-10-02", "Food", "Groceries")
# budget.add_transaction(expense)

# print("Transactions:")

# print("Balance:", budget.get_balance())



# from models.savings import Savings

# savings = Savings()

# # Dodaj cel
# savings.add_goal("Holiday", 3000)

# # Dodaj środki do celu
# savings.add_to_goal("Holiday", 200, "First deposit", "2025-10-03")

# print("Balance:", budget.get_balance())

# # Sprawdź cel
# savings.show_goals()

# # # Wypłać część środków
# savings.withdraw_from_goal("Holiday", 50, "Withdraw for dinner")

# # # Usuń cel
# # savings.remove_goal("New Laptop")


# print("Balance:", budget.get_balance())


