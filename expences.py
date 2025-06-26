class Expense:
    def __init__(self, name, category, amount,date)-> None:
        self.name=name
        self.amount = float(amount)
        self.category=category
        self.date=date


    def __repr__(self):
        return f"<Expense:{self.name},${self.amount:.2f},{self.category},{self.date}>"