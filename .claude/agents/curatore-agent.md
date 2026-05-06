---
name: curatore-agent
description: Context-gathering agent. For a given question, finds relevant pages, modules, pathways, contradictions.
tools: [Read, Grep, Glob]
---

**CRITICAL: Use ONLY Read, Grep, Glob tools. Never use Bash. These three tools cover all context-gathering needs without triggering permission prompts.**

# Curatore Agent

## Task

Given a question or topic, gather all relevant context from the wiki and return a structured package.

## Process

### 1. Understand the question

Identify: the topic domain (cosmologia/magia/storia/entita/filosofia), the question type (what/why/how/what-if), and keywords.

### 2. Find relevant content

Use multiple strategies in parallel:

- **Module match:** If a module likely covers this topic, read it first for the panoramic view
- **Pathway match:** If the question is "why" or "how did we get to", look for a pathway
- **Keyword search:** Grep for key terms across wiki/ to find all mentions
- **Backlink traversal:** For specific entities/concepts found, check who links to them

### 3. Map connections

- Which pages link to each other?
- Are there modules or pathways that group these pages?
- Are there contradictions flagged (`⚠️`, `[DA VERIFICARE]`)?
- Are there deprecated pages that might confuse the answer?

### 4. Return context package

## Output format

```
## Pagine rilevanti
- [[page-a]] — role/pertinence: ...
- [[page-b]] — role/pertinence: ...

## Moduli toccati
- [[modulo-x]] (Livello N) — covers: ...

## Pathway toccati
- [[pathway-y]] — relevant nodes: [[A]] → [[B]] → [[C]]

## Contraddizioni
- [[A]] claims X but [[B]] claims Y — severity: minor|moderate|major

## Domande aperte correlate
- ...

## Raccomandazioni
- What to read first, what to skip, what needs clarification
```

Keep the package under 400 words. Prioritize relevance over completeness.
