"""
Smart Password Generator
------------------------
Features:
- Generate cryptographically strong random passwords
- Select custom password length
- Custom configuration: include/exclude uppercase, lowercase, numbers, special characters
- Check and score password strength (Weak, Medium, Strong, Very Strong)
- Generate multiple passwords at once

Concepts Demonstrated:
- random / secrets: Cryptographically secure character selection and shuffling
- string: Character sets (ascii_lowercase, ascii_uppercase, digits, punctuation)
- Loops: Ensuring character requirements are satisfied
- Functions: Modular password generation, validation, and strength scoring
- Modules: Working with standard library modules (secrets, random, string, math)
"""

import math
import secrets
import string
from typing import Dict, Tuple


# Predefined character pools
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SPECIAL = "!@#$%^&*()-_=+[]{}|;:,.<>?"


def evaluate_password_strength(password: str) -> Tuple[str, int, str]:
    """
    Evaluates password strength based on entropy, length, and character diversity.
    Returns: (rating_label, score_out_of_100, feedback)
    """
    if not password:
        return "None", 0, "Password is empty."

    length = len(password)
    has_lower = any(c in LOWERCASE for c in password)
    has_upper = any(c in UPPERCASE for c in password)
    has_digit = any(c in DIGITS for c in password)
    has_special = any(c in SPECIAL for c in password)

    # Pool size calculation for Shannon entropy
    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += len(SPECIAL)

    entropy = length * math.log2(pool_size) if pool_size > 0 else 0

    score = 0
    # Length contribution (up to 40 points)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    else:
        score += 10

    # Diversity contribution (up to 40 points)
    diversity_count = sum([has_lower, has_upper, has_digit, has_special])
    score += diversity_count * 10

    # Entropy contribution (up to 20 points)
    if entropy >= 70:
        score += 20
    elif entropy >= 50:
        score += 15
    elif entropy >= 30:
        score += 10
    else:
        score += 5

    score = min(score, 100)

    if score >= 85 and length >= 12:
        rating = "Very Strong"
        feedback = "Excellent! Highly resilient against brute-force and dictionary attacks."
    elif score >= 65 and length >= 8:
        rating = "Strong"
        feedback = "Good security level for most accounts."
    elif score >= 45:
        rating = "Medium"
        feedback = "Moderate security. Consider increasing length and mixing special symbols."
    else:
        rating = "Weak"
        feedback = "Vulnerable to attacks. Increase length to 12+ characters and include digits and symbols."

    return rating, score, feedback


def generate_password(
    length: int = 14,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str:
    """
    Generates a cryptographically strong random password ensuring at least one
    character from each selected pool is guaranteed to be present.
    """
    selected_pools = []
    guaranteed_chars = []

    if use_lower:
        selected_pools.append(LOWERCASE)
        guaranteed_chars.append(secrets.choice(LOWERCASE))
    if use_upper:
        selected_pools.append(UPPERCASE)
        guaranteed_chars.append(secrets.choice(UPPERCASE))
    if use_digits:
        selected_pools.append(DIGITS)
        guaranteed_chars.append(secrets.choice(DIGITS))
    if use_special:
        selected_pools.append(SPECIAL)
        guaranteed_chars.append(secrets.choice(SPECIAL))

    if not selected_pools:
        raise ValueError("At least one character type must be selected!")

    if length < len(guaranteed_chars):
        raise ValueError(f"Password length must be at least {len(guaranteed_chars)} to satisfy selected criteria.")

    # Combine all characters from chosen pools
    all_allowed = "".join(selected_pools)

    # Fill remaining characters randomly
    remaining_len = length - len(guaranteed_chars)
    remaining_chars = [secrets.choice(all_allowed) for _ in range(remaining_len)]

    # Combine and shuffle characters cryptographically
    all_chars = guaranteed_chars + remaining_chars
    # SystemRandom shuffle to prevent predictable positions
    rng = secrets.SystemRandom()
    rng.shuffle(all_chars)

    return "".join(all_chars)


def print_strength_bar(score: int) -> str:
    """Returns visual meter bar for score out of 100."""
    filled = int(score / 5)  # 20 segments
    bar = "█" * filled + "░" * (20 - filled)
    return f"[{bar}] {score}/100"


def generate_password_flow():
    """Interactive CLI flow for generating passwords."""
    print("\n--- Generate Passwords ---")

    # Get length
    while True:
        try:
            length_input = input("Enter password length (recommended 12-32, default 16): ").strip()
            if not length_input:
                length = 16
                break
            length = int(length_input)
            if length < 4:
                print("[!] Length must be at least 4.")
                continue
            if length > 128:
                print("[!] Maximum allowed length is 128.")
                continue
            break
        except ValueError:
            print("[!] Please enter a valid integer.")

    # Include options
    print("Select character types (press Enter for 'Yes'):")
    use_upper = input("Include Uppercase letters (A-Z)? (Y/n): ").strip().lower() != 'n'
    use_lower = input("Include Lowercase letters (a-z)? (Y/n): ").strip().lower() != 'n'
    use_digits = input("Include Numbers (0-9)? (Y/n): ").strip().lower() != 'n'
    use_special = input("Include Special symbols (!@#$...)? (Y/n): ").strip().lower() != 'n'

    if not (use_upper or use_lower or use_digits or use_special):
        print("[X] You must enable at least one character type!")
        return

    # Count
    try:
        count_input = input("How many passwords to generate? (default 1): ").strip()
        count = int(count_input) if count_input else 1
        count = max(1, min(count, 10))
    except ValueError:
        count = 1

    print("\n" + "=" * 55)
    print(f"  Generated {count} Password(s):")
    print("=" * 55)

    for i in range(1, count + 1):
        pwd = generate_password(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_special=use_special
        )
        rating, score, feedback = evaluate_password_strength(pwd)
        meter = print_strength_bar(score)

        print(f"\nPassword #{i}:  {pwd}")
        print(f"Strength    :  {rating}  {meter}")
        print(f"Feedback    :  {feedback}")

    print("=" * 55)


def check_custom_password_flow():
    """Interactive CLI flow to inspect user-provided password strength."""
    print("\n--- Test Password Strength ---")
    pwd = input("Enter password to test: ").strip()
    if not pwd:
        print("[!] Input cannot be empty.")
        return

    rating, score, feedback = evaluate_password_strength(pwd)
    meter = print_strength_bar(score)

    print("\n" + "-" * 50)
    print(f"Password Evaluated: {pwd}")
    print(f"Length            : {len(pwd)} characters")
    print(f"Strength Rating   : {rating}")
    print(f"Security Score    : {meter}")
    print(f"Feedback          : {feedback}")
    print("-" * 50)


def main():
    while True:
        print("\n" + "=" * 50)
        print("         SMART PASSWORD GENERATOR & CHECKER")
        print("=" * 50)
        print("1. Generate New Password(s)")
        print("2. Check Strength of an Existing Password")
        print("3. Quick Generate (16 chars, all types)")
        print("4. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            generate_password_flow()
        elif choice == "2":
            check_custom_password_flow()
        elif choice == "3":
            pwd = generate_password(16, True, True, True, True)
            rating, score, feedback = evaluate_password_strength(pwd)
            print(f"\nGenerated: {pwd}")
            print(f"Strength : {rating} {print_strength_bar(score)}")
            print(f"Note     : {feedback}")
        elif choice == "4":
            print("\nStay secure! Goodbye.")
            break
        else:
            print("[X] Invalid choice. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()

