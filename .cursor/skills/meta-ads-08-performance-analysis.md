---
name: meta-ads-08-performance-analysis
description: Stage 8 — Analyze exported metrics, classify winners/losers, recommend prune/scale/hold actions.
---

# Stage 8 — Performance analysis

Turn exported Meta metrics into decisions. Output: **`analysis/[campaign-slug].md`**.

## Inputs

- Metrics CSV in `metrics/` or `metrics/exports/` (user-provided export)
- `meta-ads-config.yaml` — `metrics_thresholds`, `budget_guardrails`
- `strategy/[slug].md` — decision rules
- `.cursor/rules/meta-ads-safety.mdc`

## Process

### 1. Confirm data
Required columns (or map them): `ad_name`, `ad_set_name`, `spend`, `impressions`, `clicks`, `conversions`, `cpa` or computable from spend/conversions.

If missing, ask user to re-export from Ads Manager.

### 2. Run analyzer (optional)
```bash
python meta_ads_tools/analyze_metrics.py --metrics path/to.csv --config meta-ads-config.yaml --slug [slug]
```

Use tool output as a starting point; explain reasoning in prose.

### 3. Classify each ad / ad set
- **Winner** — scale candidate
- **Loser** — pause/kill candidate
- **Hold** — learning / insufficient data
- **Fatigue** — frequency high, CTR decay

Respect `min_spend_before_decision_usd` and `min_days_before_kill`.

### 4. Recommendations
Concrete actions: pause ad X, increase ad set Y budget by 20%, duplicate winner to new ad set, etc. **Recommendations only** — no API execution.

### 5. Creative/copy insights
What hooks, angles, audiences drove results?

## Output template

Save to `analysis/[slug].md`:

```markdown
---
slug: "[slug]"
metrics_file: "metrics/..."
date: "YYYY-MM-DD"
status: "complete"
period: "YYYY-MM-DD to YYYY-MM-DD"
---

# Performance Analysis: [slug]

## Executive summary
- **Spend:**
- **Conversions:**
- **CPA / ROAS:**
- **vs target:**

## Decision table
| Entity | Spend | Conv | CPA | ROAS | Impr | Freq | Action | Reason |
|--------|-------|------|-----|------|------|------|--------|--------|
| Ad A1 | | | | | | | SCALE | |

## Ad set summary
...

## Winners (scale)
1. ...

## Losers (pause)
1. ...

## Hold / learning
1. ...

## Budget recommendations
| Ad set | Current daily | Recommended | Change % |
|--------|---------------|-------------|----------|

## Creative insights
- **Hooks:**
- **Formats:**
- **Audiences:**

## Next tests
1. ...

## Human action checklist
- [ ] Pause losers in Ads Manager
- [ ] Apply budget changes
- [ ] Export fresh metrics after 3-5 days
```

## After completion

Ask approval before **Learning loop** (`meta-ads-09-learning-loop`).
