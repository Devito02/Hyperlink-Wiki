---
name: check-agent
description: Wiki health-check agent. Verifies frontmatter, links, orphans, deprecated pages.
tools: [Read, Grep, Glob]
---

**CRITICAL: Use ONLY Read, Grep, Glob tools. Never use Bash. These three tools cover all health-check needs without triggering permission prompts.**

# Check Agent

## Task

Run a full health-check on the wiki and produce a structured report.

## Checks

### 1. Frontmatter validation
- Every page in `wiki/` (excluding fonti/ and sintesi/) must have: `Categoria`, `Fonte`, `Aggiornato`
- Pages with `Stato: Deprecato` must also have `Sostituito_Da`

### 2. Broken links
- Find all `[[links]]` across all pages
- Check if the target file exists (search for `<link>.md` anywhere in wiki/ or raw/)
- Report links that don't resolve

### 3. Orphan pages
- Pages with zero inbound links from other wiki pages
- Exclude: fonti/, sintesi/, moduli/, pathway/

### 4. Deprecated pages with active backlinks
- Pages where `Stato: Deprecato` AND `file.inlinks.length > 0`
- These are pages that others still reference — needs attention

### 5. Unresolved claims
- Count `[DA VERIFICARE]` and `⚠️` across all pages
- Report pages with unresolved markers

## Output

Save to `wiki/sintesi/lint-YYYY-MM-DD.md` with sections for each check above. Include counts and specific page references.
