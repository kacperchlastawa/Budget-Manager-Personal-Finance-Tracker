from .conection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Transactions' AND xtype='U')
        CREATE TABLE Transactions (
            id INT PRIMARY KEY IDENTITY(1,1),
            type NVARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
            amount FLOAT NOT NULL,
            date DATE NOT NULL,
            category NVARCHAR(100) NOT NULL,
            description NVARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_transaction(obj):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Transactions (type,amount, date, category, description)
        VALUES (?,?, ?, ?, ?)
    """, (obj.type,obj.amount, obj.t_date, obj.category, obj.description))
    conn.commit()
    cursor.close()
    conn.close()

def get_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_transaction_by_type(t_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions WHERE type = ?", (t_type,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_balance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
               (i-e) as balance
        FROM ( 
           SELECT 
                ISNULL(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as i,
                ISNULL(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as e
           FROM Transactions
        ) t
    """)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0


def filter_transactions_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions WHERE LOWER(category) = ?", (category,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def total_by_transaction_type(t_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT SUM(amount) FROM Transactions WHERE type = ?
                   """, (t_type))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

def total_transaction_by_category():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT category, SUM(amount) totalAmount,Count(*) transactionCount FROM Transactions WHERE type = 'expense'
                   GROUP BY category ORDER BY TotalAmount DESC
                   """)
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows 

def balance_over_time(period):
    conn = get_connection()
    cursor = conn.cursor()
    if period  == 'monthly':
        cursor.execute("""
                SELECT FORMAT(date,'yyyy-MM') as period,SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END ) as net_amount 
                       FROM Transactions GROUP BY FORMAT(date,'yyyy-MM')
                       ORDER BY period
            """)
    elif period == 'daily':
                cursor.execute("""
                SELECT date as period,SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END ) as net_amount 
                       FROM Transactions GROUP BY date
                       ORDER BY period
            """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
        
def income_vs_expense(limit):
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute("""
                    SELECT TOP ?
                    FORMAT(date,'yyyy-MM') period, 
                                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
                       FROM Transactions GROUP BY FORMAT(date,'yyyy-MM')
                       ORDER BY period DESC

                       """, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def month_summary(year,month):
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
            AVG(CASE WHEN type = 'income' THEN amount END) AS avg_income,
            MAX(CASE WHEN type = 'income' THEN amount END) AS max_income,
            MIN(CASE WHEN type = 'income' THEN amount END) AS min_income,
            COUNT(CASE WHEN type = 'income' THEN 1 END) AS income_count,
            
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense,
            AVG(CASE WHEN type = 'expense' THEN amount END) AS avg_expense,
            MAX(CASE WHEN type = 'expense' THEN amount END) AS max_expense,
            MIN(CASE WHEN type = 'expense' THEN amount END) AS min_expense,
            COUNT(CASE WHEN type = 'expense' THEN 1 END) AS expense_count,
            
        FROM Transactions
        WHERE YEAR(date) = ? AND MONTH(date) = ?
    """, (year, month))
    
     row = cursor.fetchone()
     cursor.close()
     conn.close()
     return row