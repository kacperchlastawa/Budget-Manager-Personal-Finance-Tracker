from conection import get_connection

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    def insert_user(user):
        conn = get_connection()
        cursor = conn.cursor()
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
    
    def get_user_by_username(username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row