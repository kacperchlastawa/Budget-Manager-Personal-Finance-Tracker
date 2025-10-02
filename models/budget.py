from .transaction import Income, Expense, Transaction
from data.budget_db import *
class Budget:

    def __init__(self):
        pass
    
    def add_transaction(self, transaction):
        if isinstance(transaction, Expense):
            if transaction.amount > self.get_balance():
                print("Not enough balance for this expense.")
                return False
        insert_transaction(transaction)

    def get_balance(self):
        balance = get_balance()
        return balance
    
    def get_transactions(self):
        self.transactions = []
        rows = get_transactions()
        for row in rows:
            _,t_type, amount, date, category, description = row 
            if t_type == 'income':
                transaction = Income(amount, date, category, description)
            elif t_type == 'expense':
                transaction = Expense(amount, date, category, description)
            self.transactions.append(transaction)
        return self.transactions
    

    def filter_by_category(self, category):
        filtered = []
        filtered = filter_transactions_by_category(category)
        transactions = []
        for row in filtered:
            _,t_type, amount, date, category, description = row 
            if t_type == 'income':
                transaction = Income(amount, date, category, description)
            elif t_type == 'expense':
                transaction = Expense(amount, date, category, description)
            transactions.append(transaction)
        return transactions
    
    def total_by_type(self, transaction_type):
        total = 0
        if transaction_type.type == 'income':
            t_type = 'income'
        
        elif transaction_type.type == 'expense':
            t_type = 'expense'
        total = get_transaction_by_type(t_type)
        return total
    
