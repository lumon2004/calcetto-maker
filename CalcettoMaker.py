import json
import os
import time
from itertools import combinations

DATA_FILE = "giocatoriCalcetto.json"
dati = {"giocatori": [], "affinita": []}

ALPHA = 0.7  # Peso del bilanciamento livello (0.7 = 70%)

def wait(seconds):
    time.sleep(seconds)


def input_sicuro(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nRitorno al menu principale.")
        return None


def chiedi_intero(prompt, min_val=None, max_val=None):
    while True:
        risposta = input_sicuro(prompt)
        if risposta is None:
            return None
        risposta = risposta.strip()
        try:
            valore = int(risposta)
        except ValueError:
            print("Valore non valido. Inserisci un numero intero.")
            continue
        if min_val is not None and valore < min_val:
            print(f"Il valore deve essere almeno {min_val}.")
            continue
        if max_val is not None and valore > max_val:
            print(f"Il valore deve essere al massimo {max_val}.")
            continue
        return valore


def seleziona_giocatori(giocatori):
    prompt = f"Inserisci i numeri di esattamente 10 giocatori (1-{len(giocatori)}), separati da spazi: "
    risposta = input_sicuro(prompt)
    if risposta is None:
        return None
    risposta = risposta.strip()
    if not risposta:
        print("Nessun input fornito.")
        return None

    numeri = risposta.split()
    if len(numeri) != 10:
        print("Devi selezionare esattamente 10 giocatori.")
        return None

    selezione = []
    for token in numeri:
        if not token.isdigit():
            print(f"Token non valido: '{token}'. Usa solo numeri interi.")
            return None
        indice = int(token)
        if indice < 1 or indice > len(giocatori):
            print(f"Numero fuori range: {indice}. Deve essere tra 1 e {len(giocatori)}.")
            return None
        if indice in selezione:
            print(f"Numero duplicato: {indice}. Ogni giocatore può essere selezionato una sola volta.")
            return None
        selezione.append(indice)

    return [giocatori[i - 1] for i in selezione]


def main():
    print("Benvenuto al Calcetto Maker!")
    print("Questo programma ti aiuterà a creare due squadre per giocare a calcetto.")

    giocatori = carica()
    print(f"Giocatori caricati: {len(giocatori)}")

    try:
        while True:
            print("\nScegli un'opzione:")
            print("1. Mostra giocatori")
            print("2. Aggiungi giocatore")
            print("3. Formula squadre")
            print("4. Modifica giocatore")
            print("5. Elimina giocatore")
            print("6. Esci")

            scelta = input_sicuro("> ")
            if scelta is None:
                continue
            scelta = scelta.strip()

            if scelta == "1":
                mostra(giocatori)
            elif scelta == "2":
                aggiungi(giocatori)
            elif scelta == "3":
                formula_squadre(giocatori)
            elif scelta == "4":
                modifica_giocatore(giocatori)
            elif scelta == "5":
                elimina_giocatore(giocatori)
            elif scelta == "6":
                print("Arrivederci!")
                break
            else:
                print("Opzione non valida. Riprova.")
    except KeyboardInterrupt:
        print("\nInterruzione ricevuta. Arrivederci!")


def formula_squadre(giocatori):
    if len(giocatori) < 10:
        print("Non ci sono abbastanza giocatori per formare due squadre (minimo 10).")
        return
    elif len(giocatori) > 10:
        print("Ci sono più di 10 giocatori. Chi gioca questa volta?")
        mostra(giocatori)
        giocatoriCorrenti = seleziona_giocatori(giocatori)
        if giocatoriCorrenti is None:
            return
    else:
        giocatoriCorrenti = giocatori

    esegui_algoritmo(giocatoriCorrenti)


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
    for aff in dati.get("affinita", []):
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


def get_affinita(giocatore1, giocatore2):
    for coppia in dati["affinita"]:
        if "a" in coppia and "b" in coppia:
            if (coppia["a"] == giocatore1 and coppia["b"] == giocatore2) or \
               (coppia["a"] == giocatore2 and coppia["b"] == giocatore1):
                return coppia["valore"]
    return None


def set_affinita(giocatore1, giocatore2, valore):
    for coppia in dati["affinita"]:
        if "a" in coppia and "b" in coppia:
            if (coppia["a"] == giocatore1 and coppia["b"] == giocatore2) or \
               (coppia["a"] == giocatore2 and coppia["b"] == giocatore1):
                coppia["valore"] = valore
                return
    dati["affinita"].append({"a": giocatore1, "b": giocatore2, "valore": valore})


def carica():
    global dati
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dati = json.load(f)
    except json.JSONDecodeError:
        print(f"Impossibile leggere '{DATA_FILE}': file JSON non valido.")
        dati = {"giocatori": [], "affinita": []}
        return []
    except OSError as exc:
        print(f"Errore di accesso a '{DATA_FILE}': {exc}")
        return []

    if not isinstance(dati, dict):
        print(f"Dati non validi in '{DATA_FILE}'.")
        dati = {"giocatori": [], "affinita": []}
        return []

    if not isinstance(dati.get("giocatori"), list):
        print("La lista dei giocatori non è valida. Viene usata una lista vuota.")
        dati["giocatori"] = []

    if not isinstance(dati.get("affinita"), list):
        dati["affinita"] = []

    return dati["giocatori"]


def salva(giocatori):
    global dati
    dati["giocatori"] = giocatori
    if not isinstance(dati.get("affinita"), list):
        dati["affinita"] = []
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=4, ensure_ascii=False)
    except OSError as exc:
        print(f"Impossibile salvare i dati in '{DATA_FILE}': {exc}")


