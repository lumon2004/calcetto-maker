from data import carica
from ui import input_sicuro, seleziona_giocatori
from algoritmo import esegui_algoritmo
from giocatori import mostra, aggiungi, modifica_giocatore, elimina_giocatore

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

if __name__ == "__main__":
    main()