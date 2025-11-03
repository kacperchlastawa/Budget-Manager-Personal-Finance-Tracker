from .conection import get_connection
from .budget_db import *  

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SavingGoals' AND xtype='U')
        CREATE TABLE SavingGoals (
            id INT PRIMARY KEY IDENTITY(1,1),
            user_id INT NOT NULL UNIQUE,
            name NVARCHAR(50) NOT NULL,
            amount FLOAT NOT NULL DEFAULT 0,
            goal_amount FLOAT NOT NULL

                   )
                """)
    cursor.execute("""
                   IF NOT EXISTS ( SELECT * FROM sysobjects WHERE name='SavingTransactions' AND xtype='U')
                   CREATE TABLE SavingTransactions(
                          id INT PRIMARY KEY IDENTITY(1,1),
                          user_id INT NOT NULL UNIQUE,
                          goal_id INT NOT NULL,
                          amount FLOAT NOT NULL,
                          date DATE NOT NULL,
                          description NVARCHAR(255),
                          FOREIGN KEY (goal_id) REFERENCES SavingGoals(id) ON DELETE CASCADE
                     )
                   """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_goal(goal, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO SavingGoals (name, amount, goal_amount)
            VALUES (?, ?, ?) WHERE user_id = ?
        """, (goal.name, goal.amount, goal.goal_amount, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_goal(goal_name, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SavingGoals WHERE name = ? AND user_id = ?", (goal_name,user_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_goals(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SavingGoals WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
def get_goal_by_name(goal_name, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SavingGoals WHERE name = ? AND user_id = ?", (goal_name,user_id))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def update_goal_amount(goal_name, new_amount, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE SavingGoals
        SET amount = ?
        WHERE name = ?
        AND user_id = ?
    """, (new_amount, goal_name,user_id))
    conn.commit()
    cursor.close()
    conn.close()

def insert_savings_transaction(goal_id,amount, t_date, description, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                INSERT INTO SavingTransactions(goal_id,amount,date,description)
                   VALUES(?,?,?,?) WHERE user_id = ?
                   """,(goal_id,amount,t_date,description, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_transactions(goal_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    DELETE FROM SavingTransactions WHERE goal_id = ? AND user_id = ?
                   """, (goal_id,user_id))
    conn.commit()
    cursor.close()
    conn.close()