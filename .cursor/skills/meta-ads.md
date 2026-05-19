---
name: meta-ads
description: Router for the Meta (Facebook/Instagram) ads pipeline. Detects current stage from artifacts and directs to the correct stage skill. Use when starting or resuming a campaign.
---

# Meta Ads — pipeline router

You orchestrate **which stage skill to run** for a Meta ads campaign. You do **not** run all stages in one session unless the user explicitly asks. Load **only** the stage skill needed.

## Mandatory context (read once per session)

1. `AGENTS.md` — business, ICP, compliance
2. `meta-ads-config.yaml` — paths, defaults, thresholds
3. `.cursor/rules/meta-ads-first-run.mdc` — stop if placeholders remain
4. `.cursor/rules/meta-ads-safety.mdc` — before build, review, or analysis
5. `learnings/` — skim `hooks.md`, `angles.md`, `audiences.md` if they exist

## First-run check

If `business.name` is `YOUR_BUSINESS_NAME` or `business.domain` is `yourdomain.com`, open **meta-ads-01-intake** and run setup — do not skip to later stages.

## Stage skills

| Stage | Skill file | Primary artifact |
|-------|------------|------------------|
| 1 | `meta-ads-01-intake.md` | `intake/[slug].md` |
| 2 | `meta-ads-02-research.md` | `research/[slug].md` |
| 3 | `meta-ads-03-strategy.md` | `strategy/[slug].md` |
| 4 | `meta-ads-04-creative.md` | `creative/[slug].md` |
| 5 | `meta-ads-05-copy.md` | `copy/[slug].md` |
| 6 | `meta-ads-06-build-drafts.md` | `campaign-drafts/[slug].yaml` |
| 7 | `meta-ads-07-review-launch-pack.md` | `qa-reports/[slug].md`, `api-payloads/[slug]/` |
| 8 | `meta-ads-08-performance-analysis.md` | `analysis/[slug].md` |
| 9 | `meta-ads-09-learning-loop.md` | `learnings/*.md` |

Paths come from `meta-ads-config.yaml` → `paths`.

## How to determine current stage (resume)

Given **campaign slug** (e.g. `q2-trial-push`), check **reverse order**:

1. `learnings/` updated with this slug in changelog **and** user wants next cycle → **Stage 9** or new **Stage 1**
2. `analysis/[slug].md` exists, no new learning pass requested → **Stage 9** if user wants learnings; else done
3. `metrics/` has export for slug, no `analysis/[slug].md` → **Stage 8**
4. `qa-reports/[slug].md` with status approved, campaign live, metrics pending → wait for metrics; **Stage 8** when ready
5. `api-payloads/[slug]/` or `qa-reports/[slug].md` exists, not approved → **Stage 7**
6. `campaign-drafts/[slug].yaml` exists → **Stage 7** (if not yet reviewed) or **Stage 6** (if user wants edits)
7. `copy/[slug].md` exists, no campaign draft → **Stage 6** (after creative approved)
8. `creative/[slug].md` exists, no copy → **Stage 5** (strategy must be approved)
9. `strategy/[slug].md` exists → **Stage 4** or **5** (creative before copy; both need strategy approval)
10. `research/[slug].md` exists → **Stage 3**
11. `intake/[slug].md` exists → **Stage 2**
12. Nothing → **Stage 1**

**Parallel note:** Stages 4 and 5 both require approved strategy. Default order: **4 Creative → 5 Copy → 6 Build**.

If ambiguous, list artifacts found and ask which stage to run.

## Invoking external skills (when relevant)

| When | Skill |
|------|-------|
| Ad copy, headlines, CTAs | `copywriting` |
| Clarity in prose | `writing-clearly-and-concisely` |
| Paid strategy framing | `paid-ads` |
| Policy-sensitive copy pass | `humanizer` (light touch — do not remove specifics) |

## Critical rules

1. **Human gates** — never auto-advance stages.
2. **One stage per session** unless user requests multiple with approval between each.
3. **No live Meta API** — drafts only in `api-payloads/`.
4. Open the **target stage skill** and follow it completely for that stage.

## User prompts

- *Start a new Meta campaign for [offer]* → Stage 1
- *Resume campaign [slug]* → detect stage above
- *Run performance analysis for [slug]* → Stage 8
- *Update learnings from [slug]* → Stage 9

Tell the user which stage skill you are opening and why.
