import pandas as pd

def load_user_data(conn, username):
    df = pd.read_sql(f"SELECT * FROM expenses WHERE username='{username}'", conn)
    df["date"] = pd.to_datetime(df["date"])
    return df