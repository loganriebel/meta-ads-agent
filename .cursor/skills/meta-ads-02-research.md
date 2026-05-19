---
name: meta-ads-02-research
description: Stage 2 — Research audience pains, competitor ad angles, Meta Ad Library patterns, and policy risks.
---

# Stage 2 — Research

Turn approved intake into research for angles and creative. Output: **`research/[campaign-slug].md`**.

## Inputs

- `intake/[slug].md` (approved)
- `AGENTS.md`, `meta-ads-config.yaml`
- `learnings/` (if exists)

## Process

### 1. Read intake
Confirm slug, offer, ICP, constraints.

### 2. Audience & pain research
- Search Reddit, X, LinkedIn, reviews for **verbatim language** (paraphrase with source).
- List top 5 pains and desired outcomes.
- Note objections to the offer.

### 3. Competitor / category ads
- Use web search and **Meta Ad Library** (search competitor names + category).
- Record 5–10 ad patterns: hooks, formats, offers, social proof style.
- Do **not** copy; note gaps you can own.

### 4. Angle hypotheses (raw)
Propose 5+ angles ranked by fit to ICP and offer.

### 5. Policy & compliance scan
Flag restricted claims, personal attributes, sensational health/finance language.

### 6. Learnings cross-check
If `learnings/hooks.md` or `angles.md` exist, note what to reuse or avoid.

## Output template

Save to `research/[slug].md`:

```markdown
---
slug: "[slug]"
intake: "intake/[slug].md"
date: "YYYY-MM-DD"
status: "complete"
---

# Research: [Campaign name]

## ICP snapshot
[2-3 sentences]

## Pain points (evidence)
| Pain | Source | Quote or paraphrase |
|------|--------|---------------------|
| ... | Reddit / review / ... | ... |

## Objections
1. ...
2. ...

## Competitor ad patterns
| Brand | Hook style | Format | Offer | Gap we can exploit |
|-------|------------|--------|-------|-------------------|
| ... | ... | static/video | ... | ... |

## Meta Ad Library notes
- **Queries used:**
- **Patterns:** (UGC, demo, stat-led, etc.)

## Angle hypotheses (ranked)
### 1. [Angle name] ⭐
- **Hook direction:**
- **Why now:**
- **Risk:**

### 2. ...

## Policy flags
- [ ] None
- [ ] Items: ...

## Recommended angles for strategy (top 3)
1. ...
2. ...
3. ...

## Raw notes
...
```

## After completion

Ask user to pick angles (or adjust). Approve before **Strategy** (`meta-ads-03-strategy`).
