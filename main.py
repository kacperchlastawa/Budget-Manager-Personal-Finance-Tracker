from models.transaction import  Income, Expense
import json 

def add_income():
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")
    income = Income(amount, date, category, description)
    transactions.append(income)
    print("Income added successfully.")
def add_expense():
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")
    expense = Expense(amount, date, category, description)
    transactions.append(expense)
    print("Expense added successfully.")
def show_transactions():
    if not transactions:
        print("No transactions found.")
        return
    for transaction in transactions:
        print(transaction)
    
def get_balance():
    balance = 0
    for transaction in transactions:
        if isinstance(transaction, Income):
            balance += transaction.amount
        elif isinstance(transaction, Expense):
            balance -= transaction.amount
    print(f"Current balance: {balance}")

def load_data(filename = 'transactions.json'):
    try:
        with open('transactions.json', 'r') as file:
            data = json.load(file)
            for item in data:
                if item['type'] == 'income':
                    transaction = Income(item['amount'], item['date'], item['category'], item['description'])
                elif item['type'] == 'expense':
                    transaction = Expense(item['amount'], item['date'], item['category'], item['description'])
                transactions.append(transaction)
    except  FileNotFoundError:
        print("No previous data found. Starting with empty list.")
    
def save_data(filename = 'transactions.json'):
    with open('transactions.json', 'w',encoding="utf-8") as file:
        data = [transaction.to_dict() for transaction in transactions]
        json.dump(data, file,ensure_ascii=False, indent=4)

def menu():

    while True:
        print("\n--- Budget Manager ---")
        print("1. Add income")
        print("2. Add expense ")
        print("3. Show all transactions")
        print("4. Get balance")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_income()
            save_data()
        elif choice == '2':
            add_expense()
            save_data()
        elif choice == '3':
            show_transactions()
        elif choice == '4':
            get_balance()
        elif choice == '5':
            save_data()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

transactions = []
load_data(filename='transactions.json')
