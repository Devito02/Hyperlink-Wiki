# Sub-Agent Architecture for LLM Wiki

**Date:** 2026-05-06
**Status:** Design (not yet implemented)
**Topic:** Sub-agent system for wiki workflows

## Architecture

```
Main Agent (Claude Code)
├── Decide strategy (which layers, what radius)
├── Read modules (structural context)
├── Launch explore-agent(s) (1+ parallel, by radius or pathway)
├── Synthesize results from all layers
└── Respond to user

check-agent (on "/lint" or after 3+ ingests accumulated)
├── Explore entire wiki
├── Verify: frontmatter, broken links, orphans, deprecated with backlinks, unresolved claims
└── Produce report
```

## Agents

### Main Agent (Claude Code curator)

- Reads modules first for structural context (Level 1 → 2 → 3 as needed)
- Decides exploration strategy adaptively per query:
  - "What is X?" → radius-1 agent only
  - "Why did Y happen?" → modules + pathway agent
  - "How does Z work?" → modules + radius-1 agent
- Synthesizes results from all sub-agents
- Does NOT delegate synthesis — the main agent is the only one with query intent

### explore-agent(s)

Launched in parallel by main agent. Each instance:
- Explores one page + its direct backlinks (radius-1)
- Can also explore pathways (reads a pathway file and all nodes in sequence)
- Returns: structured summary of findings (entities, connections, contradictions)
- Model: Haiku (cheap, fast, read-only research)

Strategy selection (main agent decision):
1. **By radius:** one agent for target page + backlinks
2. **By pathway:** one agent reads the pathway narrative
3. **Mixed:** parallel radius + pathway agents for complex queries

### check-agent

Activation:
- Explicit: user types "/lint"
- Prompted: after 3+ ingests accumulated, main agent asks "check?"

Tasks:
- Frontmatter validation (required fields present, valid values)
- Broken link detection ([[links]] that don't resolve)
- Orphan detection (pages with zero inlinks, excluding fonti/sintesi)
- Deprecated pages with active backlinks
- Unresolved claims ([DA VERIFICARE] and ⚠️ markers)

Returns: report saved to `wiki/sintesi/lint-YYYY-MM-DD.md`

## Design Decisions

- **No separate synthesis-agent.** Synthesis requires query intent, which only the main agent has. Adding a synthesis agent would create latency without value.
- **Elastic strategy.** The main agent adaptively chooses which layers to use. No rigid rules — AI judgment per query.
- **Modules first.** Structural context via modules before detailed exploration. Prevents the "forest vs trees" problem.
- **Check is periodic, not per-ingest.** Running full lint every ingest is wasteful. Accumulate and batch.

## Sub-CLAUDE.md Strategy

Sub-directory CLAUDE.md files for lazy-loading domain context:

```
wiki/cosmologia/CLAUDE.md   — rules for cosmologia concepts
wiki/magia/CLAUDE.md        — rules for magic mechanics
wiki/storia/CLAUDE.md       — timeline and event rules
wiki/entita/CLAUDE.md       — entity categorization rules
wiki/filosofia/CLAUDE.md    — framework and interpretation rules
wiki/moduli/CLAUDE.md       — module creation guidelines
wiki/pathway/CLAUDE.md      — pathway creation guidelines
```

Loaded on-demand when files in those directories are touched.

## Not Designed (future)

- Path-scoped rules via `.claude/rules/`
- Hooks for automation (PreToolUse, PostToolUse, SessionStart)
- Custom agent files in `.claude/agents/`
- These will be explored in the next phase
