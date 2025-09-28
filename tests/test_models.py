import unittest
from models.transaction import Income, Expense


class TestTransactions(unittest.TestCase):

    def test_income_creation(self):
        income = Income(1000, "2025-01-01", "Salary", "Monthly payment")
        self.assertEqual(income.amount, 1000)
        self.assertEqual(income.date, "2025-01-01")
        self.assertEqual(income.category, "Salary")
        self.assertEqual(income.description, "Monthly payment")
        self.assertEqual(income.to_dict()["type"], "income")

    def test_expense_creation(self):
        expense = Expense(200, "2025-01-02", "Food", "Groceries")
        self.assertEqual(expense.amount, 200)
        self.assertEqual(expense.date, "2025-01-02")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Groceries")
        self.assertEqual(expense.to_dict()["type"], "expense")

    def test_income_vs_expense(self):
        income = Income(500, "2025-01-03", "Bonus", "Project bonus")
        expense = Expense(300, "2025-01-04", "Transport", "Bus tickets")
        self.assertNotEqual(income.to_dict()["type"], expense.to_dict()["type"])


if __name__ == "__main__":
    unittest.main()
