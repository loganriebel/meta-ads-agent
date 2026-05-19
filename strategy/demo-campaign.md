---
slug: "demo-campaign"
intake: "intake/demo-campaign.md"
research: "research/demo-campaign.md"
date: "2026-05-18"
status: "complete"
---

# Strategy: Q2 Free Trial Push

## Goals
- **Objective:** OUTCOME_LEADS (trial signup)
- **Primary KPI:** CPA $75 target / $112 kill / scale when CPA ≤ $60 with 10+ conversions

## Hypotheses
| ID | Hypothesis | Success signal |
|----|------------|----------------|
| H1 | Monday pain hook beats feature hook for cold traffic | Lower CPA on Ad A1 vs A2 |
| H2 | LAL 1% trial users beats interest stack | Lower CPA on Ad set B vs A |
| H3 | Retargeting 7d visitors with proof closes cheap | CPA < $50 on Ad set C |

## Angles in this flight
| Angle | Audience | Priority |
|-------|----------|----------|
| Monday report pain | Cold broad + interests | P0 |
| Leadership dashboard | Cold interests | P1 |
| Social proof trial | Retarget 7d | P0 |

## Testing matrix
| Level | Test | Hold constant |
|-------|------|---------------|
| Ad set | Audience (broad, LAL, retarget) | Angle per ad set |
| Ad | Hook + format (static vs video) | Targeting within ad set |

## Campaign structure
```
Campaign: META_OUTCOME_LEADS_demo-campaign_20260518
├── Ad set A: Interests — marketing software, HubSpot, GA4 — Angle Monday pain
│   ├── Ad A1-v1: Static — Monday 8pm hook
│   └── Ad A2-v1: Video 15s — spreadsheet chaos → dashboard
├── Ad set B: LAL 1% trial signups — Angle Monday pain
│   └── Ad B1-v1: Static — same hook as A1
└── Ad set C: Retarget website 7d — Social proof
    └── Ad C1-v1: Static — logo row + trial CTA
```

## Budget plan
| Ad set | Daily USD | Role | Min spend before decision |
|--------|-----------|------|---------------------------|
| A | 50 | test | 30 |
| B | 50 | test | 30 |
| C | 50 | scale retarget | 30 |

## Targeting notes
### Ad set A
- **Targeting:** US/CA/UK/AU, 25–54, interests: digital marketing, HubSpot, Google Analytics
- **Exclusions:** existing customers, 180d converters
- **Placements:** Feed, Stories, Reels (per config)

### Ad set B
- **Targeting:** 1% LAL trial signups
- **Exclusions:** same as A

### Ad set C
- **Targeting:** Website visitors 7d
- **Exclusions:** converters 14d

## Decision rules
- **Kill:** CPA > $112 after $30 spend OR 0 conversions after $30
- **Hold:** spend < $30 or < 1000 impressions
- **Scale:** CPA ≤ $60, 10+ conversions — increase budget 20%, max 30% per step

## Naming convention
- Campaign: `META_OUTCOME_LEADS_demo-campaign_20260518`
- Ad set: `META_OUTCOME_LEADS_interest_monday_20260518`
- Ad: `META_AD_A1-v1_monday-static`

## Creative & copy brief (for next stages)
| Ad ID | Angle | Hook | Format | Notes |
|-------|-------|------|--------|-------|
| A1-v1 | Monday pain | Still building the Monday deck at 8pm? | 1:1 static | UI screenshot |
| A2-v1 | Monday pain | Video: spreadsheet → dashboard | 9:16 | captions |
| B1-v1 | Monday pain | Same as A1 | 1:1 | LAL cell |
| C1-v1 | Proof | Teams ship Monday reports in 20 min | 1:1 | logos blurred |

## Risks & mitigations
- Creative fatigue on small audiences → monitor frequency > 3
