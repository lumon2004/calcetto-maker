from itertools import combinations
from config import ALPHA
import data

def internal_affinity(team, affinity_dict):
    """Sums the affinities between all internal pairs of a team."""
    total = 0
    names = [p['name'] for p in team]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            total += affinity_dict.get(names[i], {}).get(names[j], 0)
    return total

def run_algorithm(players):
    if len(players) != 10:
        print("The number of players is not exactly 10.")
        return

    for p in players:
        if not isinstance(p, dict) or 'name' not in p or 'level' not in p:
            print("Invalid player data. Check the players list.")
            return
        if not isinstance(p['name'], str) or not p['name'].strip():
            print("Every player must have a valid name.")
            return
        if not isinstance(p['level'], int) or p['level'] < 1:
            print("Every player must have a valid integer level.")
            return

    affinity_dict = {p['name']: {} for p in players}
    for aff in data.dataset.get("affinities", []):
        if not isinstance(aff, dict):
            continue
        a = aff.get('a')
        b = aff.get('b')
        val = aff.get('value', 0)
        if a in affinity_dict and b in affinity_dict:
            try:
                value = int(val)
            except (TypeError, ValueError):
                value = 0
            affinity_dict[a][b] = value
            affinity_dict[b][a] = value

    max_level = sum(sorted([p['level'] for p in players], reverse=True)[:5])
    max_level_delta = max_level if max_level > 0 else 1
    max_affinity_delta = 5 * 10

    best_score = float('inf')
    best_team1 = None
    best_team2 = None

    indices = list(range(10))
    for combo in combinations(indices, 5):
        team1 = [players[i] for i in combo]
        team2 = [players[i] for i in indices if i not in combo]

        level_t1 = sum(p['level'] for p in team1)
        level_t2 = sum(p['level'] for p in team2)
        aff_t1 = internal_affinity(team1, affinity_dict)
        aff_t2 = internal_affinity(team2, affinity_dict)

        delta_level = abs(level_t1 - level_t2)
        delta_affinity = abs(aff_t1 - aff_t2)

        delta_level_norm = delta_level / max_level_delta
        delta_affinity_norm = delta_affinity / max_affinity_delta

        score = ALPHA * delta_level_norm + (1 - ALPHA) * delta_affinity_norm

        if score < best_score:
            best_score = score
            best_team1 = team1
            best_team2 = team2

    if best_team1 is None or best_team2 is None:
        print("Unable to find a valid combination.")
        return

    for team_name, team in [("Team 1", best_team1), ("Team 2", best_team2)]:
        print(f"\n{team_name}:")
        for p in team:
            name = p.get('name', 'Unknown')
            level = p.get('level', 0)
            print(f"  {name} (Level: {level})")
        total_level = sum(p.get('level', 0) for p in team)
        total_aff = internal_affinity(team, affinity_dict)
        print(f"  Total level: {total_level}")
        print(f"  Internal affinity: {total_aff}")

    t1_level = sum(p.get('level', 0) for p in best_team1)
    t2_level = sum(p.get('level', 0) for p in best_team2)
    print(f"\nLevel imbalance: {abs(t1_level - t2_level)}")
    print(f"Final imbalance score: {best_score:.4f} (lower = more balanced)")
