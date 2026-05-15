from data import load
from ui import safe_input, select_players
from algorithm import run_algorithm
from players import show, add, edit_player, delete_player

def main():
    print("Welcome to Pitch Picker!")
    print("This program will help you create two balanced teams for a five-a-side match.")

    players = load()
    print(f"Players loaded: {len(players)}")

    try:
        while True:
            print("\nChoose an option:")
            print("1. Show players")
            print("2. Add player")
            print("3. Build teams")
            print("4. Edit player")
            print("5. Delete player")
            print("6. Exit")

            choice = safe_input("> ")
            if choice is None:
                continue
            choice = choice.strip()

            if choice == "1":
                show(players)
            elif choice == "2":
                add(players)
            elif choice == "3":
                build_teams(players)
            elif choice == "4":
                edit_player(players)
            elif choice == "5":
                delete_player(players)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
    except KeyboardInterrupt:
        print("\nInterruption received. Goodbye!")

def build_teams(players):
    if len(players) < 10:
        print("Not enough players to form two teams (minimum 10).")
        return
    elif len(players) > 10:
        print("There are more than 10 players. Who is playing tonight?")
        show(players)
        current_players = select_players(players)
        if current_players is None:
            return
    else:
        current_players = players

    run_algorithm(current_players)

if __name__ == "__main__":
    main()