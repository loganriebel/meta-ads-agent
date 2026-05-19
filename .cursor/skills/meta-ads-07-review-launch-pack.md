---
name: meta-ads-07-review-launch-pack
description: Stage 7 — Validate draft payloads, policy review, and prepare human launch/API review package.
---

# Stage 7 — Review launch pack

QA the campaign draft and API payload drafts before any human pastes into Meta. Output: **`qa-reports/[campaign-slug].md`** and verified **`api-payloads/[campaign-slug]/`**.

## Inputs

- `campaign-drafts/[slug].yaml`
- `api-payloads/[slug]/` (generate via `build_payloads.py` if missing)
- All prior artifacts for cross-check
- `.cursor/rules/meta-ads-safety.mdc`

## Process

### 1. Run validators
```bash
python meta_ads_tools/validate_config.py meta-ads-config.yaml
python meta_ads_tools/validate_artifact.py campaign-drafts/[slug].yaml
```

### 2. Payload review
For each file in `api-payloads/[slug]/`:
- `_meta.status` must be `draft`
- `_meta.reviewed_by_human` must be `false` until user signs off
- Required fields present: account_id placeholder OK with warning

### 3. Crosswalk
| Check | Pass/Fail |
|-------|-----------|
| Every ad in strategy exists in YAML | |
| Copy matches copy/[slug].md | |
| URLs match intake landing page | |
| Budgets ≤ guardrails | |
| Naming matches convention | |
| UTMs on all ads | |

### 4. Policy pass
List any copy/creative/policy flags with severity (blocker / warning).

### 5. Launch pack for human
Summarize: what to create in Ads Manager, order of operations, what to paste from payloads.

## Output template

Save to `qa-reports/[slug].md`:

```markdown
---
slug: "[slug]"
date: "YYYY-MM-DD"
status: "pass" | "fail" | "pass-with-notes"
payload_reviewed: false
---

# QA / Launch Pack: [slug]

## Summary
**Status:** PASS / FAIL
**Payloads:** api-payloads/[slug]/
**Human must:** create in Ads Manager OR import after reviewing JSON

## Validation results
| Tool | Result |
|------|--------|
| validate_config | |
| validate_artifact | |
| build_payloads | |

## Crosswalk
[table]

## Policy
| Item | Severity | Action |
|------|----------|--------|

## Launch steps (human)
1. ...
2. Upload creatives to Meta...
3. Create campaign PAUSED...
4. ...

## Sign-off
- [ ] I approve launching this campaign in Meta (human initials/date)
```

Update payload `_meta.reviewed_by_human` only after user explicitly approves in chat.

## After completion

Tell user to launch in Meta manually or via their own API tooling. After live + data: export metrics to `metrics/` and run **Stage 8**.