def mostra(giocatori):
    if not giocatori:
        print("Nessun giocatore trovato.")
        return
    for i, c in enumerate(giocatori, 1):
        nome = c.get('nome', 'Sconosciuto') if isinstance(c, dict) else 'Sconosciuto'
        livello = c.get('livello', '?') if isinstance(c, dict) else '?'
        print(f"{i}. {nome} (Livello: {livello})")


def aggiungi(giocatori):
    while True:
        nome = input_sicuro("Inserisci il nome del giocatore: ")
        if nome is None:
            return
        nome = nome.strip()
        if not nome:
            print("Il nome non può essere vuoto.")
            continue
        if any(isinstance(g, dict) and g.get('nome') == nome for g in giocatori):
            print("Esiste già un giocatore con questo nome. Scegli un nome diverso.")
            continue
        break

    livello = chiedi_intero("Inserisci il livello del giocatore (1-10): ", 1, 10)
    if livello is None:
        return
    nuovo_giocatore = {"nome": nome, "livello": livello}
    for g in giocatori:
        if not isinstance(g, dict) or 'nome' not in g:
            continue
        aff = chiedi_intero(f"Inserisci l'affinità tra {nome} e {g['nome']} (0-5): ", 0, 5)
        if aff is None:
            return
        set_affinita(nome, g["nome"], aff)

    giocatori.append(nuovo_giocatore)
    salva(giocatori)
    print("Giocatore aggiunto con successo!")


def scegli_giocatore(giocatori, descrizione="giocatore"):
    if not giocatori:
        print("Nessun giocatore disponibile.")
        return None
    mostra(giocatori)
    indice = chiedi_intero(f"Seleziona il numero del {descrizione} (1-{len(giocatori)}): ", 1, len(giocatori))
    if indice is None:
        return None
    return indice - 1


def chiedi_intero_opzionale(prompt, min_val=None, max_val=None, default=None):
    while True:
        risposta = input_sicuro(prompt)
        if risposta is None:
            return None
        risposta = risposta.strip()
        if risposta == "":
            return default
        try:
            valore = int(risposta)
        except ValueError:
            print("Valore non valido. Inserisci un numero intero o lascia vuoto per mantenere il valore corrente.")
            continue
        if min_val is not None and valore < min_val:
            print(f"Il valore deve essere almeno {min_val}.")
            continue
        if max_val is not None and valore > max_val:
            print(f"Il valore deve essere al massimo {max_val}.")
            continue
        return valore


def modifica_nome_affinita(vecchio_nome, nuovo_nome):
    for coppia in dati.get("affinita", []):
        if not isinstance(coppia, dict):
            continue
        if coppia.get("a") == vecchio_nome:
            coppia["a"] = nuovo_nome
        if coppia.get("b") == vecchio_nome:
            coppia["b"] = nuovo_nome


def modifica_giocatore(giocatori):
    if not giocatori:
        print("Nessun giocatore da modificare.")
        return

    indice = scegli_giocatore(giocatori, "giocatore da modificare")
    if indice is None:
        return

    giocatore = giocatori[indice]
    nome_vecchio = giocatore.get('nome', '')
    livello_vecchio = giocatore.get('livello', 0)

    print(f"Modifica giocatore {nome_vecchio} (Livello: {livello_vecchio})")
    nuovo_nome = input_sicuro("Nuovo nome (lascia vuoto per mantenere): ")
    if nuovo_nome is None:
        return
    nuovo_nome = nuovo_nome.strip()
    if nuovo_nome:
        if any(isinstance(g, dict) and g.get('nome') == nuovo_nome for i, g in enumerate(giocatori) if i != indice):
            print("Esiste già un giocatore con questo nome. Modifica annullata.")
            return
        giocatore['nome'] = nuovo_nome
        modifica_nome_affinita(nome_vecchio, nuovo_nome)

    nuovo_livello = chiedi_intero_opzionale("Nuovo livello (1-10, lascia vuoto per mantenere): ", 1, 10, default=livello_vecchio)
    if nuovo_livello is None:
        return
    if nuovo_livello is None:
        nuovo_livello = livello_vecchio
    giocatore['livello'] = nuovo_livello

    salva(giocatori)
    print("Giocatore modificato con successo!")


def elimina_giocatore(giocatori):
    if not giocatori:
        print("Nessun giocatore da eliminare.")
        return

    indice = scegli_giocatore(giocatori, "giocatore da eliminare")
    if indice is None:
        return

    giocatore = giocatori[indice]
    nome = giocatore.get('nome', '')
    conferma = input_sicuro(f"Vuoi davvero eliminare {nome}? (s/n): ")
    if conferma is None:
        return
    conferma = conferma.strip().lower()
    if conferma not in ('s', 'si'):
        print("Eliminazione annullata.")
        return

    del giocatori[indice]
    dati["affinita"] = [c for c in dati.get("affinita", []) if not (isinstance(c, dict) and (c.get("a") == nome or c.get("b") == nome))]
    salva(giocatori)
    print("Giocatore eliminato con successo.")


if __name__ == "__main__":
    main()
