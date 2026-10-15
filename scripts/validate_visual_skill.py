#!/usr/bin/env python3
"""Validate the single active visual skill package, not model/client behavior."""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ACTIVE = SKILLS / "visual-explanation"


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid frontmatter: {path}")
    return data


def validate():
    entries = []
    for path in SKILLS.rglob("SKILL.md"):
        data = frontmatter(path)
        if str(data.get("name", "")).startswith("visual-explanation"):
            entries.append(path)
    if entries != [ACTIVE / "SKILL.md"]:
        raise ValueError(f"Expected one active visual skill, found: {entries}")
    directories = sorted(p.name for p in SKILLS.iterdir()
                         if p.is_dir() and p.name.startswith("visual-explanation"))
    if directories != ["visual-explanation"]:
        raise ValueError(f"Duplicate visual directories: {directories}")
    data = frontmatter(ACTIVE / "SKILL.md")
    name = data.get("name")
    if name != ACTIVE.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Skill name must match its directory and use lowercase hyphens")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        raise ValueError("Description must be nonempty")
    version = data.get("metadata", {}).get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("metadata.version must be a semantic version string")
    if data.get("license") != "MIT" or not (ACTIVE / "LICENSE.show-me").is_file():
        raise ValueError("MIT license file is missing or mismatched")
    config = yaml.safe_load((ACTIVE / "agents/openai.yaml").read_text(encoding="utf-8"))
    interface = config["interface"]
    prompt = interface["default_prompt"]
    if "$visual-explanation" not in prompt or "visual-explanation_2" in prompt:
        raise ValueError("UI invocation must use the canonical skill name")
    if not interface.get("display_name") or not interface.get("short_description"):
        raise ValueError("UI labels are missing")
    for target in re.findall(r"\]\(([^)]+)\)", (ACTIVE / "SKILL.md").read_text()):
        if "://" not in target and not target.startswith("#"):
            if not (ACTIVE / target.split("#", 1)[0]).exists():
                raise ValueError(f"Broken runtime reference: {target}")
    return {"status": "passed", "name": name, "version": version,
            "active_visual_entries": len(entries),
            "scope": "package structure and invocation metadata; no native client or generation test"}


if __name__ == "__main__":
    try:
        print(json.dumps(validate(), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        raise SystemExit(str(error))
