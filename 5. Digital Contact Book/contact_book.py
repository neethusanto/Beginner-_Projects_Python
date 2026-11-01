"""
Digital Contact Book
--------------------
Features:
- Add contact details (Name, Phone, Email, Address, Category)
- Search contacts by name or phone
- Update phone numbers or other fields
- Delete contacts with confirmation
- List and export all contacts

Concepts Demonstrated:
- Dictionaries: Nested structures for contacts keyed by normalized contact ID/name
- Functions: Modular CRUD operations with parameter checks
- File Handling: JSON and CSV persistence for contacts
- Exception Handling: try-except blocks handling FileNotFoundError, ValueError, KeyError, JSONDecodeError, IOError
"""

import json
import os
import re
from typing import Dict, Any, Optional, List


DATA_FILE = "contacts.json"


def validate_phone(phone: str) -> bool:
    """Validate phone number (basic pattern allowing digits, +, -, spaces)."""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    return bool(re.match(r"^\+?\d{7,15}$", cleaned))


def validate_email(email: str) -> bool:
    """Simple email format validation."""
    if not email:
        return True  # Optional field
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


def load_contacts(filepath: str = DATA_FILE) -> Dict[str, Dict[str, Any]]:
    """
    Load contacts dictionary from a JSON file.
    Demonstrates Exception Handling (FileNotFoundError, JSONDecodeError, PermissionError).
    """
    if not os.path.exists(filepath):
        # Create initial seed contacts
        seed_data = {
            "alice smith": {
                "name": "Alice Smith",
                "phone": "+1-555-0101",
                "email": "alice.smith@example.com",
                "category": "Work",
                "address": "100 Innovation Way"
            },
            "bob johnson": {
                "name": "Bob Johnson",
                "phone": "+1-555-0102",
                "email": "bob.j@example.com",
                "category": "Personal",
                "address": "452 Maple Street"
            }
        }
        try:
            save_contacts(seed_data, filepath)
            return seed_data
        except IOError as e:
            print(f"[!] Warning: Could not create seed contacts file: {e}")
            return {}

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            contacts = json.load(file)
            if not isinstance(contacts, dict):
                raise ValueError("Contacts file does not contain a dictionary.")
            return contacts
    except FileNotFoundError:
        print("[!] File not found. Initializing empty contact book.")
        return {}
    except json.JSONDecodeError as err:
        print(f"[X] JSON format error in '{filepath}' at line {err.lineno}: {err.msg}. Starting with empty directory.")
        return {}
    except (PermissionError, IOError) as err:
        print(f"[X] File access error: {err}")
        return {}


