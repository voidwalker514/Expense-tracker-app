import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data(n=500):

    categories = ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment"]

    data = []
    start = datetime(2024, 1, 1)

    for _ in range(n):
        date = start + timedelta(days=random.randint(0, 180))
        category = random.choice(categories)

        # 🔥 FIX: lowercase type
        type_ = random.choices(["expense", "income"], weights=[0.8, 0.2])[0]

        amount = random.uniform(100, 5000) if type_ == "expense" else random.uniform(10000, 80000)

        data.append([date, category, float(amount), type_])

    df = pd.DataFrame(data, columns=["date", "category", "amount", "type"])

    # 🔥 FORCE CLEAN
    df["type"] = df["type"].str.lower().str.strip()

    return df