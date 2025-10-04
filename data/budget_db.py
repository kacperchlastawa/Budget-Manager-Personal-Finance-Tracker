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