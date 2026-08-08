#!/usr/bin/env python3
"""Repair the handful of legacy line references left by an old generator."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODES_PATH = ROOT / "public" / "episodes.json"

# These were descriptive aliases emitted by an old batch prompt.  The catalog
# now has the corresponding canonical reusable characters.
CHARACTER_ALIASES = {
    "char_listener_monk": "char_monk",
    "char_singer_echo": "char_chanida",
    "char_cartographer": "char_ampa",
    "char_inquisitor": "char_kamon",
    "char_tam": "char_thanet",
    "char_groundless": "char_prayut",
    "char_lead_enforcer": "char_kamon",
}


def main():
    episodes = json.loads(EPISODES_PATH.read_text(encoding="utf-8"))
    replacements = 0

    def visit(value):
        nonlocal replacements
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "character" and child in CHARACTER_ALIASES:
                    value[key] = CHARACTER_ALIASES[child]
                    replacements += 1
                else:
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(episodes)
    EPISODES_PATH.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"canonicalized {replacements} legacy character references")


if __name__ == "__main__":
    main()
