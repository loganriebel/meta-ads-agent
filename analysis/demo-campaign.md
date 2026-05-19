---
slug: "demo-campaign"
metrics_file: "examples/demo-campaign/metrics.csv"
date: "2026-05-18"
status: "complete"
period: "2026-05-04 to 2026-05-17"
---

# Performance Analysis: demo-campaign

## Executive summary
- **Spend:** $474.00
- **Conversions:** 47 trial signups
- **CPA:** $10.09 blended (demo data — artificially strong)
- **vs target:** Well below $75 target on winners; A2 video underperforms

## Decision table
| Entity | Spend | Conv | CPA | Impr | Freq | Action | Reason |
|--------|-------|------|-----|------|------|--------|--------|
| A1-v1 | $142.50 | 19 | $7.50 | 12400 | 2.1 | SCALE | CPA below target; strong volume |
| A2-v1 | $198.30 | 8 | $24.79 | 18200 | 2.4 | HOLD | CPA elevated but not at kill; test new hook |
| B1-v1 | $88.20 | 11 | $8.02 | 6200 | 1.8 | SCALE | LAL performing |
| C1-v1 | $45.00 | 9 | $5.00 | 2100 | 1.5 | SCALE | Retarget efficient |

## Ad set summary
- **Interest stack:** A1 carries ad set; pause A2 if CPA worsens next period
- **LAL:** Scale +20% daily
- **Retarget:** Scale +20%; watch audience size

## Winners (scale)
1. A1-v1 — Monday static hook
2. B1-v1 — same hook on LAL
3. C1-v1 — retarget proof

## Losers (pause)
- None at kill threshold in demo window

## Hold / learning
1. A2-v1 video — high spend, CPA $24.79; refresh hook or cut Reels-only

## Budget recommendations
| Ad set | Current daily | Recommended | Change % |
|--------|---------------|-------------|----------|
| Interest | $50 | $60 | +20% (A1 only; pause A2 optional) |
| LAL | $50 | $60 | +20% |
| Retarget | $50 | $60 | +20% |

## Creative insights
- **Hooks:** "Monday deck at 8pm" beats Excel video opener on CPA
- **Formats:** Static 1:1 outperformed 15s video in this demo
- **Audiences:** LAL and retarget amplify winning hook

## Next tests
1. New video hook matching A1 static line
2. Duplicate A1 to new broad ad set with 10% budget test

## Human action checklist
- [ ] Pause A2-v1 if CPA > $112 after $30 more spend
- [ ] Increase budgets per table (max 30% per guardrails)
- [ ] Export fresh metrics after 5 days
