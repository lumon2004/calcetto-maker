import json, os
from config import DATA_FILE

dataset = {"players": [], "affinities": []}

def load():
    global dataset
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    except json.JSONDecodeError:
        print(f"Unable to read '{DATA_FILE}': invalid JSON file.")
        dataset = {"players": [], "affinities": []}
        return []
    except OSError as exc:
        print(f"Error accessing '{DATA_FILE}': {exc}")
        return []

    if not isinstance(dataset, dict):
        print(f"Invalid data in '{DATA_FILE}'.")
        dataset = {"players": [], "affinities": []}
        return []

    if not isinstance(dataset.get("players"), list):
        print("The players list is invalid. Using an empty list.")
        dataset["players"] = []

    if not isinstance(dataset.get("affinities"), list):
        dataset["affinities"] = []

    return dataset["players"]

def save(players):
    global dataset
    dataset["players"] = players
    if not isinstance(dataset.get("affinities"), list):
        dataset["affinities"] = []
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=4, ensure_ascii=False)
    except OSError as exc:
        print(f"Unable to save data to '{DATA_FILE}': {exc}")

def get_affinity(player1, player2):
    for pair in dataset["affinities"]:
        if "a" in pair and "b" in pair:
            if (pair["a"] == player1 and pair["b"] == player2) or \
               (pair["a"] == player2 and pair["b"] == player1):
                return pair["value"]
    return None

def set_affinity(player1, player2, value):
    for pair in dataset["affinities"]:
        if "a" in pair and "b" in pair:
            if (pair["a"] == player1 and pair["b"] == player2) or \
               (pair["a"] == player2 and pair["b"] == player1):
                pair["value"] = value
                return
    dataset["affinities"].append({"a": player1, "b": player2, "value": value})

def update_affinity_name(old_name, new_name):
    for pair in dataset.get("affinities", []):
        if not isinstance(pair, dict):
            continue
        if pair.get("a") == old_name:
            pair["a"] = new_name
        if pair.get("b") == old_name:
            pair["b"] = new_name
