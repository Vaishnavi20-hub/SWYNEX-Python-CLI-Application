import json 
import os

DATA_FILE = "expenses.json" # In this file of json our input data will store

# Data  Management Function
def load_data():
    """load expenses from a JSON files with exception handling."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("\n [Error] Reading data file. Starting with an empty list.")
        return []
    except Exception as e:
        print(f'\n[Error] An unexpected error occurred: {e}')
        return []

def save_data(expenses):
    """Save expenses list to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(expenses, file, indent=4)
    except Exception as e:
        print(f'\n[Error] Fail to save data: {e}')

# Validation Functions

def get_valid_amount():
    """VAlidate user input for expense amount."""
    while True:
        try:
            amount = float(input("Enter Amount (₹): "))
            if amount <= 0:
                print("Amount Must Be Greater Than Zero.")
                continue
            return amount
        except ValueError:
            print("Invalid Input! Pese enter a valid number.")

def get_valid_string(prompt):
    """Validate that the string input is not empty."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Filed cannot be empty . try again.")
            continue
        return value
    
# Core Feature function

def add_expense():
    """Prompt user for details and save a new expense."""
    print("\n--- Add New Expense ---")
    category = get_valid_string("Enter category (e.g., Food, Rent, Travel): ")
    amount = get_valid_amount()
    description = get_valid_string("Enter description of the expense: ")
    
    expenses = load_data()
    expenses.append({
        "category": category,
        "amount": amount,
        "description": description
    })
    save_data(expenses)
    print("\nExpense added successfully!")

def view_expenses():
    """Display all tracker expenses."""
    expenses = load_data()
    if not expenses:
        print("\n No expenses logged yet.")
        return

    print("\n--- Tracked Expenses ---")
    total = 0.0
    for index, exp in enumerate(expenses, start=1):
        category = exp.get('category', 'N/A')
        amount = exp.get('amount', 0.0)
        desc = exp.get('description', 'N/A')
        print(f"{index}. [{category}] ₹{amount:.2f} - {desc}")
        total += amount
    print("-" * 30)
    print(f"Total Expenditure: ₹{total:.2f}")

def delete_expense():
    """Display expenses with numbers and delete the chosen entry to clear wrong data."""
    expenses = load_data()
    
    if not expenses:
        print("\nNo expenses found to delete.")
        return

    print("\n--- Current Expenses (Select to Delete) ---")
    for index, exp in enumerate(expenses, start=1):
        print(f"{index}. [{exp.get('category', 'N/A')}] ₹{exp.get('amount', 0):.2f} - {exp.get('description', 'N/A')}")
    
    while True:
        try:
            choice = input("\nEnter the number to delete (or 'c' to cancel): ").strip()
            if choice.lower() == 'c':
                print("Deletion cancelled.")
                return

            choice_idx = int(choice)
            if 1 <= choice_idx <= len(expenses):
                # Remove the entry and update JSON
                removed = expenses.pop(choice_idx - 1)
                save_data(expenses)
                print(f"\nSuccessfully deleted: [{removed.get('category')}] ₹{removed.get('amount')}")
                break
            else:
                print(f"Invalid entry number. Please choose between 1 and {len(expenses)}.")
            
        except ValueError:
            print("Invalid input! Please enter a valid number or 'c' to cancel.")


# Main User Interface loop

def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense ")
        print("2. View Expenses & Total ")
        print("3. Delete Expense ")
        print("4. Exit")
        print("===========================")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            print("\nExiting Expense Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select a option from 1 to 4.")

if __name__ == "__main__":
    main()
