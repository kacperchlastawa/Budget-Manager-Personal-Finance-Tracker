import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=BudgetDB;'
        'UID=sa;'
        'PWD=Czarny12345!'        
    )
    return conn