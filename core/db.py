import sqlite3

DB = "data/expenses.db"

def get_conn():
    return sqlite3.connect(DB)

def create_table():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        category TEXT,
        amount REAL,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_data(df):
    conn = get_conn()
    c = conn.cursor()

    # 🔥 CRITICAL FIX: ensure clean list of tuples
    rows = [
        (
            str(row.username),
            str(row.date),
            str(row.category),
            float(row.amount),
            str(row.type)
        )
        for row in df.itertuples(index=False)
    ]

    c.executemany("""
        INSERT INTO expenses (username, date, category, amount, type)
        VALUES (?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()

    print("✅ INSERTED ROWS:", len(rows))