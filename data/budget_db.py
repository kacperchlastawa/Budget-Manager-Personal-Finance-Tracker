from .conection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Transactions' AND xtype='U')
        CREATE TABLE Transactions (
            id INT PRIMARY KEY IDENTITY(1,1),
            user_id INT NOT NULL UNIQUE,
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

def insert_transaction(obj, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Transactions (user_id,type,amount, date, category, description)
        VALUES (?,?, ?, ?, ?) WHERE user_id = ?
    """, (obj.type,obj.amount, obj.t_date, obj.category, obj.description, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions WHERE user_id = ? ORDER BY date", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_transaction_by_type(t_type, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions WHERE type = ? AND user_id = ? ORDER BY date", (t_type,user_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
               (i-e) as balance
        FROM ( 
           SELECT 
                ISNULL(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as i,
                ISNULL(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as e
           FROM Transactions WHERE user_id = ?
        ) t
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0


def filter_transactions_by_category(category, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions WHERE LOWER(category) = LOWER(?) AND user_id = ? ORDER BY date", (category,user_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def total_by_transaction_type(t_type, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT SUM(amount) FROM Transactions WHERE type = ? AND user_id = ?
                    """, (t_type, user_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0

def total_transaction_by_category(month, year, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT category, SUM(amount) totalAmount,Count(*) transactionCount FROM Transactions WHERE type = 'expense'
                    AND MONTH(date) = ?
                    AND YEAR(date) = ?
                    AND user_id = ?
                   GROUP BY category ORDER BY TotalAmount DESC
                   """, (month, year, user_id))
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows 

def balance_over_time(period, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    if period  == 'monthly':
        cursor.execute("""
                SELECT FORMAT(date,'yyyy-MM') as period,SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END ) as net_amount 
                       FROM Transactions WHERE user_id = ? GROUP BY FORMAT(date,'yyyy-MM')
                       ORDER BY period
            """, (user_id,))
    elif period == 'daily':
                cursor.execute("""
                SELECT date as period,SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END ) as net_amount 
                       FROM Transactions WHERE user_id = ? GROUP BY date
                       ORDER BY period
            """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
        
def income_vs_expense(limit,  user_id=None):
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute(f"""
                    SELECT TOP ({limit})
                    FORMAT(date,'yyyy-MM') period, 
                                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
                       FROM Transactions 
                       WHERE user_id = ?
                       GROUP BY FORMAT(date,'yyyy-MM')
                       ORDER BY period DESC
                       """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def month_summary(year,month, user_id):
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
            COUNT(*) AS total_transactions

        FROM Transactions
        WHERE YEAR(date) = ? AND MONTH(date) = ?
        AND user_id = ?
    """, (year, month, user_id))
    
     row = cursor.fetchone()
     cursor.close()
     conn.close()
     return row

def get_top_expenses_from_db(limit, year=None, month=None, user_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT TOP {limit}
               category, 
               SUM(amount) AS total_amount
        FROM Transactions
        WHERE type = 'expense'
        AND YEAR(date) = ?
        AND MONTH(date) = ?
        AND user_id = ?
        GROUP BY category
        ORDER BY total_amount DESC
    """, (year, month, user_id))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_categories(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT category FROM Transactions
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]

