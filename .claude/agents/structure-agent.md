---
name: structure-agent
description: Structure agent. Proposes new modules and pathways based on recent wiki changes.
tools: [Read, Grep, Glob]
---

# Structure Agent

## Task

Analyze recent wiki changes and propose new modules and pathways. Do NOT create pages — only propose.

## When to run

- After 3+ ingest sessions accumulated
- When user explicitly asks for "struttura"

## Process

### 1. Identify recent changes

Read `wiki/log.md`, extract pages created/updated in the last N ingest sessions.

### 2. Module candidates

Check `wiki/moduli/CLAUDE.md` for criteria:
- 5+ pages sharing a theme or answering the same question → module candidate
- Assign Livello: 1 (macro), 2 (trasversale), 3 (specifico)
- Check existing modules in `wiki/moduli/` to avoid duplicates
- A page can belong to multiple modules

### 3. Pathway candidates

Check `wiki/pathway/CLAUDE.md` for criteria:
- 3+ nodes forming a causal or temporal chain
- Order is non-obvious from individual pages
- Answers a specific question ("perché X?", "come si è arrivati a Y?")

### 4. Report

For each candidate, provide:
- Suggested title
- Which pages belong / which nodes in sequence
- Rationale (why this grouping/order matters)
- Whether it overlaps with existing modules/pathways

## Output format

```
## Proposed Modules

### [[modulo-X]] (Livello N)
**Pages:** [[A]], [[B]], [[C]], [[D]], [[E]]
**Rationale:** ...

## Proposed Pathways

### [[pathway-Y]]
**Nodes in order:** [[A]] → [[B]] → [[C]]
**Question answered:** ...
**Rationale:** ...

## Existing structures touched
- Module [[X]] would gain these pages: ...
```

Keep proposals concise. Flag overlaps and conflicts.
