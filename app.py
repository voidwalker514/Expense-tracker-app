import streamlit as st
import sqlite3
import pandas as pd

from dashboard import show_dashboard

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------------- FINTECH DARK UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0E1117;
}

/* Headings */
h1, h2, h3 {
    color: #00FFD1;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #1C1F26;
    border: 1px solid #2A2D34;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

/* Inputs */
.stNumberInput input {
    background-color: #1C1F26;
    color: white;
}

/* Divider spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("💰 Expense Tracker Dashboard")

# ---------------- LOAD DATA ----------------
conn = sqlite3.connect("data/expenses.db")
df = pd.read_sql("SELECT * FROM expenses", conn)
conn.close()

# ---------------- CLEAN DATA ----------------
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["type"] = df["type"].astype(str).str.lower().str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.dropna()

# ---------------- CHECK ----------------
if df.empty:
    st.error("❌ No data found. Run main.py first.")
    st.stop()

# ---------------- PREVIEW ----------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df.head())

# ---------------- DASHBOARD ----------------
show_dashboard(df)