# Function to view all expenses
import hashlib

d1 ={'date': '2025', 'amount': '12.00', 'Desc': 'For Lunch'}
d2 ={'date': '2024', 'amount': '24.00', 'Desc': 'For Lunch'}

listItem = [d1, d2]


print(listItem)
var1 = input('Enter Expecse ')
print(var1)
def view_expenses(expenses):
    """Function to display all expenses."""
    if not expenses:
        print("No expenses recorded.")
    else:
        for expense in expenses:
            # Check if the keys exist before accessing them
            if all(key in expense for key in ['date', 'category', 'amount', 'description']):
                print(f"Date: {expense['date']}, Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")
            else:
                print(f"Invalid expense record: {expense}")