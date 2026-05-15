# ⚽ Pitch Picker

A terminal tool to automatically split a group of friends into **two balanced teams** for a five-a-side football match, taking into account each player's skill level and the affinities between them.

## How it works

The algorithm assigns players to teams by trying to:
1. **Balance the total skill level** of both teams
2. **Maximise affinities** within each team (teammates who know each other well play better together)

## Requirements

- Python 3.8 or higher
- No external libraries required (standard library only)

## Installation and setup

1. Clone the repository: ```git clone https://github.com/lumon2004/calcetto-maker.git```,
```cd calcetto-maker```
2. Copy the example file and rename it: ```cp players.example.json players.json```
3. Start the program: ```python main.py```

## 🐳 Running with Docker

```bash
docker build -t pitch-picker .
docker run -it -v $(pwd)/players.json:/app/players.json pitch-picker
```

## The players file (JSON)

The program reads data from `players.json`. You can create it manually from the example (`players.example.json`) or use the **"Add player"** option directly from the program menu.

### File structure

```json
{
    "players": [
        {"name": "PlayerName", "level": 7}
    ],
    "affinities": [
        {"a": "Player1", "b": "Player2", "value": 4}
    ]
}
```

- **`level`**: from 1 (beginner) to 10 (expert)
- **`value` (affinity)**: from 0 (they hate each other) to 5 (best friends)

## Usage
```
1. Show players   → lists all saved players
2. Add player     → adds a new player and sets affinities
3. Build teams    → generates the two balanced teams
4. Edit player    → updates an existing player's name or level
5. Delete player  → removes a player
6. Exit
```

If you have more than 10 registered players, the program will ask you to select who is playing that evening.

## License

MIT License — do whatever you want with the code.