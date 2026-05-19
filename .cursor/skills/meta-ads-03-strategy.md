---
name: meta-ads-03-strategy
description: Stage 3 — Define hypotheses, testing matrix, campaign structure, budgets, kill/scale thresholds, and naming.
---

# Stage 3 — Strategy

Design the test plan and Meta campaign architecture. Output: **`strategy/[campaign-slug].md`**.

## Inputs

- `intake/[slug].md`, `research/[slug].md` (approved)
- `meta-ads-config.yaml` — `campaign_defaults`, `budget_guardrails`, `metrics_thresholds`, `naming`
- `learnings/` optional

Invoke **`paid-ads`** skill for structure and testing best practices.

## Process

### 1. Confirm angles
User-selected angles from research (1–3 for first flight).

### 2. Hypotheses
For each angle, write: *If we show [message] to [audience], then [metric] will improve because [reason].*

### 3. Testing matrix
Define what varies at each level:

| Level | What we test | Hold constant |
|-------|----------------|---------------|
| Campaign | objective, budget type | — |
| Ad set | audience, placement, budget | creative theme per cell |
| Ad | creative, copy variant | targeting within ad set |

Aim for **statistical-ish separation**: don't change audience and hook in the same cell without a plan.

### 4. Campaign structure
Example (adapt to budget):

```
Campaign: META_OUTCOME_LEADS_[slug]_[date]
├── Ad set A: Broad + interest stack — Angle 1
│   ├── Ad A1: Hook variant 1
│   └── Ad A2: Hook variant 2
├── Ad set B: Lookalike 1% purchasers — Angle 1
└── Ad set C: Retargeting 7d visitors — Angle 2
```

### 5. Budget allocation
- % prospecting vs retargeting
- Daily budget per ad set (respect `budget_guardrails`)
- Minimum spend before kill (`min_spend_before_decision_usd`)

### 6. Decision rules
From config thresholds — document kill, hold, scale rules for this flight.

### 7. Naming
Apply `naming.pattern` from config with concrete examples.

## Output template

Save to `strategy/[slug].md`:

```markdown
---
slug: "[slug]"
intake: "intake/[slug].md"
research: "research/[slug].md"
date: "YYYY-MM-DD"
status: "complete"
---

# Strategy: [Campaign name]

## Goals
- **Objective:**
- **Primary KPI:** target / kill / scale thresholds

## Hypotheses
| ID | Hypothesis | Success signal |
|----|------------|----------------|
| H1 | ... | CPA < $X |

## Angles in this flight
| Angle | Audience | Priority |
|-------|----------|----------|
| ... | ... | P0 |

## Testing matrix
[table or diagram]

## Campaign structure
[tree]

## Budget plan
| Ad set | Daily USD | Role | Min spend before decision |
|--------|-----------|------|---------------------------|
| ... | ... | test / scale | ... |

## Targeting notes
### Ad set A
- **Targeting:**
- **Exclusions:**
- **Placements:**

## Decision rules
- **Kill:** ...
- **Hold:** ...
- **Scale:** max +30% per step, min 3 days

## Naming convention
- Campaign: `...`
- Ad set: `...`
- Ad: `...`

## Creative & copy brief (for next stages)
| Ad ID | Angle | Hook | Format | Notes |
|-------|-------|------|--------|-------|
| A1 | ... | ... | 1:1 static | ... |

## Risks & mitigations
- ...
```

## After completion

Ask approval before **Creative** (`meta-ads-04-creative`) and **Copy** (`meta-ads-05-copy`).
