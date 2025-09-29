from models.transaction import  Income, Expense
from models.budget import Budget
from models.savings import Savings, SavingGoal
from data.storage import save_to_file, load_from_file
from datetime import date


#Budget
#########################################################
def add_income(budget):
    amount = float(input("Enter amount: "))
    if amount <= 0:
        print("Amount must be greater than 0.")
        return
    t_date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    description = input("Enter description: ")
    income = Income(amount, t_date, category, description)
    budget.add_transaction(income)
    save_to_file(budget,'transactions.json')

def add_expense(budget):
    amount = float(input("Enter amount: "))
    t_date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    if not category:
        print("Category cannot be empty.")
        return
    description = input("Enter description: ")
    expense = Expense(amount, t_date, category, description)
    budget.add_transaction(expense)
    save_to_file(budget, 'transactions.json')

def show_transactions(budget):
    if not budget.get_transactions():
        print("No transactions found.")
        return
    for transaction in budget.get_transactions():
        print(transaction)
    
def get_balance(budget):
    balance = budget.get_balance()
    print(f"Current balance: {balance}")

def filtered_by_category(budget):
    category = input("Enter category to filter by: ").lower()
    filtered = budget.filter_by_category(category)
    if not filtered:
        print(f"No transactions found in category '{category}'.")
        return
    for transaction in filtered:
        print(transaction)
def total_by_type(budget):
    transaction_type = input("Enter transaction type (income/expense): ").strip().lower()
    if transaction_type == 'income':
        total = budget.total_by_type(Income)
    elif transaction_type == 'expense':
        total = budget.total_by_type(Expense)
    else:
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
        return
    print(f"Total {transaction_type}: {total}")
###################
#Savings
###################
def add_savings_goal(savings):
    goal_name = input("Enter goal name: ")
    goal_amount = float(input("Enter goal amount: "))
    if goal_amount <= 0:
        print("Goal amount must be greater than 0.")
        return
    savings.add_goal(goal_name, goal_amount)
    save_to_file(savings,'savings.json')
    print("Savings goal added successfully.")

def add_money_to_goal(savings, budget):
    goal_name = input("Enter goal name: ")
    amount = float(input("Enter amount to add: "))
    description = input("Enter description: ")
    if budget.get_balance() < amount:
            print("Not enough balance in the budget")
            return False
    if savings.add_to_goal(goal_name, amount, description):
        save_to_file(savings,'savings.json')
        print("Money added to goal successfully.")
        expense = Expense(amount, date.today().isoformat(), f"Savings: {goal_name}", description)
        budget.add_transaction(expense)
        save_to_file(budget, 'transactions.json')
    else:
        print("Failed to add money to goal.")

def withdraw_money_from_goal(savings, budget):
    goal_name = input("Enter goal name: ")
    amount = float(input("Enter amount to withdraw: "))
    description = input("Enter description: ")
    if savings.withdraw_from_goal(goal_name, amount, description):
        save_to_file(savings,'savings.json')
        print("Money withdrawn from goal successfully.")
        income = Income(amount, date.today().isoformat(), f"Savings: {goal_name}", description)
        budget.add_transaction(income)
        save_to_file(budget,'transactions.json')
    else:
        print("Failed to withdraw money from goal.")

def show_savings_goals(savings):
    if not savings.goals:
        print("No savings goals found.")
        return
    savings.show_goals()

def show_goal_progress(savings):
    goal_name = input("Enter goal name: ")
    goal = savings.get_goal(goal_name)
    if goal:
        progress = (goal.amount / goal.goal_amount) * 100 if goal.goal_amount > 0 else 0
        print(f"Progress for '{goal.name}': {goal.amount}/{goal.goal_amount} ({progress:.2f}%)")
    else:
        print("Goal not found.")

def remove_goal(savings, budget):
    goal_name = input("Enter goal name to remove: ")
    goal = savings.get_goal(goal_name)
    if goal:
        remaining = goal.get_balance()
        if remaining > 0:
            income = Income(
                remaining,
                date.today().isoformat(), 
                "Savings return",
                f"Funds returned from goal '{goal_name}'"
            )
            budget.add_transaction(income)
            save_to_file(budget, 'transactions.json')
            print(f"Returned {remaining} from '{goal_name}' back to budget.")
        if savings.remove_goal(goal_name):
            save_to_file(savings, 'savings.json')
            print("Goal removed successfully.")
    else:
        print("Goal not found.")

#Main Menu        
def menu(budget, savings):

    while True:
        print("\n--- Budget Manager ---")
        print("1. Add income")
        print("2. Add expense ")
        print("3. Show all transactions")
        print("4. Show balance")
        print("5. Filter by category")
        print("6.Total by type (income/expense)\n")
        print("---- Savings Menu ----")
        print("7. Add savings goal")
        print("8. Add money to goal")
        print("9. Withdraw money from goal")
        print("10. Show savings goals")
        print("11. Show progress of a goal")
        print("12. Remove a goal")
        print("------------------------")
        print("13. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_income(budget)
        elif choice == '2':
            add_expense(budget)
        elif choice == '3':
            show_transactions(budget)
        elif choice == '4':
            get_balance(budget)
        elif choice == '5':
            filtered_by_category(budget)
        elif choice == '6':
            total_by_type(budget)
        elif choice == '7':
            add_savings_goal(savings)
        elif choice == '8':
            add_money_to_goal(savings, budget)
        elif choice == '9':
            withdraw_money_from_goal(savings, budget)
        elif choice == '10':
            show_savings_goals(savings)
        elif choice == '11':
            show_goal_progress(savings)
        elif choice == '12':
            remove_goal(savings, budget)
        elif choice == '13':
            save_to_file(budget, 'transactions.json')
            save_to_file(savings,'savings.json')
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")