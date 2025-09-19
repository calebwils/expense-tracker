import json
from datetime import datetime

class Expense:
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        # if no date is given, use today's date
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }


class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_data()

    def add_expense(self, amount, category, description, date=None):
        try:
            amount = float(amount)  # make sure the amount is a number
        except ValueError:
            print("❌ Invalid amount! Must be a number.")
            return

        expense = Expense(amount, category, description, date)
        self.expenses.append(expense)
        self.save_data()
        print("✅ Expense added successfully!")

    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                json.dump([exp.to_dict() for exp in self.expenses], f, indent=4)
        except Exception as e:
            print("❌ Error saving data:", e)

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.expenses = [Expense(**exp) for exp in data]
        except FileNotFoundError:
            self.expenses = []
        except Exception as e:
            print("❌ Error loading data:", e)

    def view_all(self):
        if not self.expenses:
            print("No expenses found.")
            return
        for idx, exp in enumerate(self.expenses, start=1):
            print(f"{idx}. {exp.date} - {exp.category} - {exp.amount} - {exp.description}")

    def view_by_category(self, category):
        filtered = [exp for exp in self.expenses if exp.category.lower() == category.lower()]
        if not filtered:
            print(f"No expenses found in category: {category}")
            return
        for idx, exp in enumerate(filtered, start=1):
            print(f"{idx}. {exp.date} - {exp.category} - {exp.amount} - {exp.description}")


def menu():
    tracker = ExpenseTracker()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Exit")
        print("4. View by category")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank: ") or None
            tracker.add_expense(amount, category, description, date)

        elif choice == "2":
            tracker.view_all()

        elif choice == "3":
            print("👋 Goodbye!")
            break

        elif choice == "4":
            category = input("Enter category to filter: ")
            tracker.view_by_category(category)

        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    menu()

    
