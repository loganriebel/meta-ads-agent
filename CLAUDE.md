# Meta Ads Agent — project memory

Update this file when you change pipeline behavior or ship campaigns so future sessions stay consistent.

## What this is

A **standalone** Cursor pipeline repo for **Meta/Facebook/Instagram ads only**. The router is **`.cursor/skills/meta-ads.md`**. Each stage has its own skill file. Configuration lives in **`meta-ads-config.yaml`**; voice in **`.cursor/rules/meta-ads-brand-voice.mdc`**; positioning in **`AGENTS.md`**.

## First run

1. Complete **SETUP.md** (or run `meta-ads-01-intake`).
2. Remove placeholder values from `meta-ads-config.yaml` (`YOUR_BUSINESS_NAME`, `yourdomain.com`, etc.).

## Artifact paths (default)

Defined under `paths` in `meta-ads-config.yaml`:

| Area | Location |
|------|----------|
| Intake | `intake/` |
| Research | `research/` |
| Strategy | `strategy/` |
| Creative | `creative/` |
| Copy | `copy/` |
| Campaign drafts | `campaign-drafts/` |
| API payloads (drafts) | `api-payloads/` |
| Metrics | `metrics/` |
| Analysis | `analysis/` |
| Learnings | `learnings/` |
| QA | `qa-reports/` |

## Critical rules

1. **Human approval** between stages.
2. **One stage skill per run** when possible — load only the skill for the current stage.
3. **No live Meta API** — `api-payloads/` are drafts for human review.
4. **Brand voice** — read `meta-ads-brand-voice.mdc` before creative and copy.
5. **Safety** — read `meta-ads-safety.mdc` before build, review, and analysis recommendations.

## Stage map

| # | Skill | Output |
|---|-------|--------|
| 1 | meta-ads-01-intake | `intake/[slug].md` |
| 2 | meta-ads-02-research | `research/[slug].md` |
| 3 | meta-ads-03-strategy | `strategy/[slug].md` |
| 4 | meta-ads-04-creative | `creative/[slug].md` |
| 5 | meta-ads-05-copy | `copy/[slug].md` |
| 6 | meta-ads-06-build-drafts | `campaign-drafts/[slug].yaml` |
| 7 | meta-ads-07-review-launch-pack | `qa-reports/[slug].md`, `api-payloads/[slug]/` |
| 8 | meta-ads-08-performance-analysis | `analysis/[slug].md` |
| 9 | meta-ads-09-learning-loop | `learnings/*.md` updates |

## Key files

| File | Purpose |
|------|---------|
| `meta-ads-config.yaml` | Account config, paths, thresholds |
| `SETUP.md` | First-time checklist |
| `AGENTS.md` | Business context for agents |
| `.cursor/rules/meta-ads-brand-voice.mdc` | Voice and creative standards |
| `.cursor/rules/meta-ads-safety.mdc` | Safety and policy guardrails |
| `.cursor/rules/meta-ads-first-run.mdc` | Placeholder gate |
| `.cursor/skills/meta-ads.md` | Router |
| `meta_ads_tools/` | Validation and helpers |

---

## Campaign inventory

### Active / in pipeline

| Slug | Offer | Stage | Notes |
|------|-------|-------|-------|
| `demo-campaign` | Example SaaS trial | complete (example) | See `examples/demo-campaign/` |

### Shipped (live in Meta)

| Slug | Objective | Launched | Notes |
|------|-----------|----------|-------|
| *(add rows as you launch)* | | | |

---

## Changelog

- 2026-05-18 — Initial portfolio template scaffold.
