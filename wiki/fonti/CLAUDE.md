# Regole Ingest

## Template

Usa sempre `_templates/fonte.md` per creare pagine in `wiki/fonti/`.

## Ordine creazione

1. Pagina fonte (`wiki/fonti/`)
2. Pagine entità (`wiki/entita/`)
3. Pagine cosmologia/magia/storia/filosofia
4. Sintesi solo se cambia la visione d'insieme
5. Aggiorna `wiki/index.md` domande aperte
6. Aggiorna `wiki/log.md` (append-only)

## Protocollo Deprecazione

Quando un trascritto contraddice un concetto:
1. NON eliminare la pagina esistente
2. Aggiorna YAML: `Stato: Deprecato`, `Sostituito_Da: '[[nuovo-concetto]]'`
3. Aggiungi avviso in cima
4. Crea redirect se il vecchio nome è linkato altrove

## Formato Log

```
## [YYYY-MM-DD] ingest | Titolo Sorgente

**Pagine create:** [[...]]
**Pagine aggiornate:** [[...]] (cosa è cambiato)
**Raffinamenti:** ...
**File:** raw/Trascritto_X.md
```

## Segnalazione Struttura

Alla fine dell'ingest, segnala (NON modificare):
- Moduli toccati
- Possibili nuovi pathway
