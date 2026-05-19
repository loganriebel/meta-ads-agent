# First-time setup (10–15 minutes)

Use this checklist once after cloning. The pipeline reads **`meta-ads-config.yaml`**, **`.cursor/rules/meta-ads-brand-voice.mdc`**, and **`AGENTS.md`** on every run. Placeholder values trigger the setup wizard in `.cursor/skills/meta-ads-01-intake.md`.

## 1. Clone and open in Cursor

```bash
git clone https://github.com/loganriebel/meta-ads-agent.git
cd meta-ads-agent
```

Open the folder in Cursor (or your editor with AI agent support).

## 2. Configure your business

**Option A — manual:** Copy [`meta-ads-config.example.yaml`](meta-ads-config.example.yaml) to `meta-ads-config.yaml` if needed, then edit:

- `business.name`, `business.domain`, `business.primary_offer_url`
- `meta.account_id`, `meta.pixel_id` (optional placeholders until you launch)
- `brand_voice` (tone, audience, topics)
- `campaign_defaults` (objective, placements, budget guardrails)
- `metrics_thresholds` (CPA, ROAS, spend minimums for decisions)

**Option B — guided:** Ask the agent to run **meta-ads-01-intake**. It walks through questions and writes `intake/[campaign-slug].md` plus updates config where appropriate.

## 3. Brand voice rule file

Edit [`.cursor/rules/meta-ads-brand-voice.mdc`](.cursor/rules/meta-ads-brand-voice.mdc): replace template sections with your real audience, tone, and creative standards.

## 4. Business context for the agent

Fill in [`AGENTS.md`](AGENTS.md) so intake and strategy use **your** ICP, offer, proof, and compliance constraints.

## 5. Safety rules

Read [`.cursor/rules/meta-ads-safety.mdc`](.cursor/rules/meta-ads-safety.mdc). This repo never executes live budget changes or Meta API calls.

## 6. Paths and tools (optional)

Default paths are repo-relative (`intake/`, `research/`, etc.). If you embed this folder in a monorepo, adjust `paths.*` in `meta-ads-config.yaml`.

## 7. Quick validation

From repo root (Python 3.10+):

```bash
python meta_ads_tools/validate_config.py meta-ads-config.yaml
```

## 8. Start a campaign

Ask your agent: *Start a new Meta ads campaign for [offer]* and follow **meta-ads** stage by stage, approving each stage before the next.

Try the demo: see [`examples/demo-campaign/`](examples/demo-campaign/).

---

## Template maintenance

**Project-specific campaigns** should live in **your** fork — not in the public template. Fork if you need a stable custom copy.
