from data import dati, salva, get_affinita, set_affinita, modifica_nome_affinita
from ui import input_sicuro, chiedi_intero, chiedi_intero_opzionale, seleziona_giocatori

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
