import json

class SavingGoal:
    def __init__(self, name: str, amount: float, goal_amount: float): 
        self.amount = amount
        self.name = name
        self.goal_amount = goal_amount
        self.transactions = []
    def __repr__(self):
        progress = (self.amount / self.goal_amount * 100) if self.goal_amount else 0
        return (f"SavingGoal(name='{self.name}', amount={self.amount}, "f"goal_amount={self.goal_amount}, progress={progress:.2f}%)")

    def add(self, amount : float, description : str, date = None):
        self.transactions.append((amount, description, date))
        self.amount += amount
    
    def withdraw(self, amount : float, description : str, date = None):
        self.transactions.append((- amount, description, date))
        self.amount -= amount

    def get_balance(self):
        return self.amount
    
    def how_much_left(self):
        return self.goal_amount - self.amount

    def progress(self):
        return (self.amount / self.goal_amount * 100) if self.goal_amount else 0

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "goal_amount": self.goal_amount,
            "transactions": self.transactions
        }
    def from_dict(self, data):
        self.name = data["name"]
        self.amount = data["amount"]
        self.goal_amount = data["goal_amount"]
        self.transactions = data["transactions"]

#####

class Savings:
    def __init__(self):
        self.goals = []    
    
    def add_goal(self, goal_name:str, goal_amount:float):
        new_goal = SavingGoal(goal_name, 0, goal_amount)
        self.goals.append(new_goal)
    
    def remove_goal(self, goal_name : str):
        for goal in self.goals:
            if goal.name == goal_name:
                self.goals.remove(goal)
                return True
            
        print("Goal not found")
        return False
    
    def get_goal(self, goal_name : str):
        for goal in self.goals:
            if goal.name == goal_name:
                return goal
            
        print("Goal not found")
        return None
            
    def add_to_goal(self, goal_name : str, amount: float, description : str, date = None):
        goal = self.get_goal(goal_name)
        if goal:
            goal.add(amount, description, date)
            return True
        else:
            print("Goal not found")
            return False
        
    def withdraw_from_goal(self, goal_name : str, amount: float, description : str, date =  None):
        goal = self.get_goal(goal_name)
        if goal:
            goal.withdraw(amount, description, date)
            return True
        else:
            print("Goal not found")
            return False
        
    def show_goals(self):
        for goal in self.goals:
            print(goal) 

    def to_dict(self):
        return {
            "goals": [goal.to_dict() for goal in self.goals]
        }
    def from_dict(self,data):
        self.goals = []
        for goal_data in data.get("goals",[]):
            goal = SavingGoal(goal_data["name"], goal_data["amount"],goal_data["goal_amount"])
            goal.transactions = goal_data.get("transactions",[])
            self.goals.append(goal)
    
    def save_to_file(self, filename = 'savings.json'):
        with open(filename, 'w',encoding= "utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=4)

    def load_from_file(self, filename = 'savings.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.from_dict(data)
        except FileNotFoundError:
            print(f"No existing savings data found in {filename}. Starting with an empty list.")
            self.goals = []

    