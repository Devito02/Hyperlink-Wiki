# Regole Lint

## Cosa verificare

1. Frontmatter YAML valido: `Categoria`, `Fonte`, `Aggiornato` presenti
2. `Stato: Deprecato` implica `Sostituito_Da`
3. Link `[[wiki]]` che non risolvono a file esistenti
4. Pagine orfane (zero backlinks, escluso fonti/sintesi/moduli/pathway)
5. Deprecate con backlink attivi
6. Claim `[DA VERIFICARE]` e `⚠️` non risolti

## Formato Report

Salva in `wiki/sintesi/lint-YYYY-MM-DD.md`:

```
# Lint Report YYYY-MM-DD

## Frontmatter issues
- [[pagina]] — campi mancanti: X, Y

## Broken links
- [[pagina]] linka [[inesistente]]

## Orphan pages
- [[pagina]] — nessun backlink

## Deprecated with backlinks
- [[pagina]] — deprecata ma ancora linkata da [[A]], [[B]]

## Unresolved claims
- [[pagina]] — N marker [DA VERIFICARE] o ⚠️
```
