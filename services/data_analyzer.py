from data.savings_db import *
from data.budget_db import *
import pandas as pd

def get_transactions_by_category():
    rows = total_transaction_by_category()
    if not rows:
        return pd.DataFrame(columns=['category','TotalAmount','count'])
    
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
    pass
def get_top_expenses():
    pass
