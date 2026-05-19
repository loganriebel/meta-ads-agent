# meta_ads_tools

Local helpers for the Meta Ads Agent template. **No live Meta API calls.**

| Script | Purpose |
|--------|---------|
| `validate_config.py` | Check YAML config structure, placeholders, thresholds |
| `validate_artifact.py` | Validate stage `.md` frontmatter or `campaign-drafts/*.yaml` |
| `build_payloads.py` | Emit draft JSON under `api-payloads/{slug}/` |
| `analyze_metrics.py` | Classify ads from Ads Manager CSV export |

## Install

```bash
pip install -r requirements.txt
```

## Examples

```bash
python meta_ads_tools/validate_config.py meta-ads-config.yaml --allow-placeholders
python meta_ads_tools/validate_artifact.py intake/demo-campaign.md
python meta_ads_tools/build_payloads.py --campaign demo-campaign
python meta_ads_tools/analyze_metrics.py --metrics examples/demo-campaign/metrics.csv --slug demo-campaign
```

Schemas: `schemas/`
