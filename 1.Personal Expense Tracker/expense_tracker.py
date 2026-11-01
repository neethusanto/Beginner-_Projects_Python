"""
Personal Expense Tracker
Concepts used:
- Variables
- Lists
- Dictionaries
- Functions
- File Handling (CSV format)
"""

import os
from datetime import datetime

# File name used for persistent storage
FILE_NAME = "expenses.txt"

# Predefined categories
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]


def load_expenses():
    """
    Load expenses from a file.
    Returns a list of expense dictionaries.
    Demonstrates: File Handling (reading), Lists, Dictionaries, Variables.
    """
    expenses = []
    if not os.path.exists(FILE_NAME):
        return expenses

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 4:
                date, category, amount_str, description = parts
                try:
                    amount = float(amount_str)
                    expense = {
                        "date": date,
                        "category": category,
                        "amount": amount,
                        "description": description
                    }
                    expenses.append(expense)
                except ValueError:
                    continue
    return expenses


def save_expense_to_file(date, category, amount, description):
    """
    Appends a new expense to the file.
    Demonstrates: File Handling (writing/appending), Variables.
    """
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(f"{date},{category},{amount:.2f},{description}\n")


def add_expense(expenses):
    """
    Adds a daily expense by taking inputs and updating both the list and the file.
    Demonstrates: Functions, Variables, Lists, Dictionaries, User Input.
    """
    print("\n--- Add Daily Expense ---")
    
    # Date input (default to today)
    today = datetime.now().strftime("%Y-%m-%d")
    date_input = input(f"Enter date (YYYY-MM-DD) [Leave blank for today ({today})]: ").strip()
    if not date_input:
        date = today
    else:
        try:
            # Validate format
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print("Invalid date format. Using today's date instead.")
            date = today

    # Category selection
    print("\nSelect a category:")
    for idx, cat in enumerate(CATEGORIES, start=1):
        print(f"{idx}. {cat}")
    
    cat_choice = input(f"Enter choice (1-{len(CATEGORIES)}) [default: 1]: ").strip()
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(CATEGORIES):
        category = CATEGORIES[int(cat_choice) - 1]
    else:
        category = "Other"

    # Amount input
    while True:
        amount_input = input("Enter expense amount: ").strip()
        try:
            amount = float(amount_input)
            if amount < 0:
                print("Amount cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical amount.")

    # Description input
    description = input("Enter description/notes: ").strip()
    # Avoid commas in description to keep CSV formatting clean
    description = description.replace(",", ";")
    if not description:
        description = "N/A"

    # Create dictionary representing the expense
    new_expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }

    # Add to list and persist to file
    expenses.append(new_expense)
    save_expense_to_file(date, category, amount, description)
    print(f"\n Expense of ${amount:.2f} under '{category}' recorded successfully!")


def view_all_expenses(expenses):
    """
    Displays all recorded expenses in a formatted table.
    Demonstrates: Iteration over Lists of Dictionaries.
    """
    print("\n--- All Recorded Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'Date':<12} | {'Category':<15} | {'Amount ($)':<12} | {'Description'}")
    print("-" * 60)
    for exp in expenses:
        print(f"{exp['date']:<12} | {exp['category']:<15} | {exp['amount']:<12.2f} | {exp['description']}")


def calculate_total_expenses(expenses):
    """
    Calculates and displays total expenses overall and categorized.
    Demonstrates: Variables, Dictionaries (for category sums), Functions.
    """
    print("\n--- Expense Summary & Totals ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = 0.0
    category_totals = {}

    for exp in expenses:
        amount = exp["amount"]
        category = exp["category"]

        total += amount
        category_totals[category] = category_totals.get(category, 0.0) + amount

    print(f"Total Expenses: ${total:.2f}\n")
    print("Breakdown by Category:")
    for cat, cat_total in category_totals.items():
        percentage = (cat_total / total) * 100 if total > 0 else 0
        print(f" - {cat:<15}: ${cat_total:>8.2f} ({percentage:>5.1f}%)")


def monthly_expense_summary(expenses):
    """
    Displays expenses aggregated by month (YYYY-MM).
    Demonstrates: Dictionaries, String slicing, Aggregation.
    """
    print("\n--- Monthly Expense Summaries ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    monthly_totals = {}
    monthly_by_category = {}

    for exp in expenses:
        # Date format is YYYY-MM-DD, month is first 7 chars (YYYY-MM)
        month = exp["date"][:7]
        amount = exp["amount"]
        cat = exp["category"]

        monthly_totals[month] = monthly_totals.get(month, 0.0) + amount

        if month not in monthly_by_category:
            monthly_by_category[month] = {}
        monthly_by_category[month][cat] = monthly_by_category[month].get(cat, 0.0) + amount

    # Sort months chronologically
    sorted_months = sorted(monthly_totals.keys())

    for month in sorted_months:
        print(f"\nMonth: {month} | Total: ${monthly_totals[month]:.2f}")
        print("  Category Breakdown:")
        for cat, cat_amount in monthly_by_category[month].items():
            print(f"    - {cat:<12}: ${cat_amount:.2f}")


def main():
    """
    Main application loop with an interactive menu.
    """
    expenses = load_expenses()

    while True:
        print("\n=================================")
        print("    PERSONAL EXPENSE TRACKER     ")
        print("=================================")
        print("1. Add Daily Expense")
        print("2. View All Expenses")
        print("3. Calculate Total & Category Totals")
        print("4. Display Monthly Summaries")
        print("5. Exit")
        print("=================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_all_expenses(expenses)
        elif choice == "3":
            calculate_total_expenses(expenses)
        elif choice == "4":
            monthly_expense_summary(expenses)
        elif choice == "5":
            print("\nThank you for using Personal Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()

