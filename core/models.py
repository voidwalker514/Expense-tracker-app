from dataclasses import dataclass

@dataclass
class Expense:
    username: str
    date: str
    category: str
    amount: float
    type: str