---
name: meta-ads-06-build-drafts
description: Stage 6 — Build campaign/ad set/ad YAML structure from approved strategy, creative, and copy.
---

# Stage 6 — Build drafts

Assemble a machine-readable campaign draft for tooling and API payload generation. Output: **`campaign-drafts/[campaign-slug].yaml`**.

## Inputs

- `strategy/[slug].md`, `creative/[slug].md`, `copy/[slug].md` (all approved)
- `meta-ads-config.yaml`
- `.cursor/rules/meta-ads-safety.mdc`

**Do not call Meta API.**

## Process

### 1. Merge artifacts into YAML
Use schema in `meta_ads_tools/schemas/campaign_draft.schema.json`.

### 2. Structure
```yaml
_meta:
  slug: ...
  status: draft
  created: YYYY-MM-DD
campaign:
  name: ...
  objective: ...
  status: PAUSED  # always PAUSED in template
ad_sets:
  - name: ...
    daily_budget_usd: ...
    targeting: ...
    ads:
      - name: ...
        creative_ref: ...
        copy: { primary_text, headline, ... }
        utm: ...
```

### 3. Validate locally
Run: `python meta_ads_tools/validate_artifact.py campaign-drafts/[slug].yaml`

### 4. Optional: generate payloads
Run: `python meta_ads_tools/build_payloads.py --campaign [slug]`
Outputs to `api-payloads/[slug]/` — still **DRAFT**.

## Output

Save `campaign-drafts/[slug].yaml` with all campaigns, ad sets, ads from strategy.

Include `launch_checklist` section at bottom:

```yaml
launch_checklist:
  - pixel firing verified
  - landing page mobile OK
  - UTMs tested
  - human approved qa-reports
```

## After completion

Ask approval before **Review launch pack** (`meta-ads-07-review-launch-pack`).
