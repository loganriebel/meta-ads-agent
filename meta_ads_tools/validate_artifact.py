#!/usr/bin/env python3
"""Validate stage artifacts: markdown frontmatter or campaign YAML drafts."""

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

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore

SCHEMA_DIR = Path(__file__).parent / "schemas"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

STAGE_REQUIRED_SECTIONS: dict[str, list[str]] = {
    "intake": ["# Campaign Intake", "## Offer", "## Success criteria"],
    "research": ["# Research", "## Angle hypotheses", "## Policy flags"],
    "strategy": ["# Strategy", "## Hypotheses", "## Decision rules"],
    "creative": ["# Creative", "## Asset checklist"],
    "copy": ["# Ad Copy", "## Policy review"],
    "analysis": ["# Performance Analysis", "## Decision table"],
    "qa": ["# QA / Launch Pack", "## Launch steps"],
}


def load_schema(name: str) -> dict | None:
    path = SCHEMA_DIR / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def validate_markdown(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append("Missing YAML frontmatter (--- ... ---)")
        return errors

    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid frontmatter: {e}")
        return errors

    if not isinstance(fm, dict):
        errors.append("Frontmatter must be a mapping")
        return errors

    for key in ("slug", "date", "status"):
        if key not in fm:
            errors.append(f"Frontmatter missing: {key}")

    stage = None
    parent = path.parent.name
    if parent in ("intake", "research", "strategy", "creative", "copy", "analysis"):
        stage = parent
    elif parent == "qa-reports":
        stage = "qa"

    if stage and stage in STAGE_REQUIRED_SECTIONS:
        for section in STAGE_REQUIRED_SECTIONS[stage]:
            if section not in text:
                errors.append(f"Missing section: {section}")

    return errors


def validate_campaign_yaml(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"Invalid YAML: {e}"]

    if not isinstance(data, dict):
        return ["Root must be a mapping"]

    schema = load_schema("campaign_draft.schema.json")
    if jsonschema and schema:
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
            errors.append(f"Schema: {err.message} at {list(err.path)}")
    else:
        for key in ("_meta", "campaign", "ad_sets"):
            if key not in data:
                errors.append(f"Missing key: {key}")
        if data.get("_meta", {}).get("status") != "draft":
            errors.append("_meta.status should be 'draft' until human approval")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pipeline artifacts")
    parser.add_argument("path", type=Path, help="File to validate (.md or .yaml)")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"FAIL: {args.path} not found", file=sys.stderr)
        return 1

    suffix = args.path.suffix.lower()
    if suffix in (".md", ".markdown"):
        errors = validate_markdown(args.path)
    elif suffix in (".yaml", ".yml"):
        errors = validate_campaign_yaml(args.path)
    else:
        print(f"FAIL: unsupported file type {suffix}", file=sys.stderr)
        return 1

    if errors:
        print(f"FAIL: {args.path}")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"PASS: {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
