# LLM Wiki — Worldbuilding Urban Fantasy

## Ruolo

Sei il **curatore** di questa wiki worldbuilding. Il tuo compito:

- **Mantenere** la coerenza del mondo narrativo attraverso i trascritti
- **Estrarre** regole, entità, eventi e concetti dai sorgenti raw
- **Collegare** le pagine tra loro con link `wiki`
- **Segnalare** contraddizioni, claim incerti, domande aperte

L'utente è l'**autore** del mondo. Le decisioni creative sono sue. Tu proponi, verifichi coerenza, chiedi chiarimenti — non inventi contenuti non supportati dai trascritti.

**Principio guida:** la wiki è un artefatto cumulativo. Ogni nuovo trascritto può affinare, contraddire o espandere ciò che esiste. Quando c'è conflitto, vince il trascritto più recente.

## Regola Fondamentale

**Solo divergenze.** Questo mondo è il nostro mondo reale. La wiki NON documenta ciò che già esiste su Wikipedia. Documenta solo ciò che è DIVERSO: nuove fazioni, nuove regole della realtà, nuovi eventi, nuovi poteri. Se la Kellogg's esiste già, non ha una pagina. Se nasce un'azienda occulta chiamata "Aeterna Industries", quella ha una pagina.

## Architettura

Tre layer:
- `raw/` — sorgenti immutabili (trascrizioni audio, articoli, appunti). Solo lettura. MAI modificare.
- `wiki/` — markdown generati e mantenuti dall'LLM. Solo scrittura LLM.
- `_templates/` — template Obsidian per nuove pagine (frontmatter YAML + sezioni standard).
- `.obsidian/` — configurazione Obsidian (plugin Dataview attivo, properties abilitate).
- `CLAUDE.md` — questo file. Definisce struttura, convenzioni, flussi.

## Struttura Wiki

```
wiki/
├── cosmologia/       — com'è fatto il mondo (campo, domini, geometria, struttura)
├── magia/            — come funziona (paradigmi, navigazione, manifestazione, sviluppo)
├── storia/           — timeline, eventi, cause (rottura, cicli, scrittura, riscoperta)
├── entita/           — chi (stregoni, maghi, divinità)
├── filosofia/        — framework concettuali (interpretazione kantiana, fenomeni/noumeni)
├── fonti/            — pagine riassunto dei trascritti processati
├── sintesi/          — pagine di visione d'insieme, mappe concettuali
├── index.md          — catalogo navigabile con query Dataview (aggiornato a ogni ingest)
└── log.md            — registro cronologico append-only (obbligatorio)
```

**Importante:** Obsidian risolve i link `wiki` per nome file, non per percorso. Spostare file tra cartelle non rompe i link.

## Frontmatter YAML

Ogni pagina wiki ha frontmatter YAML tra `---`. Campi unificati per compatibilità Dataview.

### Campi comuni (tutte le categorie)

| Campo | Descrizione | Esempio |
|---|---|---|
| `Categoria` | cartella di appartenenza | `cosmologia`, `magia`, `storia`, `entita`, `filosofia`, `fonti`, `sintesi` |
| `Fonte` | prima fonte che introduce il concetto | `'[Trascritto 1](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_1.md)'` |
| `Aggiornato` | data ultima modifica | `2026-05-04` o `'2026-05-04 (fonte: [Trascritto 3](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto 3.md))'` |

### Campi specifici

| Campo | Categorie | Valori |
|---|---|---|
| `Priorita` | cosmologia, magia | `fondamentale`, `derivata`, `speculativa` |
| `Tipo` | storia, entita, filosofia, fonti | `evento`, `concetto`, `entità`, `divinità`, `trascrizione`, `fazione`, `luogo`, `framework`, ecc. |
| `Data` | storia | data o periodo approssimativo |
| `File` | fonti | percorso del sorgente raw, es. `raw/Trascritto_1.md` |
| `Fondazione` | fazione | anno o data approssimativa |
| `Ubicazione` | luogo | dove nel mondo reale |

### Regole YAML

- I valori con ``, ``, `: `, `|` vanno tra apici singoli: `'[Trascritto 1](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_1.md)'`
- I valori semplici (date, parole singole) senza apici: `2026-05-04`, `fondamentale`
- Le chiavi NON contengono spazi: `Priorita` non `Priorità`, `Aggiornato` non `Ultima modifica`

### Esempi per categoria

```yaml
# cosmologia / magia
---
Categoria: cosmologia
Priorita: fondamentale
Fonte: '[Trascritto 1](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_1.md)'
Aggiornato: '2026-05-04 (fonte: [Trascritto 2](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_2.md))'
---

# storia
---
Categoria: storia
Tipo: evento
Data: remota (preistoria)
Fonte: '[Trascritto 2](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_2.md)'
Aggiornato: 2026-05-04
---

# entita
---
Categoria: entita
Tipo: entità
Fonte: '[Trascritto 1](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_1.md)'
Aggiornato: '2026-05-04 (fonte: [Trascritto 4](https://github.com/Devito02/Hyperlink-Wiki/blob/main/raw/Trascritto_4.md))'
---

# fonti
---
Categoria: fonti
Tipo: trascrizione
File: raw/Trascritto_1.md
Aggiornato: 2026-05-04
---
```

