---
slug: "demo-campaign"
date: "2026-05-18"
status: "pass-with-notes"
payload_reviewed: false
---

# QA / Launch Pack: demo-campaign

## Summary
**Status:** PASS WITH NOTES
**Payloads:** api-payloads/demo-campaign/
**Human must:** Review JSON drafts; create PAUSED entities in Ads Manager; upload creatives

## Validation results
| Tool | Result |
|------|--------|
| validate_config | Placeholders expected in template config |
| validate_artifact | PASS on campaign-drafts/demo-campaign.yaml |
| build_payloads | Run to regenerate api-payloads |

## Crosswalk
| Check | Pass/Fail |
|-------|-----------|
| Every ad in strategy exists in YAML | Pass |
| Copy matches copy/demo-campaign.md | Pass |
| URLs use signalboard.example | Pass (fictional) |
| Budgets ≤ guardrails ($50/ad set) | Pass |
| Naming matches convention | Pass |
| UTMs on all ads | Pass |

## Policy
| Item | Severity | Action |
|------|----------|--------|
| Fictional social proof "500+ teams" in C1 creative | warning | Use real proof before live |

## Launch steps (human)
1. Upload A1-v1, A2-v1, C1-v1 assets to Meta Creative Library
2. Create campaign PAUSED — objective Leads
3. Create 3 ad sets per strategy; paste targeting manually
4. Optional: use api-payloads JSON as reference only after setting act_/pixel/page IDs
5. Publish ads PAUSED; review previews; then enable

## Sign-off
- [ ] I approve launching this campaign in Meta (human initials/date)
