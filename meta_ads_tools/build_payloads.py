#!/usr/bin/env python3
"""Build draft Meta Marketing API payload JSON files from campaign-drafts YAML."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)


def load_config(config_path: Path) -> dict:
    with config_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_draft(repo_root: Path, slug: str, config: dict) -> dict:
    drafts_dir = Path(config.get("paths", {}).get("campaign_drafts", "campaign-drafts/"))
    path = repo_root / drafts_dir / f"{slug}.yaml"
    if not path.exists():
        path = repo_root / "examples" / slug / "campaign-draft.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No campaign draft for slug '{slug}' at {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def payload_meta(slug: str, entity_type: str, warning: str | None = None) -> dict:
    meta = {
        "status": "draft",
        "reviewed_by_human": False,
        "slug": slug,
        "entity_type": entity_type,
    }
    if warning:
        meta["warning"] = warning
    return meta


def build_campaign_payload(slug: str, draft: dict, config: dict) -> dict:
    campaign = draft["campaign"]
    account_id = config.get("meta", {}).get("account_id") or "act_REPLACE_ME"
    warning = None if config.get("meta", {}).get("account_id") else "Set meta.account_id before any real API use"

    body = {
        "name": campaign["name"],
        "objective": campaign.get("objective", config.get("campaign_defaults", {}).get("objective")),
        "status": campaign.get("status", "PAUSED"),
        "special_ad_categories": [],
        "buying_type": campaign.get("buying_type", config.get("campaign_defaults", {}).get("buying_type", "AUCTION")),
    }

    return {
        "_meta": payload_meta(slug, "campaign", warning),
        "endpoint": f"/v21.0/{account_id}/campaigns",
        "method": "POST",
        "body": body,
    }


def build_ad_set_payload(slug: str, ad_set: dict, config: dict, campaign_name: str) -> dict:
    account_id = config.get("meta", {}).get("account_id") or "act_REPLACE_ME"
    daily = ad_set.get("daily_budget_usd", config.get("campaign_defaults", {}).get("daily_budget_usd", 50))
    # Meta uses cents for some endpoints; document in warning
    body = {
        "name": ad_set["name"],
        "campaign_id": "{{campaign_id}}",
        "daily_budget": int(daily * 100),
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "bid_strategy": config.get("campaign_defaults", {}).get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
        "status": "PAUSED",
        "targeting": ad_set.get("targeting", {}),
        "promoted_object": {"pixel_id": config.get("meta", {}).get("pixel_id") or "PIXEL_REPLACE_ME"},
    }

    return {
        "_meta": payload_meta(slug, "ad_set", "Replace campaign_id and verify daily_budget currency units in Meta docs"),
        "endpoint": f"/v21.0/{account_id}/adsets",
        "method": "POST",
        "body": body,
        "notes": {"parent_campaign": campaign_name},
    }


def build_ad_payload(slug: str, ad: dict, ad_set_name: str, config: dict) -> dict:
    account_id = config.get("meta", {}).get("account_id") or "act_REPLACE_ME"
    copy = ad.get("copy", {})
    page_id = config.get("meta", {}).get("page_id") or "PAGE_REPLACE_ME"

    body = {
        "name": ad["name"],
        "adset_id": "{{adset_id}}",
        "status": "PAUSED",
        "creative": {
            "object_story_spec": {
                "page_id": page_id,
                "link_data": {
                    "message": copy.get("primary_text", ""),
                    "name": copy.get("headline", ""),
                    "description": copy.get("description", ""),
                    "link": copy.get("url", config.get("business", {}).get("primary_offer_url", "")),
                    "call_to_action": {"type": copy.get("cta", "LEARN_MORE")},
                },
            },
        },
    }

    return {
        "_meta": payload_meta(slug, "ad", "Upload creative assets separately; link_data is simplified draft"),
        "endpoint": f"/v21.0/{account_id}/ads",
        "method": "POST",
        "body": body,
        "notes": {"parent_ad_set": ad_set_name, "creative_ref": ad.get("creative_ref")},
    }


def write_payload(out_dir: Path, filename: str, payload: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build draft Meta API payloads")
    parser.add_argument("--campaign", required=True, help="Campaign slug")
    parser.add_argument("--config", type=Path, default=Path("meta-ads-config.yaml"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()

    repo = args.repo.resolve()
    config_path = (repo / args.config).resolve()
    if not config_path.exists():
        print(f"FAIL: config not found: {config_path}", file=sys.stderr)
        return 1

    config = load_config(config_path)
    slug = args.campaign

    try:
        draft = load_draft(repo, slug, config)
    except FileNotFoundError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1

    payloads_dir = Path(config.get("paths", {}).get("api_payloads", "api-payloads/"))
    out_dir = repo / payloads_dir / slug

    print(f"Building payloads for '{slug}' -> {out_dir}")

    write_payload(out_dir, "01-campaign.json", build_campaign_payload(slug, draft, config))

    for i, ad_set in enumerate(draft.get("ad_sets", []), start=1):
        safe = re.sub(r"[^\w\-]", "_", ad_set["name"])[:40]
        write_payload(
            out_dir,
            f"02-adset-{i:02d}-{safe}.json",
            build_ad_set_payload(slug, ad_set, config, draft["campaign"]["name"]),
        )
        for j, ad in enumerate(ad_set.get("ads", []), start=1):
            ad_safe = re.sub(r"[^\w\-]", "_", ad["name"])[:30]
            write_payload(
                out_dir,
                f"03-ad-{i:02d}-{j:02d}-{ad_safe}.json",
                build_ad_payload(slug, ad, ad_set["name"], config),
            )

    readme = out_dir / "README.txt"
    readme.write_text(
        "DRAFT API PAYLOADS — HUMAN REVIEW REQUIRED\n"
        "Do not POST to Meta without verifying account IDs, pixel, page, budgets, and creative assets.\n",
        encoding="utf-8",
    )
    print("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
