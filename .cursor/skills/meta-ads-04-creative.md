---
name: meta-ads-04-creative
description: Stage 4 — Generate creative concepts, visual/video briefs, hooks, variants, and production notes for Meta ads.
---

# Stage 4 — Creative

Produce creative direction and production-ready briefs (not final rendered assets unless user provides tools). Output: **`creative/[campaign-slug].md`**.

## Inputs

- `strategy/[slug].md` (approved)
- `research/[slug].md`, `intake/[slug].md`
- `.cursor/rules/meta-ads-brand-voice.mdc`
- `learnings/creative-formats.md` if exists

## Skills

- **`copywriting`** — for hook lines on visuals
- **`paid-ads`** — creative testing hierarchy

## Process

### 1. Map ads from strategy table
One section per Ad ID (A1, A2, …).

### 2. Per ad: concept
- **Concept name**
- **Angle & hook** (3 sec / thumb-stop)
- **Format:** static 1:1, 4:5, 9:16 video, carousel
- **Visual description** (scene, text on image, UI mock if SaaS)
- **Motion/script** (for video: scene-by-scene, 15–30s)

### 3. Variants
At least 2 visual directions per priority ad where budget allows.

### 4. Production notes
- Dimensions, safe zones, caption requirement
- AI image prompt OR designer handoff checklist
- Asset filename convention: `creative/[slug]/[ad-id]-[variant].png`

### 5. Policy check on visuals
No before/after body, misleading UI, fake notifications.

## Output template

Save to `creative/[slug].md`:

```markdown
---
slug: "[slug]"
strategy: "strategy/[slug].md"
date: "YYYY-MM-DD"
status: "complete"
---

# Creative: [Campaign name]

## Global direction
- **Visual style:**
- **Talent:** (founder, UGC, no face)
- **Brand elements:**

## Ad A1 — [Concept name]
### Concept
[1 paragraph]

### Hook (on-screen / first frame)
- ...

### Static frame / storyboard
| Beat | Visual | Text overlay | Duration |
|------|--------|--------------|----------|
| 1 | ... | ... | 0-3s |

### Variants
| Variant | Change | Hypothesis |
|---------|--------|------------|
| A1-v1 | ... | ... |
| A1-v2 | ... | ... |

### Production
- **Size:** 1080x1080 / 1080x1920
- **AI prompt / designer brief:**
- **File:** `assets/...`

## Ad A2
[repeat]

## Asset checklist
| Ad ID | Variant | Format | Status |
|-------|---------|--------|--------|
| A1 | v1 | 1:1 | briefed / ready |

## Policy review (creative)
- [ ] Pass — notes:
```

## After completion

Ask approval before **Copy** (`meta-ads-05-copy`).
