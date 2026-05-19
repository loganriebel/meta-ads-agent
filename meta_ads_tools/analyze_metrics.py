#!/usr/bin/env python3
"""Analyze exported Meta ads metrics CSV and recommend kill/scale/hold actions."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

COLUMN_ALIASES = {
    "ad_name": ["ad name", "ad_name", "ad"],
    "ad_set_name": ["ad set name", "ad_set_name", "adset name"],
    "spend": ["amount spent (usd)", "spend", "amount spent"],
    "impressions": ["impressions"],
    "clicks": ["link clicks", "clicks"],
    "conversions": ["results", "conversions", "purchases", "leads"],
    "cpa": ["cost per result", "cpa", "cost per conversion"],
    "roas": ["roas", "purchase roas"],
    "frequency": ["frequency"],
}


def normalize_header(h: str) -> str:
    return h.strip().lower()


def map_columns(fieldnames: list[str]) -> dict[str, str]:
    normalized = {normalize_header(f): f for f in fieldnames}
    mapping: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                mapping[canonical] = normalized[alias]
                break
    return mapping


def parse_float(val: str | None) -> float:
    if val is None or val == "":
        return 0.0
    return float(str(val).replace(",", "").replace("$", "").strip() or 0)


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def classify_row(row: dict, config: dict) -> tuple[str, str]:
    mt = config.get("metrics_thresholds", {})
    bg = config.get("budget_guardrails", {})

    spend = parse_float(row.get("spend"))
    conversions = parse_float(row.get("conversions"))
    impressions = parse_float(row.get("impressions"))
    frequency = parse_float(row.get("frequency"))

    target_cpa = float(mt.get("target_cpa_usd", 75))
    kill_mult = float(mt.get("kill_cpa_multiplier", 1.5))
    target_roas = mt.get("target_roas")
    scale_roas_mult = float(mt.get("scale_roas_multiplier", 1.2))
    min_spend = float(bg.get("min_spend_before_decision_usd", 30))
    min_impr = float(mt.get("min_impressions", 1000))
    freq_fatigue = float(mt.get("frequency_fatigue", 3.0))

    cpa = parse_float(row.get("cpa"))
    if cpa == 0 and conversions > 0:
        cpa = spend / conversions
    roas = parse_float(row.get("roas"))

    if spend < min_spend or impressions < min_impr:
        return "HOLD", f"spend ${spend:.2f} or impressions {impressions:.0f} below minimum"

    if frequency >= freq_fatigue and impressions >= min_impr:
        return "HOLD", f"frequency {frequency:.2f} — possible fatigue; refresh creative"

    if conversions == 0 and spend >= min_spend:
        return "KILL", "spend without conversions"

    if cpa > target_cpa * kill_mult:
        return "KILL", f"CPA ${cpa:.2f} > kill threshold ${target_cpa * kill_mult:.2f}"

    if target_roas is not None and roas > 0:
        if roas >= float(target_roas) * scale_roas_mult:
            return "SCALE", f"ROAS {roas:.2f} above scale threshold"
        if roas < float(target_roas) * 0.8:
            return "KILL", f"ROAS {roas:.2f} below target"

    if cpa > 0 and cpa <= target_cpa:
        return "SCALE", f"CPA ${cpa:.2f} at or below target ${target_cpa:.2f}"

    return "HOLD", "meets minimum data; no strong signal"


def analyze(csv_path: Path, config: dict) -> list[dict]:
    results: list[dict] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        col_map = map_columns(list(reader.fieldnames))
        if "ad_name" not in col_map or "spend" not in col_map:
            raise ValueError(f"Could not map required columns. Found: {reader.fieldnames}")

        for raw in reader:
            row = {k: raw.get(col_map[k], "") for k in col_map}
            action, reason = classify_row(row, config)
            results.append(
                {
                    "ad_name": row.get("ad_name", ""),
                    "ad_set_name": row.get("ad_set_name", ""),
                    "spend": parse_float(row.get("spend")),
                    "conversions": parse_float(row.get("conversions")),
                    "cpa": parse_float(row.get("cpa")) or None,
                    "roas": parse_float(row.get("roas")) or None,
                    "action": action,
                    "reason": reason,
                }
            )
    return results


def print_report(results: list[dict], slug: str) -> None:
    print(f"\n=== Metrics analysis: {slug} ===\n")
    print(f"{'Ad':<30} {'Spend':>10} {'Conv':>6} {'Action':<8} Reason")
    print("-" * 90)
    for r in results:
        cpa_s = f"${r['cpa']:.2f}" if r["cpa"] else "—"
        print(
            f"{r['ad_name'][:30]:<30} ${r['spend']:>8.2f} {r['conversions']:>6.0f} "
            f"{r['action']:<8} {r['reason']}"
        )

    counts = {}
    for r in results:
        counts[r["action"]] = counts.get(r["action"], 0) + 1
    print("\nSummary:", ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Meta ads metrics CSV")
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("meta-ads-config.yaml"))
    parser.add_argument("--slug", default="campaign")
    parser.add_argument("--output", type=Path, help="Write markdown summary")
    args = parser.parse_args()

    if not args.metrics.exists():
        print(f"FAIL: {args.metrics} not found", file=sys.stderr)
        return 1

    config = load_config(args.config)
    try:
        results = analyze(args.metrics, config)
    except ValueError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print_report(results, args.slug)

    if args.output:
        lines = [
            f"# Metrics tool output: {args.slug}\n",
            "| Ad | Spend | Conv | Action | Reason |",
            "|-----|-------|------|--------|--------|",
        ]
        for r in results:
            lines.append(
                f"| {r['ad_name']} | ${r['spend']:.2f} | {r['conversions']:.0f} | "
                f"{r['action']} | {r['reason']} |"
            )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nWrote {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