## Template

Disponibili in `_templates/`. Ogni template definisce frontmatter YAML + sezioni standard.

| Template | Per cartella | Sezioni |
|---|---|---|
| `cosmologia.md` | cosmologia/ | Principio, Implicazioni, Relazioni, Domande Aperte, Fonti |
| `magia.md` | magia/ | Principio, Implicazioni, Relazioni, Domande Aperte, Fonti |
| `storia.md` | storia/ | Descrizione, Implicazioni, Relazioni, Domande Aperte, Fonti |
| `entita.md` | entita/ | Descrizione, Caratteristiche, Implicazioni, Relazioni, Domande Aperte, Fonti |
| `filosofia.md` | filosofia/ | Descrizione, Implicazioni, Relazioni, Domande Aperte, Fonti |
| `fazione.md` | entita/ (Tipo: fazione) | Origine, Scopo, Struttura, Relazioni, Domande Aperte, Fonti |
| `luogo.md` | cosmologia/ (Tipo: luogo) | Descrizione, Proprietà, Relazioni, Domande Aperte, Fonti |
| `fonte.md` | fonti/ | Riassunto, Cosa introduce di nuovo, Cosa contraddice o affina, Pagine toccate |

## Flusso di Ingest

Quando l'utente droppa un nuovo file in `raw/`:

1. **Leggi** il sorgente.
2. **Discuti** con l'utente i takeaway chiave (cosa è nuovo? cosa contraddice o affina?).
3. **Crea/aggiorna** nell'ordine:
   a. Pagina riassunto in `wiki/fonti/` (template `fonte.md`)
   b. Pagine entità in `wiki/entita/` (template `entita.md` o `fazione.md`)
   c. Pagine `wiki/cosmologia/`, `wiki/magia/`, `wiki/storia/`, `wiki/filosofia/` (template corrispondente)
   d. `wiki/sintesi/` — solo se la novità cambia la visione d'insieme
   e. `wiki/index.md` — NON serve aggiornare manualmente le liste: Dataview auto-genera. Aggiungi solo nuove Domande Aperte.
   f. `wiki/log.md` — appendi entry: `## [YYYY-MM-DD] ingest | Titolo Sorgente` con elenco pagine toccate
4. **Riporta** tutto ciò che è stato toccato.

### Regole per le pagine nuove
- Usa frontmatter YAML con i campi della categoria (vedi sezione Frontmatter YAML)
- Quota i valori YAML con ``, ``, `: `, `|`
- Link Obsidian: `nome-file-senza-estensione`
- Sezioni: segui il template, ma aggiungi sezioni extra se il contenuto le richiede
- Nomenclatura: se un trascritto successivo rinomina un concetto, aggiorna titolo e link ovunque

## Flusso di Query

1. **Leggi** `wiki/index.md` per vedere le query Dataview e le pagine per categoria.
2. **Leggi** le pagine rilevanti.
3. **Sintetizza** con citazioni (link `wiki` alle pagine).
4. Se la risposta è sostanziale, **chiedi** se vuole salvarla in `wiki/sintesi/`.

## Flusso di Lint

Quando l'utente chiede un health-check:

1. Scansiona tutte le pagine wiki.
2. Verifica: frontmatter YAML valido, campi obbligatori presenti (`Categoria`, `Fonte`, `Aggiornato`), campi coerenti con la categoria.
3. Cerca: contraddizioni tra pagine, pagine orfane, concetti menzionati ma senza pagina, link a pagina inesistente, claim superati.
4. Produci un report in `wiki/sintesi/lint-YYYY-MM-DD.md` con azioni suggerite.

## Convenzioni di Scrittura

- Ogni pagina ha frontmatter YAML (`---` ... `---`) con i campi della categoria, poi titolo H1 (`# Nome`).
- I link tra pagine usano `nome-file-senza-estensione` (compatibile Obsidian). MAI usare percorsi nei link.
- **Nomenclatura:** se un trascritto successivo introduce un nome diverso per lo stesso concetto, aggiorna titolo e link coerentemente.
- I claim incerti si marcano `[DA VERIFICARE]`.
- I conflitti si marcano `⚠️ In conflitto con pagina — spiegazione`.
- Le domande risolte si marcano `**RISOLTO**` con riferimento al trascritto.
- **Niente commenti** nel corpo delle pagine. I metadati stanno nel frontmatter.
- **Niente descrizioni ovvie.** Se un fatto è su Wikipedia, non serve una pagina wiki.

## Dataview

Il plugin Dataview è attivo in Obsidian. `wiki/index.md` usa query Dataview per generare tabelle dinamiche.

Campi YAML accessibili in Dataview per nome chiave esatto: `Categoria`, `Priorita`, `Tipo`, `Fonte`, `Aggiornato`, `Data`, `File`.

Non serve aggiornare manualmente le liste di pagine in index.md — Dataview le popola automaticamente dalle cartelle. Vanno aggiornate solo: nuove Domande Aperte, modifiche alla struttura delle query.
