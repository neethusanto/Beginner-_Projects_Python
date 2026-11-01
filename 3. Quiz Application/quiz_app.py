"""
Quiz Application
----------------
Features:
- Display multiple-choice questions (MCQs)
- Calculate user score and percentage
- Show immediate/detailed correct and incorrect answer breakdown
- Display final detailed performance report

Concepts Demonstrated:
- Conditional Statements: Validating user input and comparing answers
- Loops: Iterating through questions and retry options
- Functions: Modular quiz flow, evaluation, and reporting
- Dictionaries: Structured question bank with options and explanations
"""

import time
from typing import Dict, List, Any


QUESTION_BANK: List[Dict[str, Any]] = [
    {
        "id": 1,
        "question": "Which keyword is used to define a function in Python?",
        "options": {
            "A": "function",
            "B": "def",
            "C": "fun",
            "D": "define"
        },
        "answer": "B",
        "explanation": "'def' stands for define and is Python's keyword for creating functions."
    },
    {
        "id": 2,
        "question": "Which data type in Python is mutable?",
        "options": {
            "A": "tuple",
            "B": "str",
            "C": "list",
            "D": "int"
        },
        "answer": "C",
        "explanation": "Lists can be modified in-place, whereas tuples, strings, and integers are immutable."
    },
    {
        "id": 3,
        "question": "What is the output of 3 * 'ab' in Python?",
        "options": {
            "A": "ababab",
            "B": "TypeError",
            "C": "'ab3'",
            "D": "['ab', 'ab', 'ab']"
        },
        "answer": "A",
        "explanation": "Multiplying a string by an integer repeats the string that many times."
    },
    {
        "id": 4,
        "question": "Which built-in function returns the number of items in a collection?",
        "options": {
            "A": "count()",
            "B": "size()",
            "C": "length()",
            "D": "len()"
        },
        "answer": "D",
        "explanation": "len() returns the length of objects such as strings, lists, tuples, or dictionaries."
    },
    {
        "id": 5,
        "question": "How do you insert an element at the end of a list in Python?",
        "options": {
            "A": "list.push(item)",
            "B": "list.add(item)",
            "C": "list.append(item)",
            "D": "list.insert_last(item)"
        },
        "answer": "C",
        "explanation": ".append(item) adds a single element to the end of a Python list."
    },
    {
        "id": 6,
        "question": "Which of the following creates an empty dictionary?",
        "options": {
            "A": "{}",
            "B": "dict()",
            "C": "set()",
            "D": "Both A and B"
        },
        "answer": "D",
        "explanation": "Both {} and dict() initialize an empty dictionary ({} is dict, not set)."
    },
    {
        "id": 7,
        "question": "What is the time complexity of looking up a key in a Python dictionary on average?",
        "options": {
            "A": "O(n)",
            "B": "O(1)",
            "C": "O(log n)",
            "D": "O(n^2)"
        },
        "answer": "B",
        "explanation": "Python dictionaries use hash tables, providing average O(1) time complexity."
    },
    {
        "id": 8,
        "question": "What will `bool('False')` evaluate to in Python?",
        "options": {
            "A": "False",
            "B": "True",
            "C": "None",
            "D": "ValueError"
        },
        "answer": "B",
        "explanation": "Any non-empty string in Python evaluates to True in boolean context."
    }
]


def display_question(q_data: Dict[str, Any], current_num: int, total_num: int) -> None:
    """Print question prompt and multiple choice options."""
    print("\n" + "-" * 60)
    print(f"Question {current_num} of {total_num}:")
    print(q_data["question"])
    print("-" * 60)
    for key, option in q_data["options"].items():
        print(f"  [{key}] {option}")


def get_user_choice() -> str:
    """Prompt the user for a valid option (A, B, C, D) or Q to quit."""
    while True:
        choice = input("\nYour answer (A/B/C/D or Q to quit): ").strip().upper()
        if choice in ["A", "B", "C", "D", "Q"]:
            return choice
        print("[!] Invalid input. Please enter A, B, C, D or Q.")


def run_quiz(questions: List[Dict[str, Any]]) -> None:
    """Main loop to administer the quiz, evaluate responses, and generate summary."""
    score = 0
    total = len(questions)
    results: List[Dict[str, Any]] = []

    print("\n" + "=" * 60)
    print("           WELCOME TO THE PYTHON BASICS QUIZ")
    print("=" * 60)
    print(f"Total Questions: {total}")
    print("Each question has 4 options: A, B, C, or D.")
    print("Type your option and press Enter. Let's begin!\n")

    start_time = time.time()

    for idx, q in enumerate(questions, start=1):
        display_question(q, idx, total)
        choice = get_user_choice()

        if choice == "Q":
            print("\n[!] Quiz aborted early by user.")
            total = idx - 1
            break

        is_correct = (choice == q["answer"])
        if is_correct:
            score += 1
            print(f"[✓] Correct! (+1 point)")
        else:
            print(f"[X] Incorrect! Correct answer was [{q['answer']}]: {q['options'][q['answer']]}")

        print(f"    Note: {q['explanation']}")

        results.append({
            "num": idx,
            "question": q["question"],
            "user_answer": choice,
            "user_text": q["options"].get(choice, "Unknown"),
            "correct_answer": q["answer"],
            "correct_text": q["options"][q["answer"]],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    elapsed_time = round(time.time() - start_time, 1)
    display_summary(results, score, total, elapsed_time)


def display_summary(results: List[Dict[str, Any]], score: int, total: int, elapsed_time: float) -> None:
    """Display final detailed performance report."""
    if total == 0:
        print("\nNo questions answered.")
        return

    percentage = (score / total) * 100

    print("\n" + "=" * 60)
    print("                    FINAL QUIZ RESULTS")
    print("=" * 60)
    print(f"Time Taken       : {elapsed_time} seconds")
    print(f"Questions Tested : {total}")
    print(f"Correct Answers  : {score}")
    print(f"Incorrect Answers: {total - score}")
    print(f"Score Percentage : {percentage:.2f}%")

    if percentage >= 85:
        grade = "Excellent! Outstanding mastery of Python basics."
    elif percentage >= 60:
        grade = "Good job! Solid foundation, with room for minor revision."
    elif percentage >= 40:
        grade = "Fair attempt. Keep practicing Python fundamentals."
    else:
        grade = "Needs Improvement. Review the topics and try again!"

    print(f"Assessment       : {grade}")
    print("=" * 60)

    print("\n--- Detailed Answer Breakdown ---")
    for r in results:
        status_icon = "✓" if r["is_correct"] else "X"
        print(f"\nQ{r['num']}. {r['question']}")
        print(f"   Your choice   : [{r['user_answer']}] {r['user_text']} ({status_icon})")
        if not r["is_correct"]:
            print(f"   Correct answer: [{r['correct_answer']}] {r['correct_text']}")
        print(f"   Explanation   : {r['explanation']}")


def main():
    while True:
        run_quiz(QUESTION_BANK)
        retry = input("\nWould you like to retake the quiz? (y/n): ").strip().lower()
        if retry != "y":
            print("\nThanks for taking the quiz! Keep coding!\n")
            break


if __name__ == "__main__":
    main()

