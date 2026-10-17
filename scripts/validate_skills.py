#!/usr/bin/env python3
"""Check the independent package manifest and distributable skill entries."""

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"cadcraft-use", "cadcraft-cli", "cadcraft-mcp"}


def validate() -> None:
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != "cadcraft-skills":
        raise ValueError("invalid package name")
    paths = manifest.get("skills")
    if not isinstance(paths, list) or len(paths) != len(set(paths)) or not {f"./skills/{name}" for name in EXPECTED} <= set(paths):
        raise ValueError("skill manifest differs from package contents")
    actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    if {f"./skills/{name}" for name in actual} != set(paths):
        raise ValueError("skill directory set differs from manifest")
    for name in actual:
        path = ROOT / "skills" / name / "SKILL.md"
        content = path.read_text(encoding="utf-8")
        if len(content.splitlines()) >= 500:
            raise ValueError(f"skill is too long: {name}")
        if not re.match(rf"\A---\nname: {re.escape(name)}\ndescription: .+\n(?:[a-z_]+: [^\n]+\n)*---\n", content):
            raise ValueError(f"skill frontmatter is invalid: {name}")
        if re.search(r"\]\(\.\./[^)]+\)", content):
            raise ValueError(f"cross-skill relative link: {name}")
    print("CADCraft skill package valid")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"cadcraft-skills: {exc}", file=sys.stderr)
        sys.exit(1)
