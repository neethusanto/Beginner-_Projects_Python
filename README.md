# Python Beginner Projects Collection

A collection of foundational, hands-on Python projects designed to practice core programming principles, data structures, object-oriented programming (OOP), file operations, and defensive programming.

---

## 📁 Repository Structure

```
Beginner-_Projects_Python/
│
├── 1.Personal Expense Tracker/      # Daily expense manager with categorization & reports
│   ├── expense_tracker.py
│   ├── expenses.txt
│   └── README.md
│
├── 2. Library Management System/    # Catalog & book borrowing system (OOP)
│   ├── library_management.py
│   └── README.md
│
├── 3. Quiz Application/             # Interactive MCQ quiz with scoring & explanations
│   ├── quiz_app.py
│   └── README.md
│
├── 4. Smart Password Generator/     # Cryptographic password generator & strength auditor
│   ├── password_generator.py
│   └── README.md
│
├── 5. Digital Contact Book/         # Contact directory with CRUD & exception handling
│   ├── contact_book.py
│   └── README.md
│
├── .gitignore                       # Ignored build, environment, and cache files
├── requirements.txt                 # Project dependencies & environment specification
└── README.md                        # Master repository documentation
```

---

## 🚀 Projects Overview

### 1. [Personal Expense Tracker](./1.Personal%20Expense%20Tracker)
Track daily expenses, categorize transactions, compute total and category-wise spending, and generate monthly summaries.
- **Key Concepts**: Variables, Lists, Dictionaries, Functions, File Handling (`expenses.txt`).
- **Run**:
  ```bash
  python "1.Personal Expense Tracker/expense_tracker.py"
  ```

### 2. [Library Management System](./2.%20Library%20Management%20System)
Manage a book catalog with features to add, remove, search, issue, and return books while tracking availability in real-time.
- **Key Concepts**: Object-Oriented Programming (OOP: `Book`, `Library`), Lists, Dictionaries, Functions, File Handling (`books.json`).
- **Run**:
  ```bash
  python "2. Library Management System/library_management.py"
  ```

### 3. [Quiz Application](./3.%20Quiz%20Application)
Interactive multiple-choice quiz that evaluates user answers, provides immediate feedback with technical explanations, and calculates final performance metrics and grades.
- **Key Concepts**: Conditional Statements, Loops, Functions, Dictionaries.
- **Run**:
  ```bash
  python "3. Quiz Application/quiz_app.py"
  ```

### 4. [Smart Password Generator](./4.%20Smart%20Password%20Generator)
Generates cryptographically secure passwords based on user-chosen length and character sets (uppercase, lowercase, numbers, symbols), and analyzes password strength with a 0–100 score and visual meter.
- **Key Concepts**: `secrets`, `random`, `string`, `math` modules, Loops, Functions, Strings.
- **Run**:
  ```bash
  python "4. Smart Password Generator/password_generator.py"
  ```

### 5. [Digital Contact Book](./5.%20Digital%20Contact%20Book)
Full-featured contact manager allowing users to add, search, update phone numbers/details, and safely delete contacts with persistent storage.
- **Key Concepts**: Dictionaries, Functions, File Handling (`contacts.json`), Comprehensive Exception Handling (`FileNotFoundError`, `JSONDecodeError`, `KeyError`, `IOError`).
- **Run**:
  ```bash
  python "5. Digital Contact Book/contact_book.py"
  ```

---

## 🛠️ Prerequisites & Installation

These projects are built using **standard Python library modules** (`secrets`, `json`, `csv`, `math`, `re`, `time`), so **no third-party dependencies are strictly required**.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/neethusanto/Beginner-_Projects_Python.git
   cd Beginner-_Projects_Python
   ```

2. **(Optional) Setup virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📝 License
This repository is open-source and available under the [MIT License](LICENSE).
