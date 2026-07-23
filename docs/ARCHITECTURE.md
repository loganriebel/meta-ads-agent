# Architecture — the production Meta ads agent

This repo holds the public reference implementation: staged skills, artifacts on disk, draft-only
API payloads. This document describes the **production agent** the approach grew into, which runs on
Claude Code skills against a real ad account. That code is private; the design is not, and the
design is the part worth reading.

## The shape of it

Nine stages. Each one writes a file the next one reads. That is the whole architecture.

| # | Stage | Artifact |
|---|-------|----------|
| 1 | Research | Angles: pains, hooks, desired outcomes |
| 2 | Copy | Copy variants — headline, primary text, CTA |
| 3 | Image prompts | Prompt manifest paired to each copy variant |
| 4 | Assets | Rendered creative batch plus metadata |
| 5 | Compliance | Pass/fail screening report per creative |
| 6 | Publish | Ad IDs, written through the proxy |
| 7 | Performance | Winner / loser / undecided classification |
| 8 | Budget | Budget action log, written through the proxy |
| 9 | Brief update | Updated patterns file (weekly, across sprints) |

Why files instead of a message-passing pipeline: state is auditable with a file browser. There is no
daemon and no queue. A human can open any stage's output, see exactly what the agent decided, and
resume from there. Resume detection reads a sprint index first and the artifacts second.

One agent owns the whole pipeline. The stage skills exist for **context control** — load only the
stage you are on — not as handoffs between separate agents.

## Human gates

Every stage transition ends with an approval gate. The agent summarizes what it produced, names the
decisions it made and the risks it sees, and stops. It never auto-advances.

This is deliberate overhead. The documented failure mode for ad automation is an agent making a
confident wrong call at 3am across an entire account, and gates are what make that structurally
impossible rather than merely unlikely.

## The proxy guarantee

The agent has no path to the Meta Marketing API. Every write goes through a proxy that holds the
token, and the proxy enforces:

- **Allowlisted creates.** Only the object types the pipeline is supposed to make.
- **Forced paused state.** Every created object is written paused. Requests attempting an active
  state are rejected outright, not corrected.
- **Budget ceiling.** Ad-set daily budget is capped well below anything that could matter.
- **A write log.** Every attempted write is appended to an audit log, including the rejected ones.

The distinction that matters: the agent is not *trusted* to stay within limits, it is *unable* to
exceed them. Removing the guardrails takes a human editing the proxy, which is exactly the friction
you want on that particular decision.

## Pruning rules that respect Meta delivery

Naive automation kills ads too fast and traps the account in Meta's learning phase, which needs
roughly 50 optimization events in 7 days to exit. Restarting that clock repeatedly is worse than
running a mediocre ad. So the kill rules are built around delivery mechanics, not dashboards:

- **No raw CTR sorts.** Sorting by CTR on small samples selects for noise.
- **An impression floor** before any creative is eligible to be judged at all.
- **A Bayesian comparison** against the ad-set baseline rather than a threshold on a raw rate.
- **Ad-level pauses only.** Killing a creative pauses the ad. Ad-set structural changes need a much
  higher bar — a minimum runtime and a budget floor — and get batched weekly rather than applied
  continuously.
- **"Undecided" is a real verdict.** Anything that has not cleared the bar stays undecided instead of
  being killed by default.

## Explore quota

If the loop only reinforces what already won, copy homogenizes, Meta starts deprioritizing
near-identical creatives, and measured performance decays while the metrics look fine. So 20–30% of
every batch's slots are reserved for concepts that deliberately test *outside* the accumulated
winners. It is a hard rule in the copy and image stages, not a suggestion, because the whole point is
that it must survive a run where exploring looks locally irrational.

## Tracking

UTMs live in the ad creative's URL tags, applied at publish, with Meta's macros filling in campaign
and ad identifiers. They are never baked into the copy at the writing stage — the copy stage only
picks which landing page a variant points at, and the publisher resolves the final URL. One place
owns tracking, so it cannot drift per variant.

## Feedback layer

Published ad metadata, performance snapshots, and classifications go to Postgres. Stage 9 reads
across sprints weekly and rewrites the patterns file that stages 2 and 3 are briefed from.

That write-back is the actual product. Everything before it is creative production, which is
valuable but not compounding. The loop closing is what makes each sprint start smarter than the
last — and it is structured file updates, not model fine-tuning, which means a human can read the
diff and disagree with it.
