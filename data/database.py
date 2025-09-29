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

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 3+3")  # proste zapytanie testowe
    result = cursor.fetchone()
    print(result)
    if result:
        print("Połączenie działa!")
    cursor.close()
    conn.close()
except Exception as e:
    print("Błąd połączenia:", e)