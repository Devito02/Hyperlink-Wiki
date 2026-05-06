# Regole Moduli

## Template

Usa `_templates/modulo.md` per creare moduli.

## Livelli

- **1** — Macro-categorie (Cosmologia, Magia, Storia, Entità, Filosofia)
- **2** — Trasversali (es. Rottura = cosmologia ∩ storia)
- **3** — Specifici (es. Architettura della Rottura = solo crepe + centrali)

## Criteri di creazione

- Crea un modulo quando 5+ pagine condividono un tema o rispondono alla stessa domanda
- Una pagina può appartenere a più moduli (appartenenza multipla)
- Sottomoduli vanno dichiarati sia nel frontmatter YAML (`Sottomoduli`) che nel corpo
- Aggiorna `wiki/moduli/index.md` quando crei un modulo di Livello 1 o 2

## Formato

```yaml
---
Categoria: moduli
Livello: 1|2|3
Fonte: '[[fonte]]'
Aggiornato: YYYY-MM-DD
Sottomoduli:
  - '[[sottomodulo]]'
---
```

Sezioni: Descrizione, Contenuti, Sottomoduli, Relazioni.
