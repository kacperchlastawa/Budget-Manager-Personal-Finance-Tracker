from transaction import Income, Expense, Transaction
import json
class Budget:

    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_balance(self):
        balance = 0 
        for transaction in self. transactions:
            if isinstance(transaction,Income):
                balance += transaction.amount
            elif isinstance(transaction,Expense):
                balance -= transaction.amount
        return balance
    def get_transactions(self):
        return self.transactions

    def get_income(self):
        incomes = []
        for transaction in self.transactions:
            if isinstance(transaction, Income):
                incomes.append(transaction)
        return incomes
    
    def get_expenses(self):
        expenses = []
        for transaction in self.transactions:
            if isinstance(transaction, Expense):
                expenses.append(transaction)
        return expenses
    
    def load_data(self, filename):
        try: 
            with open(filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    if item['type'] == 'income':
                        transaction = Income(item['amount'], item['date'], item['category'], item['description'])
                    elif item['type'] == 'expense':
                        transaction = Expense(item['amount'], item['date'], item['category'], item['description'])
                    self.transactions.append(transaction)
            print(f"Loaded {len(self.transactions)} transactions")
        except FileNotFoundError:
            print("No previous data found. Starting with an empty list.")

    def save_data(self, filename):
        with open(filename,'w', encoding = 'utf-8') as file:
            data = [transaction.to_dict() for transaction in self.transactions]
            json.dump(data, file, ensure_ascii=False, indent=4)    


    def filter_by_category(self, category):
        filtered = []
        for transaction in self.transactions:
            if transaction.category == category:
                filtered.append(transaction)
        return filtered
    
    def total_by_type(self, transaction_type):
        total = 0
        for transaction in self.transactions:
            if isinstance(transaction, transaction_type):
                total += transaction.amount
        return total