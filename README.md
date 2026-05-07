# ⚽ CalcettoMaker

Un tool da terminale per dividere automaticamente un gruppo di amici in **due squadre equilibrate** per una partita di calcetto, tenendo conto del livello di ogni giocatore e delle affinità tra di loro.

## Come funziona

L'algoritmo assegna i giocatori alle squadre cercando di:
1. **Bilanciare il livello totale** delle due squadre
2. **Massimizzare le affinità** all'interno di ogni squadra (i compagni che si conoscono bene giocano meglio insieme)

## Requisiti

- Python 3.8 o superiore
- Nessuna libreria esterna richiesta (solo librerie standard)

## Installazione e avvio

1. Clona la repository: ```git clone https://github.com/lumon2004/calcetto-maker.git```,
```cd calcetto-maker```
2. Copia il file di esempio e rinominalo: ```cp giocatoriCalcetto.example.json giocatoriCalcetto.json```
3. Avvia il programma: ```python CalcettoMaker.py```

## Il file dei giocatori (JSON)

Il programma legge i dati da `giocatoriCalcetto.json`. Puoi crearlo manualmente partendo dall'esempio (`giocatoriCalcetto.example.json`) oppure usare l'opzione **"Aggiungi giocatore"** direttamente dal menu del programma.

### Struttura del file

```json
{
    "giocatori": [
        {"nome": "NomeGiocatore", "livello": 7}
    ],
    "affinita": [
        {"a": "Giocatore1", "b": "Giocatore2", "valore": 4}
    ]
}
```

- **`livello`**: da 1 (scarso) a 10 (fenomeno)
- **`valore` affinità**: da 0 (si detestano) a 5 (migliori amici)

## Utilizzo
```
1. Mostra giocatori → lista tutti i giocatori salvati
2. Aggiungi giocatore → aggiunge un nuovo giocatore e imposta le affinità
3. Formula squadre → genera le due squadre bilanciate
4. Esci
```

Se hai più di 10 giocatori registrati, il programma ti chiederà di selezionare chi gioca quella sera.

## Licenza

MIT License — fai quello che vuoi con il codice.