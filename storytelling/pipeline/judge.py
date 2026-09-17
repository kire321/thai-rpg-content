#!/usr/bin/env python3
"""OR-judge scaffold (sprint-8 infra): score a shipped episode with
deepseek-v3.2 (~$0.005/episode). Output is a report the human editor
adjudicates — never a ship gate.

Usage: OPENROUTER_API_KEY=... python3 judge.py EP_JSON PLAN_MD OUT_MD
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import call_llm  # noqa: E402


class _Usage:
    def add(self, *a):
        return (0, 0)


def episode_text(ep):
    out = []
    for a in ep.get("acts", []):
        out.append(f"## {a.get('id')} — {a.get('title')}")
        for s in a.get("segments", []):
            if s.get("type") == "narrative":
                for ln in s.get("lines", []):
                    sd = f" [{ln['stage_directions']}]" if ln.get("stage_directions") else ""
                    who = "NARRATOR" if ln.get("character") == "narrator" else ln.get("character")
                    out.append(f"{who}:{sd} {ln.get('dialogue', '')}")
            elif s.get("type") == "tag":
                out.append(f"[[{s.get('tag') or s.get('tag_id')}]]")
        d = a.get("decision") or {}
        if d:
            out.append("DECISION: " + (d.get("line") or {}).get("dialogue", ""))
            for c in d.get("choices", []):
                out.append(f"  [{c.get('difficulty')}] {c.get('description')} "
                           f"PASS: {c.get('pass')} FAIL: {c.get('fail')}")
    return "\n".join(out)


RUBRIC = """You are a literary judge for an educational RPG script (canal-side Siam, 1910s-1950s).
Score the episode on three axes, 1-5 each, with ONE sentence of evidence per axis:

1. MOTIVATION-INVENTORY: do inventories (lists of concrete items) demonstrate the
   collector's motivation and feed the plot — or are they decorative lists?
2. FLOW: does every line follow causally from the previous one (no non-sequiturs,
   no dropped threads, choices rooted in what the story established)?
3. ANCHOR-SEMANTICS: at each [[tag_xxx]] marker, does the preceding line's English
   anchor word genuinely unify the tag's theme with the scene — or is it pasted in?

Answer EXACTLY in this format:
MOTIVATION-INVENTORY: <1-5> — <one sentence>
FLOW: <1-5> — <one sentence>
ANCHOR-SEMANTICS: <1-5> — <one sentence>
WEAKEST LINE: <quote the single weakest line and say why in one sentence>
STRONGEST LINE: <quote the single strongest line and say why in one sentence>"""


def main():
    ep_path, plan_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    ep = json.load(open(ep_path))
    plan = open(plan_path).read() if os.path.exists(plan_path) else ""
    text = episode_text(ep)
    user = (RUBRIC + "\n\n## EPISODE SCRIPT\n" + text +
            "\n\n## TAG ANCHORS (from the plan)\n" +
            "\n".join(re.findall(r"^-\s*tag_\d+[^\n]*$", plan, re.M)[:8]))
    msg, _ = call_llm("deepseek/deepseek-v3.2",
                      "You are a terse, evidence-quoting literary judge.",
                      user, 0.3, 2000, _Usage(), "judge")
    scores = dict(re.findall(r"(MOTIVATION-INVENTORY|FLOW|ANCHOR-SEMANTICS):\s*(\d)", msg))
    report = (f"# OR-judge report — {ep.get('id', ep_path)}\n\n"
              f"model: deepseek/deepseek-v3.2 (warn-only; editor adjudicates)\n\n" + msg +
              f"\n\n## parsed scores: {scores}\n")
    open(out_path, "w").write(report)
    print(f"[judge] wrote {out_path} — scores {scores}")


if __name__ == "__main__":
    main()
