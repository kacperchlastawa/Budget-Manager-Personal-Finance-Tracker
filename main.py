from models.budget import Budget
from models.savings import Savings
from ui.console import *
from data.storage import save_to_file, load_from_file

budget = load_from_file(Budget, 'transactions.json')
savings = load_from_file(Savings,'savings.json')

menu(budget, savings)

