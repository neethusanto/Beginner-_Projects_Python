# Smart Password Generator

A secure and customizable random password generator and strength auditor built in Python.

## Core Features
- **Cryptographically Secure Generation**: Uses Python's standard `secrets` module (safe for sensitive secrets/passwords).
- **Customizable Length & Character Sets**: Configure length (4 to 128 characters) and selectively toggle lowercase, uppercase, numeric digits, and special characters.
- **Guaranteed Diversity**: Guarantees at least one character from each enabled set before random filling and shuffling.
- **Password Strength Analyzer**: Analyzes entropy, character pool, length, and diversity with a 0-100 visual meter bar.
- **Batch Generation**: Option to generate up to 10 passwords at a time.

## Concepts Demonstrated
- **Modules**: `secrets`, `random`, `string`, `math`.
- **Strings**: Manipulation, membership tests (`ascii_lowercase`, `ascii_uppercase`, `digits`, `punctuation`).
- **Loops**: Validation loops, list comprehensions, character shuffling.
- **Functions**: Pure generation function, strength evaluation function, and CLI handlers.

## How to Run
```bash
python password_generator.py
```

