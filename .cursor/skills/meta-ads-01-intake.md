---
name: meta-ads-01-intake
description: Stage 1 — Collect offer, ICP, funnel, budget, tracking, constraints, and baseline Meta performance for a new campaign.
---

# Stage 1 — Intake

Collect everything needed before research and strategy. Output: **`intake/[campaign-slug].md`**.

## Inputs

- User's campaign idea, offer, or product
- Optional: past Meta Ads Manager exports, GA4 notes, CRM conversion rates
- `AGENTS.md`, `meta-ads-config.yaml`

## First-run setup wizard

If config has placeholders (`YOUR_BUSINESS_NAME`, `yourdomain.com`, `YOUR_TONE`, `YOUR_AUDIENCE`), greet the user:

> **Welcome to Meta Ads Agent.** I'll configure your template once, then capture this campaign's intake.

Ask **one question at a time**:

1. Business name
2. Domain (no https)
3. Primary offer URL for ads
4. Brand tone (few words)
5. Target audience (specific)
6. Primary Meta objective (Leads / Sales / Traffic)
7. Target CPA or ROAS (if known)
8. Monthly or weekly test budget
9. Conversion event name (e.g. Lead, Purchase)
10. Pixel/CAPI status (none / partial / mature)
11. Meta ad account ID *(optional)*
12. Restrictions or compliance notes *(optional)*

Update `meta-ads-config.yaml` with answers. Then continue intake for the campaign.

## Campaign questions (one at a time if needed)

1. Campaign slug (or propose `kebab-case` from offer name)
2. What are we promoting this flight?
3. Landing page URL (confirm vs config default)
4. Funnel stage (cold prospecting / retargeting / both)
5. Geo and language
6. Budget for this test flight (daily + duration)
7. Success metric (CPA, ROAS, CPL, demo rate)
8. Existing creative assets? (Y/N, describe)
9. What must we **not** say or target?

## Output template

Save to `intake/[campaign-slug].md`:

```markdown
---
slug: "[campaign-slug]"
date: "YYYY-MM-DD"
status: "complete"
business: "[from config]"
---

# Campaign Intake: [Name]

## Offer
- **Product/offer:**
- **Landing URL:**
- **Primary CTA:**
- **Price/value context:**

## Audience
- **ICP:**
- **Pain:**
- **Awareness level:** cold / warm / hot

## Funnel & objective
- **Meta objective:** OUTCOME_LEADS | OUTCOME_SALES | OUTCOME_TRAFFIC
- **Conversion event:**
- **Funnel:** prospecting / retargeting / mixed

## Geo & language
- **Countries:**
- **Languages:**

## Budget & timeline
- **Daily budget (USD):**
- **Test duration (days):**
- **Total test cap:**

## Tracking
- **Pixel ID:**
- **CAPI:**
- **UTM pattern:** (from config)
- **Baseline CPA/ROAS:** (if known)

## Constraints
- **Compliance:**
- **Banned claims:**
- **Creative constraints:**

## Assets on hand
- **Existing creative:**
- **Brand kit:**

## Success criteria
- **Primary KPI:**
- **Target:**
- **Kill threshold:**

## Open questions
- ...
```

## After completion

Summarize intake. Ask:

1. Anything wrong or missing?
2. Approve to move to **Research** (`meta-ads-02-research`)?

Do not proceed without explicit approval.
