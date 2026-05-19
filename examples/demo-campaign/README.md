# Demo campaign: `demo-campaign`

Fictional **B2B SaaS free trial** campaign showing the full pipeline. Safe to copy as a reference; do not treat metrics as real.

## Artifacts in this folder

| Stage | File |
|-------|------|
| 1 Intake | [intake.md](intake.md) |
| 2 Research | [research.md](research.md) |
| 3 Strategy | [strategy.md](strategy.md) |
| 4 Creative | [creative.md](creative.md) |
| 5 Copy | [copy.md](copy.md) |
| 6 Build | [campaign-draft.yaml](campaign-draft.yaml) |
| 7 QA | [qa-report.md](qa-report.md) |
| 8 Metrics | [metrics.csv](metrics.csv) |
| 8 Analysis | [analysis.md](analysis.md) |
| 9 Learnings | [learnings-append.md](learnings-append.md) |

Copies also exist at repo root paths (`intake/demo-campaign.md`, etc.) for router resume demos.

## Try the tools

```bash
pip install -r requirements.txt
python meta_ads_tools/validate_artifact.py examples/demo-campaign/intake.md
python meta_ads_tools/validate_artifact.py campaign-drafts/demo-campaign.yaml
python meta_ads_tools/build_payloads.py --campaign demo-campaign
python meta_ads_tools/analyze_metrics.py --metrics examples/demo-campaign/metrics.csv --slug demo-campaign
```

Payloads output: `api-payloads/demo-campaign/` (DRAFT only).
