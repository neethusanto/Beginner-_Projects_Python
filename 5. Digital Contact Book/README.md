# Digital Contact Book

A terminal-based digital contact management tool supporting rich contact attributes, search, update, deletion, and persistent storage.

## Core Features
- **Add Contact Details**: Store Name, Phone Number, Email, Category (Friends, Family, Work, etc.), and Address.
- **Search Contacts**: Instant substring matching across contact names, phone numbers, and email addresses.
- **Update Phone Numbers & Info**: Selectively edit existing contact details with a field-by-field prompt.
- **Delete Contacts**: Remove records with prompt confirmation to avoid accidental data loss.
- **Data Persistence**: Stores contact book state to `contacts.json`.

## Concepts Demonstrated
- **Dictionaries**: Fast lookups and nested record modeling (`{"name": ..., "phone": ..., ...}`).
- **Functions**: Clean separation of CRUD operations (`add_contact`, `search_contacts`, `update_phone_or_contact`, `delete_contact`).
- **File Handling**: Reading and writing structured JSON data to disk.
- **Exception Handling**: Robust protection against `FileNotFoundError`, `JSONDecodeError`, `KeyError`, `ValueError`, and `IOError`.

## How to Run
```bash
python contact_book.py
```

