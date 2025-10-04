from .budget import Budget
from data.savings_db import *
from data.budget_db import *
from datetime import date
budget = Budget()
class SavingGoal:
    def __init__(self, name: str, amount: float, goal_amount: float): 
        self.amount = amount
        self.name = name
        self.goal_amount = goal_amount
    def __repr__(self):
        progress = (self.amount / self.goal_amount * 100) if self.goal_amount else 0
        return (f"SavingGoal(name='{self.name}', amount={self.amount}, "f"goal_amount={self.goal_amount}, progress={progress:.2f}%)")

    def add(self, amount : float, description : str, t_date = None):
        if t_date is None:
            t_date = date.today().isoformat()
        self.amount += amount
        update_goal_amount(self.name, self.amount)
        rows = get_goal_by_name(self.name)
        goal_id = rows[0]
        insert_savings_transaction(goal_id,+ amount, t_date, description)

            
        
    def withdraw(self, amount : float, description : str, t_date = None):
        if t_date is None:
            t_date = date.today().isoformat()
        self.amount -= amount
        update_goal_amount(self.name, self.amount)
        rows = get_goal_by_name(self.name)
        goal_id = rows[0]
        insert_savings_transaction(goal_id,- amount, t_date, description)

    def get_balance(self):
        return self.amount
    
    def how_much_left(self):
        return self.goal_amount - self.amount

    def progress(self):
        return (self.amount / self.goal_amount * 100) if self.goal_amount else 0

#####

class Savings:
    def __init__(self):
        pass

    def add_goal(self, goal_name:str, goal_amount:float):
        if goal_amount <= 0: 
            print("Goal amount must be greater than zero") 
            return
        new_goal = SavingGoal(goal_name, 0, goal_amount)
        insert_goal(new_goal)
        

    def remove_goal(self, goal_name : str):
        rows = get_goal_by_name(goal_name)
        goal_id = rows[0]
        delete_transactions(goal_id)
        delete_goal(goal_name)
        if get_goal_by_name(goal_name) is None:
            print(f"Goal '{goal_name}' removed successfully.")
            return True
        else:
            print(f"Failed to remove goal '{goal_name}'.")
            return False
    
    def get_goal(self, goal_name : str):
        goal = get_goal_by_name(goal_name)
        
        if goal:
            _, name, amount, goal_amount = goal
            goal = SavingGoal(name, amount, goal_amount)
            return goal
        else:
            print("Goal not found")
            return False
            
    def add_to_goal(self, goal_name : str, amount: float, description : str, t_date = None):
        goal_row = get_goal_by_name(goal_name)
        if goal_row:
            goal = SavingGoal(goal_row[1], goal_row[2], goal_row[3])
            goal.add(amount, description, t_date)
            return True
        else:
            print("Goal not found")
            return False
        
        
    def withdraw_from_goal(self, goal_name : str, amount: float, description : str, t_date =  None):
        goal_row = get_goal_by_name(goal_name)
        if goal_row:
            goal = SavingGoal(goal_row[1], goal_row[2], goal_row[3])
            if goal.amount < amount:
                print("Not enough balance in the goal")
                return False
            goal.withdraw(amount, description, t_date)
            return True
        else:
            print("Goal not found")
            return False
        
    def show_goals(self):
        goals = get_goals()
        if not goals:
            print("No savings goals found.")
            return
        for row in goals:
            _, name, amount, goal_amount = row
            goal = SavingGoal(name, amount, goal_amount)
            print(goal)

    