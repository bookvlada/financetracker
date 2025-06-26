import calendar
import datetime
import csv
import os
from expences import Expense


def main():
    print(f"✨Running Expense Tracker!")
    expense_file_path="transactions.csv"
    budget=2000000
    expense=get_user_expense()

    save_expense_to_file(expense,expense_file_path)
    summarize_expenses(expense_file_path,budget)

def get_user_expense():
    print(f"✨Getting User Expense!")
    expense_name=input("✨Enter expense name:")
    expense_amount = float(input("✨Enter expense amount:"))
    print(f"You have entered expense name {expense_name} and expense amount {expense_amount} $")

    expense_categories=[
        "Food",
        "Home",
        "Work",
        "Fun",
        "Transport",
        "Education",
        "Clothing",
        "Health",
        "Gifts",
        "Misc"
    ]

    while True:
        print("Select a category:")
        for i, category_name in enumerate(expense_categories):
            print(f" {i+1}.{category_name}")
        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number{value_range}:"))-1
        if selected_index in range(len(expense_categories)):
            selected_category=expense_categories[selected_index]
            today = datetime.date.today().isoformat()
            new_expense=Expense(name=expense_name,amount=expense_amount,category=selected_category,date=today)
            return new_expense
        else:
            print("Invalid category. Please try again!")



def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    file_exists = os.path.exists(expense_file_path)
    write_header = not file_exists or os.stat(expense_file_path).st_size == 0
    with open(expense_file_path, "a", encoding='utf-8', newline='') as f:
        writer = csv.writer(f,delimiter=';')
        if write_header:
            writer.writerow(["name", "amount", "category", "date"])
        writer.writerow([expense.name, expense.amount, expense.category, expense.date])

def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expenses!")
    expenses: list[Expense] = []

    with open(expense_file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            try:
                expense_name, expense_amount, expense_category, expense_date = row
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                    date=expense_date
                )
                print(line_expense)
                expenses.append(line_expense)
            except ValueError:
                print(f"Skipping bad line: {row}")

    amount_by_category={}
    for expense in expenses:
        key=expense.category
        if key in amount_by_category:
            amount_by_category[key]+=expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses by category")
    for key, amount in amount_by_category.items():
        print(f"{key}:${amount:.2f}")

    total_spent=sum([x.amount for x in expenses])
    print(f"You have spent {total_spent:.2f} in total")

    remaining_budget=budget-total_spent
    print(f"You have{remaining_budget:.2f} left")

    now=datetime.datetime.now()
    days_in_month=calendar.monthrange(now.year,now.month)[1]
    remaining_days=days_in_month-now.day
    print(f"Remaining days in current month {remaining_days}")
    daily_budget=remaining_budget/remaining_days
    print(green(f"Your daily budget {daily_budget:.2f}"))

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__=="__main__":
    main()