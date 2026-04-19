import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_dashboard(df):

    st.markdown("## 📊 Expense Analysis")

    # ---------------- CLEAN DATA ----------------
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["type"] = df["type"].astype(str).str.lower().str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna()

    # ---------------- SUMMARY ----------------
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    savings = income - expense

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Income", f"₹{income:,.0f}")
    col2.metric("💸 Expense", f"₹{expense:,.0f}")
    col3.metric("💡 Savings", f"₹{savings:,.0f}")

    st.markdown("---")

    # ---------------- CATEGORY CHART ----------------
    st.markdown("### 📌 Category-wise Spending")

    expense_df = df[df["type"] == "expense"]

    if expense_df.empty:
        st.warning("No expense data available")
        return

    cat = expense_df.groupby("category")["amount"].sum()

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        fig, ax = plt.subplots(figsize=(6,4))
        cat.plot(kind="bar", ax=ax)
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Expenses by Category")
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # ---------------- MONTHLY TREND ----------------
    st.markdown("### 📈 Monthly Trend")

    df["month"] = df["date"].dt.month
    monthly = df.groupby("month")["amount"].sum()

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6,4))
        monthly.plot(marker="o", ax=ax2)
        ax2.set_ylabel("Amount (₹)")
        ax2.set_title("Monthly Spending")
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("---")

    # ---------------- BUDGET WARNING ----------------
    st.markdown("### 💰 Budget Monitoring")

    budget = st.number_input("Set Monthly Budget (₹)", min_value=0, value=20000, step=1000)

    current_month = df["date"].dt.month.max()

    monthly_expense = df[
        (df["type"] == "expense") & (df["date"].dt.month == current_month)
    ]["amount"].sum()

    st.write(f"📅 Current Month Expense: ₹{monthly_expense:,.0f}")

    if monthly_expense > budget:
        st.error("🚨 You have exceeded your budget!")
    elif monthly_expense > 0.8 * budget:
        st.warning("⚠ You are close to your budget limit!")
    else:
        st.success("✅ You are within your budget.")

    st.markdown("---")

    # ---------------- OVERSPENDING ALERT ----------------
    st.markdown("### 🚨 Overspending Insights")

    category_spend = expense_df.groupby("category")["amount"].sum()

    top_category = category_spend.idxmax()
    top_value = category_spend.max()

    total_expense = category_spend.sum()
    percentage = (top_value / total_expense) * 100

    st.write(f"🔝 Highest Spending Category: **{top_category}** (₹{top_value:,.0f})")

    if percentage > 40:
        st.error(f"🚨 You are overspending heavily on {top_category} ({percentage:.1f}%)")
    elif percentage > 25:
        st.warning(f"⚠ High spending in {top_category} ({percentage:.1f}%)")
    else:
        st.success("✅ Spending distribution looks balanced")

    st.info(f"💡 Tip: Try reducing spending in **{top_category}** to improve savings.")