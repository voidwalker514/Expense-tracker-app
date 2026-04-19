import os
import sqlite3
from src.data_generator import generate_data
from core.db import create_table, insert_data

# Create data folder
os.makedirs("data", exist_ok=True)

print("🔧 Creating fresh database...")

# 🔥 DELETE OLD DB (IMPORTANT)
db_path = "data/expenses.db"
if os.path.exists(db_path):
    os.remove(db_path)

# Create table
create_table()

# Generate data (increase if you want more)
df = generate_data(2000)

# ---------------- CLEAN DATA ----------------
df["username"] = "admin"

# Ensure proper formats
df["type"] = df["type"].astype(str).str.lower().str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["amount"] = df["amount"].astype(float)
df["date"] = df["date"].astype(str)

# Reorder columns
df = df[["username", "date", "category", "amount", "type"]]

print("📊 Generated rows:", len(df))

# Insert into DB
insert_data(df)

# ---------------- VERIFY ----------------
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM expenses")
count = c.fetchone()[0]

conn.close()

print("✅ Rows in DB:", count)

print("🚀 Now run: streamlit run app.py")