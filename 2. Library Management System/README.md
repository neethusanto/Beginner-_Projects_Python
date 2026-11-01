# Library Management System

A complete Python console application for managing library books with persistent storage.

## Core Features
- **Add & Remove Books**: Manage book catalog with uniqueness validation.
- **Search Books**: Case-insensitive search across titles and authors.
- **Issue & Return Books**: Track who borrowed each book and update status.
- **Track Available Books**: Instant filtering between available and issued books.
- **Data Persistence**: Automatically loads from and saves to `books.json`.

## Concepts Demonstrated
- **OOP (Object-Oriented Programming)**: `Book` and `Library` classes encapsulating data and behavior.
- **Lists**: Formatting and displaying filtered collections of books.
- **Dictionaries**: O(1) keyed lookup by Book ID and JSON serialization.
- **Functions**: Clean modular methods with defensive error checking.
- **File Handling**: JSON reading and writing for persistent state.

## How to Run
```bash
python library_management.py
```

