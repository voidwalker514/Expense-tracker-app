import sqlite3
import hashlib

DB = "data/expenses.db"

def get_conn():
    return sqlite3.connect(DB)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def create_user_table():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def register_user(u, p):
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (u, hash_password(p)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(u, p):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (u, hash_password(p)))

    result = c.fetchone()
    conn.close()
    return result