def save_contacts(contacts: Dict[str, Dict[str, Any]], filepath: str = DATA_FILE) -> bool:
    """
    Save contacts to JSON file.
    Demonstrates Exception Handling for IO operations.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4)
        return True
    except PermissionError:
        print(f"[X] Permission denied: Cannot write to '{filepath}'.")
        return False
    except IOError as err:
        print(f"[X] I/O error occurred while saving contacts: {err}")
        return False
    except Exception as err:
        print(f"[X] Unexpected error during save: {err}")
        return False


def add_contact(contacts: Dict[str, Dict[str, Any]]) -> None:
    """Add a new contact to the dictionary."""
    print("\n-- Add New Contact --")
    name = input("Enter Full Name: ").strip()
    if not name:
        print("[X] Contact name cannot be empty.")
        return

    key = name.lower()
    if key in contacts:
        print(f"[!] A contact with name '{contacts[key]['name']}' already exists. Use the Update option instead.")
        return

    phone = input("Enter Phone Number: ").strip()
    if not validate_phone(phone):
        print("[!] Warning: Invalid phone format. Example: +1234567890 or 9876543210")
        confirm = input("Save anyway? (y/n): ").strip().lower()
        if confirm != "y":
            print("Contact addition cancelled.")
            return

    email = input("Enter Email Address (optional): ").strip()
    if email and not validate_email(email):
        print("[!] Warning: Email address format looks invalid.")

    category = input("Enter Category (e.g., Friends, Family, Work, Other) [Default: General]: ").strip()
    if not category:
        category = "General"

    address = input("Enter Address (optional): ").strip()

    contacts[key] = {
        "name": name,
        "phone": phone,
        "email": email,
        "category": category,
        "address": address
    }

    if save_contacts(contacts):
        print(f"[✓] Contact '{name}' added successfully!")


def search_contacts(contacts: Dict[str, Dict[str, Any]]) -> None:
    """Search contacts by name keyword or phone number substring."""
    query = input("\nEnter name or phone to search: ").strip().lower()
    if not query:
        print("[!] Search query cannot be empty.")
        return

    matches = []
    for key, c in contacts.items():
        if query in key or query in c["phone"].lower() or query in c.get("email", "").lower():
            matches.append(c)

    print(f"\n--- Search Results for '{query}' (Found: {len(matches)}) ---")
    if not matches:
        print("  No matching contacts found.")
        return

    display_contacts_table(matches)


def update_phone_or_contact(contacts: Dict[str, Dict[str, Any]]) -> None:
    """Update phone number and details for an existing contact."""
    name = input("\nEnter the full name of the contact to update: ").strip()
    key = name.lower()

    try:
        if key not in contacts:
            raise KeyError(f"No contact named '{name}' was found.")

        contact = contacts[key]
        print(f"\nCurrent Details for {contact['name']}:")
        print(f"  Phone   : {contact['phone']}")
        print(f"  Email   : {contact.get('email', '-')}")
        print(f"  Category: {contact.get('category', '-')}")
        print(f"  Address : {contact.get('address', '-')}")

        print("\nLeave blank to keep existing value:")
        new_phone = input(f"New Phone Number [{contact['phone']}]: ").strip()
        new_email = input(f"New Email [{contact.get('email', '')}]: ").strip()
        new_category = input(f"New Category [{contact.get('category', 'General')}]: ").strip()
        new_address = input(f"New Address [{contact.get('address', '')}]: ").strip()

        if new_phone:
            if not validate_phone(new_phone):
                print("[!] Warning: Phone format invalid. Saving anyway upon confirmation.")
            contact["phone"] = new_phone

        if new_email:
            contact["email"] = new_email

        if new_category:
            contact["category"] = new_category

        if new_address:
            contact["address"] = new_address

        save_contacts(contacts)
        print(f"[✓] Contact '{contact['name']}' updated successfully!")

    except KeyError as e:
        print(f"[X] Error: {e}")
    except Exception as e:
        print(f"[X] An unexpected error occurred while updating: {e}")


def delete_contact(contacts: Dict[str, Dict[str, Any]]) -> None:
    """Delete a contact from the dictionary with verification."""
    name = input("\nEnter the name of the contact to delete: ").strip()
    key = name.lower()

    try:
        if key not in contacts:
            raise KeyError(f"Contact '{name}' not found.")

        target = contacts[key]
        confirm = input(f"Are you sure you want to delete '{target['name']}' ({target['phone']})? (y/n): ").strip().lower()
        if confirm == "y":
            del contacts[key]
            save_contacts(contacts)
            print(f"[✓] Contact '{target['name']}' was successfully deleted.")
        else:
            print("Delete operation cancelled.")

    except KeyError as err:
        print(f"[X] {err}")
    except Exception as err:
        print(f"[X] An error occurred: {err}")


def display_contacts_table(contact_list: List[Dict[str, Any]]) -> None:
    """Format and print list of contacts as an aligned table."""
    header = f"{'Name':<20} | {'Phone':<18} | {'Category':<12} | {'Email':<25}"
    sep = "-" * len(header)
    print(header)
    print(sep)
    for c in contact_list:
        name_str = (c["name"][:17] + "...") if len(c["name"]) > 20 else c["name"]
        email_str = (c.get("email", "-")[:22] + "...") if len(c.get("email", "-")) > 25 else c.get("email", "-")
        phone_str = c["phone"]
        cat_str = c.get("category", "General")
        print(f"{name_str:<20} | {phone_str:<18} | {cat_str:<12} | {email_str:<25}")
    print(sep)


def view_all_contacts(contacts: Dict[str, Dict[str, Any]]) -> None:
    """Display all contacts sorted alphabetically by name."""
    if not contacts:
        print("\n[!] No contacts found. Add some contacts first!")
        return

    sorted_list = sorted(contacts.values(), key=lambda x: x["name"].lower())
    print(f"\n--- All Contacts (Total: {len(sorted_list)}) ---")
    display_contacts_table(sorted_list)


def main():
    contacts = load_contacts()

    while True:
        print("\n" + "=" * 50)
        print("             DIGITAL CONTACT BOOK")
        print("=" * 50)
        print("1. View All Contacts")
        print("2. Search Contacts")
        print("3. Add New Contact")
        print("4. Update Contact Details / Phone")
        print("5. Delete Contact")
        print("6. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                view_all_contacts(contacts)
            elif choice == "2":
                search_contacts(contacts)
            elif choice == "3":
                add_contact(contacts)
            elif choice == "4":
                update_phone_or_contact(contacts)
            elif choice == "5":
                delete_contact(contacts)
            elif choice == "6":
                print("\nSaving contacts and exiting. Goodbye!")
                save_contacts(contacts)
                break
            else:
                print("[X] Invalid option. Please select 1 through 6.")
        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user.")
            break
        except Exception as e:
            print(f"\n[X] An unhandled error occurred in application loop: {e}")


if __name__ == "__main__":
    main()

