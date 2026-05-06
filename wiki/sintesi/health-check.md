---
Categoria: sintesi
Tipo: strumento
Fonte: '[[CLAUDE.md]]'
Aggiornato: 2026-05-06
---

# Health Check

Diagnostica automatica della wiki. Apri questa pagina in Obsidian per vedere i problemi.

---

## Frontmatter Mancante o Invalido

```dataviewjs
const required = ["Categoria", "Fonte", "Aggiornato"];
const pages = dv.pages().where(p => p.file.path.startsWith("wiki/") && !p.file.path.startsWith("wiki/sintesi") && !p.file.path.startsWith("wiki/fonti"));

const issues = [];
for (const p of pages) {
    const missing = required.filter(f => !p[f]);
    if (missing.length > 0) {
        issues.push({page: p.file.link, missing: missing.join(", ")});
    }
}

if (issues.length === 0) {
    dv.paragraph("✅ Tutte le pagine hanno frontmatter completo.");
} else {
    dv.table(["Pagina", "Campi Mancanti"], issues.map(i => [i.page, i.missing]));
}
```

---

## Pagine Orfane

Pagine senza link entranti (escluse fonti e sintesi).

```dataviewjs
const orphans = dv.pages()
    .where(p => p.file.path.startsWith("wiki/") 
        && !p.file.path.startsWith("wiki/fonti") 
        && !p.file.path.startsWith("wiki/sintesi")
        && p.file.inlinks.length === 0)
    .sort(p => p.file.name);

if (orphans.length === 0) {
    dv.paragraph("✅ Nessuna pagina orfana.");
} else {
    dv.table(["Pagina", "Categoria"], orphans.map(p => [p.file.link, p.Categoria || "-"]));
}
```

---

## Deprecate con Backlink

Pagine deprecate che altre pagine linkano ancora.

```dataviewjs
const deprecated = dv.pages()
    .where(p => p.Stato === "Deprecato" && p.file.inlinks.length > 0)
    .sort(p => p.file.name);

if (deprecated.length === 0) {
    dv.paragraph("✅ Nessuna pagina deprecata con backlink attivi.");
} else {
    for (const p of deprecated) {
        dv.paragraph(`⚠️ **${p.file.link}** → sostituita da ${p.Sostituito_Da || "?"} (${p.file.inlinks.length} backlink)`);
        const linkers = p.file.inlinks
            .filter(l => l.path.startsWith("wiki/"))
            .map(l => dv.fileLink(l.path));
        dv.list(linkers);
    }
}
```

---

## Claim Incerti

`[DA VERIFICARE]` e `⚠️` ancora presenti nel corpo pagina.

```dataviewjs
const uncertain = dv.pages()
    .where(p => p.file.path.startsWith("wiki/"))
    .filter(p => {
        const content = dv.fileLink(p.file.path);
        return false; // Placeholder: content scan must be done differently
    })
    .values;

// Content scan via dv.io.load — async, non eseguibile in blocco tabella.
// Usa la lista sotto generata manualmente o esegui ricerca full-text in Obsidian.
dv.paragraph('Usa la ricerca full-text di Obsidian: cerca `[DA VERIFICARE]` e `⚠️` per trovare i claim incerti.');
```

---

## Link a Vuoto (Broken Links)

```dataviewjs
const allPages = new Set(dv.pages().map(p => p.file.path));
const broken = [];

for (const p of dv.pages().where(p => p.file.path.startsWith("wiki/"))) {
    for (const link of p.file.outlinks) {
        const targetPath = link.path.endsWith(".md") ? link.path : link.path + ".md";
        if (!allPages.has(targetPath)) {
            broken.push({
                from: p.file.link,
                to: link.path,
                type: "file-not-found"
            });
        }
    }
}

if (broken.length === 0) {
    dv.paragraph("✅ Nessun link rotto trovato.");
} else {
    // Deduplicate by link target
    const seen = new Set();
    const unique = broken.filter(b => {
        const key = b.to;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    }).slice(0, 50);

    dv.table(["Link Rotto", "Linkato Da (esempio)"], unique.map(b => [b.to, b.from]));
    if (broken.length > 50) {
        dv.paragraph(`...e altri ${broken.length - 50} link.`);
    }
}
```

---

## Riepilogo

| Check                  | Stato                                      |
| ---------------------- | ------------------------------------------ |
| Frontmatter            | vedi sopra                                 |
| Orfane                 | vedi sopra                                 |
| Deprecate con backlink | vedi sopra                                 |
| Link a vuoto           | vedi sopra                                 |
| Claim incerti          | cerca `[DA VERIFICARE]` / `⚠️` in Obsidian |
