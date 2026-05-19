---
name: meta-ads-05-copy
description: Stage 5 — Generate primary text, headlines, descriptions, CTAs, and UTM plans for each ad variant.
---

# Stage 5 — Copy

Write Meta ad copy aligned to creative and strategy. Output: **`copy/[campaign-slug].md`**.

## Inputs

- `strategy/[slug].md`, `creative/[slug].md` (approved)
- `intake/[slug].md`, `meta-ads-config.yaml` (`utm`)
- `.cursor/rules/meta-ads-brand-voice.mdc`

## Skills (invoke via Skill tool)

1. **`copywriting`** — before writing variants
2. **`writing-clearly-and-concisely`** — body primary text
3. **`humanizer`** — final pass (keep specifics; remove AI filler)

## Process

### Per Ad ID in strategy
- **Primary text** — short (≤125 chars) + medium + long optional
- **Headline** — ≤40 chars target
- **Description** — optional
- **Link description** — if used
- **CTA button** — Sign Up, Learn More, etc.
- **UTM** — build from `utm` templates with `{campaign_slug}`, `{ad_name}`

### Variant matrix
Match creative variants (A1-v1, A1-v2). Minimum 2 primary texts per priority ad.

### Banned patterns
No "In today's digital landscape," guaranteed ROI, personal attribute callouts ("Are you a stressed mom?").

## Output template

Save to `copy/[slug].md`:

```markdown
---
slug: "[slug]"
strategy: "strategy/[slug].md"
creative: "creative/[slug].md"
date: "YYYY-MM-DD"
status: "complete"
---

# Ad Copy: [Campaign name]

## UTM defaults
- source: facebook
- medium: paid_social
- campaign: [slug]

## Ad A1-v1
| Field | Copy |
|-------|------|
| Primary (short) | |
| Primary (long) | |
| Headline | |
| Description | |
| CTA | |
| URL | https://...?utm_source=... |

## Ad A1-v2
[repeat]

## Ad A2
[repeat]

## Copy testing notes
| Pair | What differs | Hypothesis |
|------|--------------|------------|
| A1-v1 vs v2 | hook | CTR |

## Policy review (copy)
- [ ] Pass
```

## After completion

Ask approval before **Build drafts** (`meta-ads-06-build-drafts`).
