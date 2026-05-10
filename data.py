import json, os
from config import DATA_FILE

dati = {"giocatori": [], "affinita": []}

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

def modifica_nome_affinita(vecchio_nome, nuovo_nome):
    for coppia in dati.get("affinita", []):
        if not isinstance(coppia, dict):
            continue
        if coppia.get("a") == vecchio_nome:
            coppia["a"] = nuovo_nome
        if coppia.get("b") == vecchio_nome:
            coppia["b"] = nuovo_nome
