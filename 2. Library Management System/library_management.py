"""
Library Management System
-------------------------
Features:
- Add and remove books
- Search books by title or author
- Issue and return books
- Track available books

Concepts Demonstrated:
- Object-Oriented Programming (OOP): Book, Library classes
- Lists & Dictionaries: Managing book collections and record lookups
- Functions: Modular operations with input validation
- File Handling: Persistent storage using JSON file
"""

import json
import os
from typing import Dict, List, Optional


class Book:
    """Represents a book in the library."""

    def __init__(self, book_id: str, title: str, author: str, is_issued: bool = False, issued_to: Optional[str] = None):
        self.book_id = book_id.strip()
        self.title = title.strip()
        self.author = author.strip()
        self.is_issued = is_issued
        self.issued_to = issued_to

    def to_dict(self) -> dict:
        """Convert book object to dictionary for JSON persistence."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "is_issued": self.is_issued,
            "issued_to": self.issued_to,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Reconstruct book object from dictionary."""
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            is_issued=data.get("is_issued", False),
            issued_to=data.get("issued_to"),
        )

    def __str__(self) -> str:
        status = f"Issued to {self.issued_to}" if self.is_issued else "Available"
        return f"[{self.book_id}] '{self.title}' by {self.author} | Status: {status}"


class Library:
    """Manages the catalog of books with persistent file storage."""

    def __init__(self, data_file: str = "books.json"):
        self.data_file = data_file
        # Dictionary for O(1) lookups by ID
        self.books: Dict[str, Book] = {}
        self.load_from_file()

    def load_from_file(self) -> None:
        """Load books from JSON file into the library dictionary."""
        if not os.path.exists(self.data_file):
            self._seed_initial_books()
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = {item["book_id"]: Book.from_dict(item) for item in data}
        except (json.JSONDecodeError, KeyError, OSError) as err:
            print(f"[!] Warning: Could not load data file ({err}). Starting fresh.")
            self.books = {}

    def save_to_file(self) -> None:
        """Save all book records to the JSON file."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json_data = [book.to_dict() for book in self.books.values()]
                json.dump(json_data, f, indent=4)
        except OSError as err:
            print(f"[!] Error saving to file: {err}")

    def _seed_initial_books(self) -> None:
        """Seeds default books if file does not exist yet."""
        initial = [
            Book("B101", "To Kill a Mockingbird", "Harper Lee"),
            Book("B102", "1984", "George Orwell"),
            Book("B103", "The Great Gatsby", "F. Scott Fitzgerald"),
            Book("B104", "Clean Code", "Robert C. Martin"),
            Book("B105", "Python Crash Course", "Eric Matthes"),
        ]
        self.books = {b.book_id: b for b in initial}
        self.save_to_file()

    def add_book(self, book_id: str, title: str, author: str) -> bool:
        """Add a new book to the library."""
        book_id = book_id.strip().upper()
        if not book_id or not title.strip() or not author.strip():
            print("[X] Error: Book ID, title, and author cannot be empty.")
            return False

        if book_id in self.books:
            print(f"[X] Error: Book with ID '{book_id}' already exists.")
            return False

        book = Book(book_id, title, author)
        self.books[book_id] = book
        self.save_to_file()
        print(f"[✓] Book successfully added: {book}")
        return True

    def remove_book(self, book_id: str) -> bool:
        """Remove a book from the library by ID."""
        book_id = book_id.strip().upper()
        if book_id not in self.books:
            print(f"[X] Error: No book found with ID '{book_id}'.")
            return False

        book = self.books[book_id]
        if book.is_issued:
            print(f"[X] Cannot remove '{book.title}' because it is currently issued to {book.issued_to}. Return it first.")
            return False

        del self.books[book_id]
        self.save_to_file()
        print(f"[✓] Book '{book.title}' (ID: {book_id}) has been removed.")
        return True

    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author (case-insensitive substring match)."""
        query_lower = query.strip().lower()
        if not query_lower:
            return []

        results = [
            b for b in self.books.values()
            if query_lower in b.title.lower() or query_lower in b.author.lower()
        ]
        return results

    def issue_book(self, book_id: str, borrower_name: str) -> bool:
        """Issue an available book to a borrower."""
        book_id = book_id.strip().upper()
        borrower_name = borrower_name.strip()

        if not borrower_name:
            print("[X] Borrower name cannot be empty.")
            return False

        if book_id not in self.books:
            print(f"[X] No book found with ID '{book_id}'.")
            return False

        book = self.books[book_id]
        if book.is_issued:
            print(f"[!] Book is already issued to {book.issued_to}.")
            return False

        book.is_issued = True
        book.issued_to = borrower_name
        self.save_to_file()
        print(f"[✓] Book '{book.title}' issued successfully to {borrower_name}.")
        return True

    def return_book(self, book_id: str) -> bool:
        """Return an issued book."""
        book_id = book_id.strip().upper()
        if book_id not in self.books:
            print(f"[X] No book found with ID '{book_id}'.")
            return False

        book = self.books[book_id]
        if not book.is_issued:
            print(f"[!] Book '{book.title}' was not issued; it is already available.")
            return False

        borrower = book.issued_to
        book.is_issued = False
        book.issued_to = None
        self.save_to_file()
        print(f"[✓] Book '{book.title}' returned successfully (previously issued to {borrower}).")
        return True

    def get_all_books(self) -> List[Book]:
        """Return a list of all books."""
        return list(self.books.values())

    def get_available_books(self) -> List[Book]:
        """Return a list of only currently available books."""
        return [b for b in self.books.values() if not b.is_issued]

    def get_issued_books(self) -> List[Book]:
        """Return a list of currently issued books."""
        return [b for b in self.books.values() if b.is_issued]


