import json
import os
import time

DATA_FILE = "giocatoriCalcetto.json"
dati = {"giocatori": [], "affinita": []} # Variabili globali per giocatori e affinità

def wait(seconds):
    time.sleep(seconds)

def main():
    # Testo di avvio
    print("Benvenuto al Calcetto Maker!")
    print("Questo programma ti aiuterà a creare due squadre per giocare a calcetto.")

    giocatori = carica()
    print(f"Giocatori caricati: {len(giocatori)}")

    while True:
        print("\nScegli un'opzione:")
        print("1. Mostra giocatori")
        print("2. Aggiungi giocatore")
        print("3. Formula squadre")
        print("4. Esci")

        scelta = input("> ").strip()

        if scelta == "1":
            mostra(giocatori)
        elif scelta == "2":
            aggiungi(giocatori)
        elif scelta == "3":
            formula_squadre(giocatori)
        elif scelta == "4":
            print("Arrivederci!")
            break
        else:
            print("Opzione non valida. Riprova.")


def formula_squadre(giocatori):
    if len(giocatori) < 10:
        print("Non ci sono abbastanza giocatori per formare due squadre (minimo 10).")
        return
    elif len(giocatori) > 10:
        print("Ci sono più di 10 giocatori. Chi gioca questa volta?")
        mostra(giocatori)
        giocatoriCorrenti = [giocatori[int(i)-1] for i in input("Inserisci i numeri dei giocatori (separati da spazi): ").strip().split()]
    else: # giocatori esattamente 10
        giocatoriCorrenti = giocatori

    esegui_algoritmo(giocatoriCorrenti)

def esegui_algoritmo(giocatori):
    if len(giocatori) != 10:
        print("Il numero di giocatori non è esatto (10).")
        return

    # Costruisci dizionario affinità
    affinita_dict = {g['nome']: {} for g in giocatori}
    for aff in dati["affinita"]:
        a, b, val = aff.get('a'), aff.get('b'), aff.get('valore')
        if a in affinita_dict and b in affinita_dict:
            affinita_dict[a][b] = val
            affinita_dict[b][a] = val

    # Ordina per livello decrescente
    ordinati = sorted(giocatori, key=lambda x: x['livello'], reverse=True)
    
    squadra1, squadra2 = [], []

    for g in ordinati:
        nome = g['nome']
        livello_s1 = sum(p['livello'] for p in squadra1)
        livello_s2 = sum(p['livello'] for p in squadra2)
        
        # Bonus affinità: quanti compagni già assegnati conosco bene?
        aff_s1 = sum(affinita_dict[nome].get(p['nome'], 0) for p in squadra1)
        aff_s2 = sum(affinita_dict[nome].get(p['nome'], 0) for p in squadra2)

        # Punteggio: voglio squadra con livello basso E affinità alta
        # Peso affinità scalato per non dominare il bilanciamento
        score_s1 = livello_s1 - aff_s1 * 0.3
        score_s2 = livello_s2 - aff_s2 * 0.3

        if len(squadra1) >= 5:
            squadra2.append(g)
        elif len(squadra2) >= 5:
            squadra1.append(g)
        elif score_s1 <= score_s2:
            squadra1.append(g)
        else:
            squadra2.append(g)

    # Stampa
    for nome_squadra, squadra in [("Squadra 1", squadra1), ("Squadra 2", squadra2)]:
        print(f"\n{nome_squadra}:")
        for p in squadra:
            print(f"  {p['nome']} (Livello: {p['livello']})")
        print(f"  Livello totale: {sum(p['livello'] for p in squadra)}")

def get_affinita(giocatore1, giocatore2):
    for coppia in dati["affinita"]:
        if "a" in coppia and "b" in coppia:
            if (coppia["a"] == giocatore1 and coppia["b"] == giocatore2) or \
               (coppia["a"] == giocatore2 and coppia["b"] == giocatore1):
                return coppia["valore"]
    return None  # non trovato

def set_affinita(giocatore1, giocatore2, valore):
    for coppia in dati["affinita"]:
        if "a" in coppia and "b" in coppia:
            if (coppia["a"] == giocatore1 and coppia["b"] == giocatore2) or \
               (coppia["a"] == giocatore2 and coppia["b"] == giocatore1):
                coppia["valore"] = valore
                return
    # Se non esiste, aggiungila
    dati["affinita"].append({"a": giocatore1, "b": giocatore2, "valore": valore})

def carica():
    global dati
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dati = json.load(f)
        return dati["giocatori"]

def salva(giocatori):
    global dati
    dati["giocatori"] = giocatori
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=4, ensure_ascii=False)

def mostra(giocatori):
    if not giocatori:
        print("Nessun giocatore trovato.")
        return
    for i, c in enumerate(giocatori, 1):
        print(f"{i}. {c['nome']} (Livello: {c['livello']})")

def aggiungi(giocatori):
    nome = input("Inserisci il nome del giocatore: ").strip()
    livello = int(input("Inserisci il livello del giocatore (1-10): "))
    giocatori.append({"nome": nome, "livello": livello})
    # aggiungi affinità con giocatori esistenti
    for g in giocatori[:-1]:  # escludi l'ultimo giocatore
        aff = int(input(f"Inserisci l'affinità tra {nome} e {g['nome']} (0-5): "))
        set_affinita(nome, g["nome"], aff)
    salva(giocatori)
    print("Giocatore aggiunto con successo!")

if __name__ == "__main__":
    main()