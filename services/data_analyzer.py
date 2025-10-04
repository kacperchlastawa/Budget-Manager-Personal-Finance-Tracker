from data.savings_db import *
from data.budget_db import *
import pandas as pd

def get_transactions_by_category():
    rows = total_transaction_by_category()
    if not rows:
        return pd.DataFrame(columns=['category','total','count'])
    
    data = []
    for row in rows:
        data.append({
            'category':row[0],
            'total': float(row[1]),
            'count': int(row[2])
        })

    df = pd.DataFrame(data)
    return df
def get_balance_over_time(period = 'daily'):
    rows = balance_over_time(period)
    if not rows:
        return pd.DataFrame(columns=['period', 'balance'])

    data = []
    for row in rows:
        data.append({
            'period': row[0],
            'net_amount': float(row[1])
        })
    df = pd.DataFrame(data)
    df['balance'] = df['net_amount'].cumsum()
    return df
    
def get_income_vs_expense(limit = 6):
    rows = income_vs_expense(limit)
    if not rows:
        return pd.DataFrame(columns = ['period','income','expenses'])
    data = []
    for row in rows:
        data.append({
            'period': row[0],
            'income': row[1],
            'expenses': row[2]
        })
    df = pd.DataFrame(data)
    df['balance'] = df['income'] - df['expenses']
    return df
def get_monthly_summary(year,month):
    row = month_summary(year,month)
    if not row:
        return None
    return {
            'year': year,
            'month': month,
            'total_income': float(row[0]) if row[0] else 0,
            'avg_income': float(row[1]) if row[1] else 0,
            'max_income': float(row[2]) if row[2] else 0,
            'min_income': float(row[3]) if row[3] else 0,
            'income_count': int(row[4]) if row[4] else 0,
            'total_expense': float(row[5]) if row[5] else 0,
            'avg_expense': float(row[6]) if row[6] else 0,
            'max_expense': float(row[7]) if row[7] else 0,
            'min_expense': float(row[8]) if row[8] else 0,
            'expense_count': int(row[9]) if row[9] else 0,
            'total_transactions': int(row[10]) if row[10] else 0,
            'balance': (float(row[0]) if row[0] else 0) - (float(row[5]) if row[5] else 0)
        }

def get_savings_progress():
    rows = get_goals()
    progress_list = []
    if not rows:
        return pd.DataFrame(columns=['goal_name', 'amount', 'goal_amount', 'progress'])
    for row in rows :
        name = row[1]
        current = row[2]
        target = row[3]
        if target > 0:
            progress = round((current/target)*100,2)
        else:
            progress = 0.0

        progress_list.append({
            'goal_name': name,
            'current_amount': float(current),
            'goal_amount': float(target),
            'progress': progress
        })
    return pd.DataFrame(progress_list)

def get_top_expenses(limit = 5):
    expenses = get_top_expenses_from_db()
    top_expenses = []
    if not expenses:
        return pd.DataFrame(columns=['category', 'total_expense'])
    for row in expenses[:limit]:
        top_expenses.append({
            'category': row[0],
            'total_expense': float(row[1])
        })
    return pd.DataFrame(top_expenses)
