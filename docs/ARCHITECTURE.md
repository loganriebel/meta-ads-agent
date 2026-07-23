# Architecture: the production Meta ads agent

This repo holds the public reference implementation: staged skills, artifacts on disk, draft-only
API payloads. This document describes the **production agent** the approach grew into, which runs on
Claude Code skills against a real ad account. That code is private. The design isn't, and the design
is the part worth reading.

## Nine stages

Nine stages, each writing a file the next one reads.

| # | Stage | Artifact |
|---|-------|----------|
| 1 | Research | Angles: pains, hooks, desired outcomes |
| 2 | Copy | Copy variants: headline, primary text, CTA |
| 3 | Image prompts | Prompt manifest paired to each copy variant |
| 4 | Assets | Rendered creative batch plus metadata |
| 5 | Compliance | Pass/fail screening report per creative |
| 6 | Publish | Ad IDs, written through the proxy |
| 7 | Performance | Winner / loser / undecided classification |
| 8 | Budget | Budget action log, written through the proxy |
| 9 | Brief update | Updated patterns file (weekly, across sprints) |

Files instead of message passing, because state stays auditable with a file browser. There's no
daemon and no queue. You can open any stage's output, see what the agent decided, and resume from
there. Resume detection reads a sprint index first and the artifacts second.

One agent owns the pipeline. The stage skills exist for **context control**, so only the active
stage loads, and they aren't handoffs between separate agents.

## Human gates

Every stage transition ends with an approval gate. The agent summarizes what it produced, names the
decisions it made and the risks it sees, and stops there until a human says go.

The overhead is deliberate. The documented failure mode for ad automation is an agent making a
confident wrong call at 3am across an entire account, and gates are what make that structurally
impossible.

## The proxy

The agent has no path to the Meta Marketing API. Every write goes through a proxy that holds the
token, and the proxy enforces four things:

- **Allowlisted creates.** Only the object types the pipeline is supposed to make.
- **Forced paused state.** Every created object is written paused. Requests attempting an active
  state get rejected outright, not corrected.
- **Budget ceiling.** Ad-set daily budget is capped well below anything that could matter.
- **A write log.** Every attempted write is appended to an audit log, including the rejected ones.

Those limits are structural. Removing them takes a human editing the proxy, which is the friction I
want on that particular decision.

## Pruning rules that respect Meta delivery

Naive automation kills ads too fast and traps the account in Meta's learning phase, which needs
roughly 50 optimization events in 7 days to exit. Restarting that clock repeatedly costs more than
running a mediocre ad. So the kill rules follow delivery mechanics rather than dashboards:

- **No raw CTR sorts.** Sorting by CTR on small samples selects for noise.
- **An impression floor** before any creative is eligible to be judged.
- **A Bayesian comparison** against the ad-set baseline rather than a threshold on a raw rate.
- **Ad-level pauses only.** Killing a creative pauses the ad. Ad-set structural changes need a much
  higher bar, a minimum runtime and a budget floor, and get batched weekly rather than applied
  continuously.
- **"Undecided" is the verdict most dashboards refuse to give you.** Anything that hasn't cleared
  the bar stays undecided.

## Explore quota

A loop that only reinforces past winners homogenizes its own copy. Meta starts deprioritizing
near-identical creatives, and measured performance decays while the metrics still look fine. So
20-30% of every batch's slots go to concepts that test *outside* the accumulated winners. It's a
hard rule in the copy and image stages, because it has to survive the run where exploring looks
irrational.

## Tracking

UTMs live in the ad creative's URL tags, applied at publish, with Meta's macros filling in campaign
and ad identifiers. They stay out of the copy stage entirely. Stage 2 picks which landing page a
variant points at, and the publisher resolves the final URL. One place owns tracking, so it can't
drift per variant.

## Feedback layer

Published ad metadata, performance snapshots, and classifications go to Postgres. Stage 9 reads
across sprints weekly and rewrites the patterns file that stages 2 and 3 are briefed from.

The write-back is what makes each sprint start from the last one's data instead of the last one's
guesses. Everything before it is creative production, which is useful but doesn't compound. And it's
structured file updates rather than model fine-tuning, so a human can read the diff and disagree
with it.
