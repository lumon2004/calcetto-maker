from data import dataset, save, get_affinity, set_affinity, update_affinity_name
from ui import safe_input, ask_integer, ask_integer_optional, select_players

def show(players):
    if not players:
        print("No players found.")
        return
    for i, p in enumerate(players, 1):
        name = p.get('name', 'Unknown') if isinstance(p, dict) else 'Unknown'
        level = p.get('level', '?') if isinstance(p, dict) else '?'
        print(f"{i}. {name} (Level: {level})")

def add(players):
    while True:
        name = safe_input("Enter the player's name: ")
        if name is None:
            return
        name = name.strip()
        if not name:
            print("Name cannot be empty.")
            continue
        if any(isinstance(p, dict) and p.get('name') == name for p in players):
            print("A player with this name already exists. Choose a different name.")
            continue
        break

    level = ask_integer("Enter the player's level (1-10): ", 1, 10)
    if level is None:
        return
    new_player = {"name": name, "level": level}
    for p in players:
        if not isinstance(p, dict) or 'name' not in p:
            continue
        aff = ask_integer(f"Enter the affinity between {name} and {p['name']} (0-5): ", 0, 5)
        if aff is None:
            return
        set_affinity(name, p["name"], aff)

    players.append(new_player)
    save(players)
    print("Player added successfully!")

def pick_player(players, description="player"):
    if not players:
        print("No players available.")
        return None
    show(players)
    index = ask_integer(f"Select the number of the {description} (1-{len(players)}): ", 1, len(players))
    if index is None:
        return None
    return index - 1

def edit_player(players):
    if not players:
        print("No players to edit.")
        return

    index = pick_player(players, "player to edit")
    if index is None:
        return

    player = players[index]
    old_name = player.get('name', '')
    old_level = player.get('level', 0)

    print(f"Editing player {old_name} (Level: {old_level})")
    new_name = safe_input("New name (leave blank to keep current): ")
    if new_name is None:
        return
    new_name = new_name.strip()
    if new_name:
        if any(isinstance(p, dict) and p.get('name') == new_name for i, p in enumerate(players) if i != index):
            print("A player with this name already exists. Edit cancelled.")
            return
        player['name'] = new_name
        update_affinity_name(old_name, new_name)

    new_level = ask_integer_optional("New level (1-10, leave blank to keep current): ", 1, 10, default=old_level)
    if new_level is None:
        return
    if new_level is None:
        new_level = old_level
    player['level'] = new_level

    save(players)
    print("Player updated successfully!")

def delete_player(players):
    if not players:
        print("No players to delete.")
        return

    index = pick_player(players, "player to delete")
    if index is None:
        return

    player = players[index]
    name = player.get('name', '')
    confirm = safe_input(f"Are you sure you want to delete {name}? (y/n): ")
    if confirm is None:
        return
    confirm = confirm.strip().lower()
    if confirm not in ('y', 'yes'):
        print("Deletion cancelled.")
        return

    del players[index]
    dataset["affinities"] = [c for c in dataset.get("affinities", []) if not (isinstance(c, dict) and (c.get("a") == name or c.get("b") == name))]
    save(players)
    print("Player deleted successfully.")
