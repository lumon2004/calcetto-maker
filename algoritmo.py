from itertools import combinations
from config import ALPHA
import data

def affinita_interna(squadra, affinita_dict):
    """Somma le affinità tra tutte le coppie interne di una squadra."""
    totale = 0
    nomi = [g['nome'] for g in squadra]
    for i in range(len(nomi)):
        for j in range(i + 1, len(nomi)):
            totale += affinita_dict.get(nomi[i], {}).get(nomi[j], 0)
    return totale

def esegui_algoritmo(giocatori):
    if len(giocatori) != 10:
        print("Il numero di giocatori non è esatto (10).")
        return

    for g in giocatori:
        if not isinstance(g, dict) or 'nome' not in g or 'livello' not in g:
            print("Dati giocatore non validi. Controlla il contenuto di giocatori.")
            return
        if not isinstance(g['nome'], str) or not g['nome'].strip():
            print("Ogni giocatore deve avere un nome valido.")
            return
        if not isinstance(g['livello'], int) or g['livello'] < 1:
            print("Ogni giocatore deve avere un livello intero valido.")
            return

    affinita_dict = {g['nome']: {} for g in giocatori}
    for aff in data.dati.get("affinita", []):
        if not isinstance(aff, dict):
            continue
        a = aff.get('a')
        b = aff.get('b')
        val = aff.get('valore', 0)
        if a in affinita_dict and b in affinita_dict:
            try:
                valore = int(val)
            except (TypeError, ValueError):
                valore = 0
            affinita_dict[a][b] = valore
            affinita_dict[b][a] = valore

    print("DEBUG affinita_dict:", affinita_dict)
    livello_max = sum(sorted([g['livello'] for g in giocatori], reverse=True)[:5])
    delta_livello_max = livello_max if livello_max > 0 else 1
    delta_affinita_max = 5 * 10

    migliore_score = float('inf')
    migliore_squadra1 = None
    migliore_squadra2 = None

    indici = list(range(10))
    for combo in combinations(indici, 5):
        squadra1 = [giocatori[i] for i in combo]
        squadra2 = [giocatori[i] for i in indici if i not in combo]

        livello_s1 = sum(g['livello'] for g in squadra1)
        livello_s2 = sum(g['livello'] for g in squadra2)
        aff_s1 = affinita_interna(squadra1, affinita_dict)
        aff_s2 = affinita_interna(squadra2, affinita_dict)

        delta_livello = abs(livello_s1 - livello_s2)
        delta_affinita = abs(aff_s1 - aff_s2)

        delta_livello_norm = delta_livello / delta_livello_max
        delta_affinita_norm = delta_affinita / delta_affinita_max

        score = ALPHA * delta_livello_norm + (1 - ALPHA) * delta_affinita_norm

        if score < migliore_score:
            migliore_score = score
            migliore_squadra1 = squadra1
            migliore_squadra2 = squadra2

    if migliore_squadra1 is None or migliore_squadra2 is None:
        print("Impossibile trovare una combinazione valida.")
        return

    for nome_squadra, squadra in [("Squadra 1", migliore_squadra1), ("Squadra 2", migliore_squadra2)]:
        print(f"\n{nome_squadra}:")
        for p in squadra:
            nome = p.get('nome', 'Sconosciuto')
            livello = p.get('livello', 0)
            print(f"  {nome} (Livello: {livello})")
        livello_tot = sum(p.get('livello', 0) for p in squadra)
        aff_tot = affinita_interna(squadra, affinita_dict)
        print(f"  Livello totale: {livello_tot}")
        print(f"  Affinità interna: {aff_tot}")

    s1_liv = sum(p.get('livello', 0) for p in migliore_squadra1)
    s2_liv = sum(p.get('livello', 0) for p in migliore_squadra2)
    print(f"\nSquilibrio livello: {abs(s1_liv - s2_liv)}")
    print(f"Score di squilibrio finale: {migliore_score:.4f} (più basso = più equilibrato)")
