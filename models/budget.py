from .transaction import Income, Expense, Transaction
class Budget:

    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, transaction):
        if isinstance(transaction, Expense):
            if transaction.amount > self.get_balance():
                print("Not enough balance for this expense.")
                return False
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
    
    def to_dict(self):
        return [t.to_dict() for t in self.transactions]
    
    def from_dict(self, data):
        self.transactions = []
        for item in data:
            if item['type'] == 'income':
                transaction = Income(
                    item['amount'],
                    item['date'],
                    item['category'],
                    item['description']
                )
            elif item['type'] == 'expense':
                transaction = Expense(
                    item['amount'],
                    item['date'],
                    item['category'],
                    item['description']
                )
            self.transactions.append(transaction)