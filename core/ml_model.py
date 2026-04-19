import pandas as pd
from sklearn.linear_model import LinearRegression

class ExpensePredictor:

    def train(self, df):
        df = df.copy()
        df["month"] = df["date"].dt.month

        monthly = df.groupby("month")["amount"].sum().reset_index()

        self.X = monthly[["month"]]
        self.y = monthly["amount"]

        self.model = LinearRegression()
        self.model.fit(self.X, self.y)

    def predict(self, month):
        return self.model.predict([[month]])[0]