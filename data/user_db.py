from data.conection import get_connection
from models.user import User
def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(100) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        email NVARCHAR(255) NOT NULL UNIQUE,
        name NVARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    def register_user(username, password, email, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SeLECT * FROM Users WHERE username = ? OR email = ?
        """, (username, email))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise ValueError("Username or email already exists")
        user = User(username, password, email, name)
        cursor.execute("""
            INSERT INTO Users (username, password_hash, email, name)
            VALUES (?, ?, ?, ?)
        """, (user.username, user.password_hash, user.email, user.name))
        conn.commit()
        cursor.close()
        conn.close()
    
    def delete_user(username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
        conn.commit()
        cursor.close()
        conn.close()
    
    def login_user(username, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        user = User([row[0], row[1], row[2], row[3], row[4]])
        if user.verify_password(password):
            return user
        return None 
    
    def get_users():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username,email, name FROM Users ")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result