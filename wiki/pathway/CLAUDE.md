# Regole Pathway

## Template

Usa `_templates/pathway.md` per creare pathway.

## Criteri di creazione

1. Esiste una storia che attraversa 3+ nodi
2. L'ordine dei nodi NON è ovvio dalle singole pagine
3. Risponde a una domanda specifica ("perché X?", "come si è arrivati a Y?")

## Formato

```yaml
---
Categoria: pathway
Fonte: '[[fonte]]'
Aggiornato: YYYY-MM-DD
Nodi:
  - '[[nodo-1]]'
  - '[[nodo-2]]'
  - '[[nodo-3]]'
---
```

Sezioni: Trama, Percorso (nodi in ordine con ruolo), Domande a cui risponde, Moduli collegati.

## Cosa rende un buon pathway

- La trama è più della somma dei nodi — l'ordine rivela qualcosa
- I nodi sono in sequenza causale o temporale, non alfabetica
- Ogni nodo ha un ruolo chiaro nella storia (causa, effetto, risposta, conseguenza)