def print_table(books: List[Book], title: str = "Books List") -> None:
    """Helper function to print formatted table of books."""
    print(f"\n--- {title} (Total: {len(books)}) ---")
    if not books:
        print("  No records found.")
        return

    header = f"{'Book ID':<10} | {'Title':<30} | {'Author':<22} | {'Status':<25}"
    separator = "-" * len(header)
    print(header)
    print(separator)
    for b in books:
        status_text = f"Issued ({b.issued_to})" if b.is_issued else "Available"
        title_str = (b.title[:27] + "...") if len(b.title) > 30 else b.title
        author_str = (b.author[:19] + "...") if len(b.author) > 22 else b.author
        print(f"{b.book_id:<10} | {title_str:<30} | {author_str:<22} | {status_text:<25}")
    print(separator)


def main():
    library = Library()

    while True:
        print("\n" + "=" * 50)
        print("        LIBRARY MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. View All Books")
        print("2. View Available Books Only")
        print("3. View Issued Books")
        print("4. Search Books (by Title / Author)")
        print("5. Add a New Book")
        print("6. Remove a Book")
        print("7. Issue a Book")
        print("8. Return a Book")
        print("9. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            print_table(library.get_all_books(), "All Library Books")

        elif choice == "2":
            print_table(library.get_available_books(), "Available Books for Borrowing")

        elif choice == "3":
            print_table(library.get_issued_books(), "Currently Issued Books")

        elif choice == "4":
            query = input("Enter title or author keyword to search: ").strip()
            results = library.search_books(query)
            print_table(results, f"Search Results for '{query}'")

        elif choice == "5":
            print("\n-- Add New Book --")
            book_id = input("Enter Book ID (e.g. B106): ").strip()
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author Name: ").strip()
            library.add_book(book_id, title, author)

        elif choice == "6":
            print("\n-- Remove Book --")
            book_id = input("Enter Book ID to remove: ").strip()
            confirm = input(f"Are you sure you want to delete book {book_id}? (y/n): ").strip().lower()
            if confirm == "y":
                library.remove_book(book_id)
            else:
                print("Operation cancelled.")

        elif choice == "7":
            print("\n-- Issue Book --")
            book_id = input("Enter Book ID to issue: ").strip()
            borrower = input("Enter borrower's name: ").strip()
            library.issue_book(book_id, borrower)

        elif choice == "8":
            print("\n-- Return Book --")
            book_id = input("Enter Book ID to return: ").strip()
            library.return_book(book_id)

        elif choice == "9":
            print("\nThank you for using Library Management System. Goodbye!")
            break

        else:
            print("[X] Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()

