#!/usr/bin/env python3
"""Validate meta-ads-config.yaml for placeholders and threshold sanity."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

PLACEHOLDER_PATTERNS = [
    re.compile(r"YOUR_BUSINESS_NAME", re.I),
    re.compile(r"yourdomain\.com", re.I),
    re.compile(r"YOUR_TONE", re.I),
    re.compile(r"YOUR_AUDIENCE", re.I),
    re.compile(r"YOUR_PRIMARY_TOPIC", re.I),
]

REQUIRED_TOP_KEYS = ("business", "meta", "campaign_defaults", "budget_guardrails", "metrics_thresholds", "paths")


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("Config root must be a mapping")
    return data


def check_placeholders(config: dict) -> list[str]:
    errors: list[str] = []
    text = yaml.dump(config)
    for pat in PLACEHOLDER_PATTERNS:
        if pat.search(text):
            errors.append(f"Placeholder detected: {pat.pattern}")
    if config.get("meta", {}).get("api_mode") != "draft_only":
        errors.append('meta.api_mode must be "draft_only" in this template')
    return errors


def check_thresholds(config: dict) -> list[str]:
    warnings: list[str] = []
    mt = config.get("metrics_thresholds") or {}
    bg = config.get("budget_guardrails") or {}

    target_cpa = mt.get("target_cpa_usd")
    kill_mult = mt.get("kill_cpa_multiplier", 1.5)
    if target_cpa is not None and kill_mult <= 1:
        warnings.append("kill_cpa_multiplier should be > 1 for meaningful kill rules")

    max_daily = bg.get("max_daily_budget_usd", 0)
    default_daily = config.get("campaign_defaults", {}).get("daily_budget_usd", 0)
    if default_daily > max_daily:
        warnings.append(
            f"campaign_defaults.daily_budget_usd ({default_daily}) exceeds "
            f"budget_guardrails.max_daily_budget_usd ({max_daily})"
        )

    scale_pct = bg.get("max_scale_increase_percent", 30)
    if scale_pct > 50:
        warnings.append("max_scale_increase_percent > 50% is aggressive for Meta learning")

    return warnings


def check_paths(config: dict) -> list[str]:
    errors: list[str] = []
    paths = config.get("paths") or {}
    for key in (
        "intake",
        "research",
        "strategy",
        "creative",
        "copy",
        "campaign_drafts",
        "api_payloads",
        "metrics",
        "analysis",
        "learnings",
        "qa_reports",
    ):
        if key not in paths:
            errors.append(f"Missing paths.{key}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate meta-ads-config.yaml")
    parser.add_argument("config", type=Path, nargs="?", default=Path("meta-ads-config.yaml"))
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Treat placeholder values as warnings (for untouched template clones)",
    )
    args = parser.parse_args()

    if not args.config.exists():
        print(f"FAIL: {args.config} not found", file=sys.stderr)
        return 1

    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1

    errors: list[str] = []
    for key in REQUIRED_TOP_KEYS:
        if key not in config:
            errors.append(f"Missing top-level key: {key}")

    warnings: list[str] = []
    placeholder_errors = check_placeholders(config)
    if args.allow_placeholders:
        for e in placeholder_errors:
            warnings.append(e.replace("Placeholder detected: ", "Placeholder: "))
    else:
        errors.extend(placeholder_errors)
    errors.extend(check_paths(config))
    warnings.extend(check_thresholds(config))

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"  ERROR: {e}")
        return 1

    print("VALIDATION PASSED")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  WARN: {w}")
    else:
        print("No warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
