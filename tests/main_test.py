import unittest
from unittest.mock import patch, mock_open
import json

from main import (
    add_income,
    add_expense,
    get_balance,
    show_transactions,
    save_data,
    load_data,
    transactions,
)
from models.transaction import Income, Expense


class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        transactions.clear()  

    @patch("builtins.input", side_effect=["1000", "2025-01-01", "Salary", "Monthly payment"])
    def test_add_income(self, mock_input):
        add_income()
        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], Income)
        self.assertEqual(transactions[0].amount, 1000)
        self.assertEqual(transactions[0].category, "Salary")

    @patch("builtins.input", side_effect=["200", "2025-01-02", "Food", "Groceries"])
    def test_add_expense(self, mock_input):
        add_expense()
        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], Expense)
        self.assertEqual(transactions[0].amount, 200)
        self.assertEqual(transactions[0].category, "Food")

    def test_get_balance(self):
        transactions.append(Income(1000, "2025-01-01", "Salary", "Monthly"))
        transactions.append(Expense(200, "2025-01-02", "Food", "Groceries"))
        with patch("builtins.print") as mock_print:
            get_balance()
            mock_print.assert_called_with("Current balance: 800")

    def test_show_transactions_empty(self):
        with patch("builtins.print") as mock_print:
            show_transactions()
            mock_print.assert_called_with("No transactions found.")

    def test_show_transactions_with_data(self):
        transactions.append(Income(500, "2025-01-01", "Gift", "Birthday"))
        with patch("builtins.print") as mock_print:
            show_transactions()
            mock_print.assert_called()  

    def test_save_and_load_data(self):
        transactions.append(Income(300, "2025-01-01", "Gift", "Present"))
        transactions.append(Expense(100, "2025-01-02", "Transport", "Bus"))

        with patch("builtins.open", mock_open()) as mocked_file:
            save_data()
            mocked_file.assert_called_with("transactions.json", "w", encoding="utf-8")
            handle = mocked_file()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            saved_json = json.loads(written_data)
            self.assertEqual(saved_json[0]["type"], "income")
            self.assertEqual(saved_json[1]["type"], "expense")

        json_content = json.dumps([
            {"type": "income", "amount": 200, "date": "2025-01-03", "category": "Bonus", "description": "Project"},
            {"type": "expense", "amount": 50, "date": "2025-01-04", "category": "Food", "description": "Snacks"}
        ])
        with patch("builtins.open", mock_open(read_data=json_content)):
            load_data()
            self.assertEqual(len(transactions), 4)  


if __name__ == "__main__":
    unittest.main()
