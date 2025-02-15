import csv
import os


def view_expenses(expenses):
    """Function to display all expenses."""
    if not expenses:
        print("No expenses recorded.")
    else:
        for expense in expenses:
            print(
                f"Date: {expense['date']}, Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")


def add_expense(expenses):
    """Function to add a new expense record."""
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the category (e.g., Food, Travel): ")

    try:
        amount = float(input("Enter the amount: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    description = input("Enter a brief description: ")
    expenses.append({
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    })
    print("Expense added successfully.")


def set_budget():
    """Function to set a monthly budget and save it to a file."""
    try:
        budget = float(input("Enter your monthly budget: "))
        with open('budget.txt', 'w') as file:
            file.write(str(budget))
        print("Budget saved successfully.")
        return budget
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return set_budget()


def load_budget():
    """Function to load the budget from a file."""
    if os.path.exists('budget.txt'):
        with open('budget.txt', 'r') as file:
            try:
                return float(file.read().strip())
            except ValueError:
                print("Invalid budget data. Resetting budget.")
                return 0.0
    return 0.0


def track_budget(expenses, budget):
    """Function to track expenses and alert if budget is exceeded."""
    total_expenses = sum(expense['amount'] for expense in expenses)
    print(f"Total expenses: {total_expenses:.2f}")

    if total_expenses > budget:
        print("⚠️ Warning: You have exceeded your budget!")
    else:
        print(f"You are within your budget. You have {budget - total_expenses:.2f} remaining.")


def save_expenses(expenses, filename='expenses.csv'):
    """Function to save expenses to a file."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        for expense in expenses:
            writer.writerow([expense['date'], expense['category'], expense['amount'], expense['description']])
    print("Expenses saved successfully.")


def load_expenses(filename='expenses.csv'):
    """Function to load expenses from a file."""
    expenses = []
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(key in row for key in ['Date', 'Category', 'Amount', 'Description']):
                    try:
                        row['amount'] = float(row['Amount'])
                        expenses.append({
                            'date': row['Date'],
                            'category': row['Category'],
                            'amount': row['amount'],
                            'description': row['Description']
                        })
                    except ValueError:
                        print(f"Skipping invalid expense amount: {row}")
                else:
                    print(f"Skipping invalid expense record: {row}")
    except FileNotFoundError:
        print("No existing expenses found. Starting fresh.")
    return expenses


def main():
    expenses = load_expenses()
    budget = load_budget()

    while True:
        print("\n Personal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Track Budget")
        print("4. Set Budget")
        print("5. Save Expenses")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            track_budget(expenses, budget)
        elif choice == '4':
            budget = set_budget()
        elif choice == '5':
            save_expenses(expenses)
        elif choice == '6':
            save_expenses(expenses)
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please select a valid option.")


if __name__ == "__main__":
    main()
