from .conection import get_connection
from .budget_db import *  

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SavingGoals' AND xtype='U')
        CREATE TABLE SavingGoals (
            id INT PRIMARY KEY IDENTITY(1,1),
            name NVARCHAR(50) NOT NULL,
            amount FLOAT NOT NULL DEFAULT 0,
            goal_amount FLOAT NOT NULL

                   )
                """)
    cursor.execute("""
                   IF NOT EXISTS ( SELECT * FROM sysobjects WHERE name='SavingTransactions' AND xtype='U')
                   CREATE TABLE SavingTransactions(
                          id INT PRIMARY KEY IDENTITY(1,1),
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

def insert_goal(goal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO SavingGoals (name, amount, goal_amount)
            VALUES (?, ?, ?)
        """, (goal.name, goal.amount, goal.goal_amount))
    conn.commit()
    cursor.close()
    conn.close()

def delete_goal(goal_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SavingGoals WHERE name = ?", (goal_name,))
    conn.commit()
    cursor.close()
    conn.close()

def get_goals():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SavingGoals")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
def get_goal_by_name(goal_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SavingGoals WHERE name = ?", (goal_name,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def update_goal_amount(goal_name, new_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE SavingGoals
        SET amount = ?
        WHERE name = ?
    """, (new_amount, goal_name))
    conn.commit()
    cursor.close()
    conn.close()

def insert_transaction(goal_id,amount, t_date, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                INSERT INTO SavingTransactions(goal_id,amount,date,description)
                   VALUES(?,?,?,?)
                   """,(goal_id,amount,t_date,description))
    conn.commit()
    cursor.close()
    conn.close()