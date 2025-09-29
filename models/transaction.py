class Transaction:
    def __init__(self, amount, t_date,category, description):
        self.amount = amount
        self.t_date = t_date
        self.description = description
        self.category = category

    def __str__(self):
        return f"Transaction(amount={self.amount}, date={self.t_date}, category={self.category}, description='{self.description}')"

    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.t_date,
            "category": self.category,
            "description": self.description
        }

class Income(Transaction):
    def __init__(self, amount, t_date, category, description):
        super().__init__(amount, t_date, category, description)
        self.type = "income"
    def __str__(self):
        return f"Income(amount={self.amount}, date={self.t_date}, category={self.category}, description='{self.description}')"
    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.type
        return data

class Expense(Transaction):
    def __init__(self, amount, t_date, category, description):
        super().__init__(amount, t_date, category, description)
        self.type = "expense"
    def __str__(self):
        return f"Expense(amount={self.amount}, date={self.t_date}, category={self.category}, description='{self.description}')"
    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.type
        return data