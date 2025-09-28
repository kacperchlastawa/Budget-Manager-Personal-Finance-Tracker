from models.transaction import  Income, Expense
from models.budget import Budget
import json 

budget = Budget()
budget.load_data('transactions.json')

def add_income():
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")
    income = Income(amount, date, category, description)
    budget.add_transaction(income)
    budget.save_data('transactions.json')
    print("Income added successfully.")
def add_expense():
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")
    expense = Expense(amount, date, category, description)
    budget.add_transaction(expense)
    budget.save_data('transactions.json')
    print("Expense added successfully.")
def show_transactions():
    if not budget.get_transactions():
        print("No transactions found.")
        return
    for transaction in budget.get_transactions():
        print(transaction)
    
def get_balance():
    balance = budget.get_balance()
    print(f"Current balance: {balance}")

def filtered_by_category():
    category = input("Enter category to filter by: ")
    filtered = budget.filter_by_category(category)
    if not filtered:
        print(f"No transactions found in category '{category}'.")
        return
    for transaction in filtered:
        print(transaction)
def total_by_type():
    transaction_type = input("Enter transaction type (income/expense): ").strip().lower()
    if transaction_type == 'income':
        total = budget.total_by_type(Income)
    else:
        total = budget.total_by_type(Expense)
    print(f"Total {transaction_type}: {total}")

def menu():

    while True:
        print("\n--- Budget Manager ---")
        print("1. Add income")
        print("2. Add expense ")
        print("3. Show all transactions")
        print("4. Show balance")
        print("5. Filter by category")
        print("6. Total by type (income/expense)")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_income()
        elif choice == '2':
            add_expense()
        elif choice == '3':
            show_transactions()
        elif choice == '4':
            get_balance()
        elif choice == '5':
            filtered_by_category()
        elif choice == '6':
            total_by_type()
        elif choice == '7':
            budget.save_data('transactions.json')
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

