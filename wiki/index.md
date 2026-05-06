# Indice della Wiki

## Cosmologia — com'è fatto il mondo

```dataview
TABLE Priorità, Aggiornato
FROM "wiki/cosmologia"
SORT file.name ASC
```

## Magia — come funziona

```dataview
TABLE Priorità, Aggiornato
FROM "wiki/magia"
SORT file.name ASC
```

## Storia — timeline, eventi, cause

```dataview
TABLE Tipo, Data
FROM "wiki/storia"
SORT file.name ASC
```

## Entità — chi

```dataview
TABLE Tipo, Aggiornato
FROM "wiki/entita"
SORT file.name ASC
```

## Filosofia — framework concettuali

```dataview
TABLE Tipo, Aggiornato
FROM "wiki/filosofia"
SORT file.name ASC
```

## Sintesi

```dataview
LIST
FROM "wiki/sintesi"
```

## Fonti Processate

```dataview
TABLE Tipo, Aggiornato
FROM "wiki/fonti"
SORT file.name ASC
```

## Domande Aperte

**Cosmologia/Magia:**
- Meccanismo di manifestazione: evoluzione accelerata, istantanea, o reimmissione epistemologica? (parzialmente risolto: tutti e tre)
- La retribuzione del dominio funziona ancora dopo la rottura?
- Soglia computazionale per processare i paradossi?
- Data esatta della Riscoperta della Magia? Cosa la innesca?
- La [[quinta-dimensione]] è accessibile o puramente geometrica? È distruttibile?

**Entità:**
- Il Dio dello Spazio è il Mago della Rottura, il Primordiale, o una terza entità?
- Il [[mago-della-rottura]] è ancora cosciente/attivo?
- Quanto tempo perché emerga il [[dio-del-significante]]?
- Le [[divinita]] ritornanti e quelle generate entreranno in conflitto?
- Cosa succede quando TUTTI i buchi ([[crepe]]) sono chiusi?
- Il guscio degli [[dei-monoteisti]] può essere riempito da qualcosa?
- L'obiettivo del [[demiurgo]] è sostituirsi al guscio vuoto del Dio monoteista?

## Statistiche

```dataview
TABLE length(rows) as "Pagine"
FROM "wiki"
WHERE Categoria
GROUP BY Categoria
SORT rows.length DESC
```
