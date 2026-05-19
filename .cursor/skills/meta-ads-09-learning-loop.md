---
name: meta-ads-09-learning-loop
description: Stage 9 — Update learnings library and seed next campaign strategy from winners.
---

# Stage 9 — Learning loop

Capture durable insights and optional next-cycle brief. Updates **`learnings/*.md`** and may create **`strategy/[slug]-v2.md`** seed.

## Inputs

- `analysis/[slug].md` (approved)
- `research/[slug].md`, `creative/[slug].md`, `copy/[slug].md`
- Prior `learnings/` files

## Process

### 1. Extract learnings
From analysis, pull:
- Winning hooks → `learnings/hooks.md`
- Winning angles → `learnings/angles.md`
- Winning audiences → `learnings/audiences.md`
- Formats → `learnings/creative-formats.md`
- Failures → `learnings/losers.md`

Use append format with date + slug + metric.

### 2. Anti-patterns
Document what to stop doing (with evidence).

### 3. Next cycle seed (optional)
If user wants another flight, draft **`strategy/[slug]-v2.md`** outline:
- Scale winners
- 1–2 new angles only
- Budget shift %

### 4. Update CLAUDE.md inventory
Add row to campaign inventory table (user or agent).

## Learning entry format

```markdown
## [YYYY-MM-DD] [slug] — [short title]
- **Metric:** CPA $X / ROAS X
- **Insight:** ...
- **Reuse when:** ...
- **Avoid when:** ...
```

## After completion

Ask:
1. Start new campaign intake?
2. Resume scale on same slug?
3. Done for now?

Do not auto-start Stage 1 without approval.
