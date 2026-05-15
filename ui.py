import time

def wait(seconds):
    time.sleep(seconds)

def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nReturning to main menu.")
        return None

def ask_integer(prompt, min_val=None, max_val=None):
    while True:
        answer = safe_input(prompt)
        if answer is None:
            return None
        answer = answer.strip()
        try:
            value = int(answer)
        except ValueError:
            print("Invalid value. Please enter an integer.")
            continue
        if min_val is not None and value < min_val:
            print(f"Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Value must be at most {max_val}.")
            continue
        return value

def ask_integer_optional(prompt, min_val=None, max_val=None, default=None):
    while True:
        answer = safe_input(prompt)
        if answer is None:
            return None
        answer = answer.strip()
        if answer == "":
            return default
        try:
            value = int(answer)
        except ValueError:
            print("Invalid value. Please enter an integer or leave blank to keep the current value.")
            continue
        if min_val is not None and value < min_val:
            print(f"Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Value must be at most {max_val}.")
            continue
        return value

def select_players(players):
    prompt = f"Enter exactly 10 player numbers (1-{len(players)}), separated by spaces: "
    answer = safe_input(prompt)
    if answer is None:
        return None
    answer = answer.strip()
    if not answer:
        print("No input provided.")
        return None

    numbers = answer.split()
    if len(numbers) != 10:
        print("You must select exactly 10 players.")
        return None

    selection = []
    for token in numbers:
        if not token.isdigit():
            print(f"Invalid token: '{token}'. Use only integers.")
            return None
        index = int(token)
        if index < 1 or index > len(players):
            print(f"Number out of range: {index}. Must be between 1 and {len(players)}.")
            return None
        if index in selection:
            print(f"Duplicate number: {index}. Each player can only be selected once.")
            return None
        selection.append(index)

    return [players[i - 1] for i in selection]
