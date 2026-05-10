import time

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
