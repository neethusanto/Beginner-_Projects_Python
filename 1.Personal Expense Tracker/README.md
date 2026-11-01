# Personal Expense Tracker

A Python console application to track daily expenses, categorize them, calculate total and category-wise spending, and generate monthly summaries.

## Core Features
- **Add Daily Expenses**: Enter amount, category, date, and description.
- **Categorize Expenses**: Categorization with pre-set types (`Food`, `Travel`, `Shopping`, `Bills`, etc.).
- **Calculate Total Expenses**: View overall spending with breakdown and percentages by category.
- **Monthly Expense Summaries**: Aggregated summaries grouped by year-month (`YYYY-MM`).
- **File Handling**: Persistent data storage in `expenses.txt`.

## Programming Concepts Demonstrated
- **Variables**: Storing user inputs, amounts, dates, and calculations.
- **Lists**: Maintaining the expense records list (`expenses`) and predefined categories (`CATEGORIES`).
- **Dictionaries**: Storing individual expense records (`{"date": ..., "category": ..., "amount": ..., "description": ...}`) and category/month aggregates.
- **Functions**: Modular logic broken into functions (`load_expenses`, `add_expense`, `calculate_total_expenses`, `monthly_expense_summary`, etc.).
- **File Handling**: Reading and writing records to/from a CSV-formatted text file (`expenses.txt`).

## How to Run
```bash
python expense_tracker.py
```

