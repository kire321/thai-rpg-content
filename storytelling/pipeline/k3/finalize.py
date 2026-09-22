#!/usr/bin/env python3
"""K3 experiment — stage 2 glue: format an outline+script into episode JSON.

Usage: python3 finalize.py --config run_config.json --outline outline.md --script script.md --out ep.json
Only structural FATALs block output (schema/place/speaker/tag-marker mapping) —
the literary lint suite is discarded for this experiment.
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
import driver

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--outline", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    cfg = json.load(open(a.config))
    prose = open(a.outline if False else a.script).read()
    plan = open(a.outline).read()

    name_map = driver.build_name_map()
    chars = driver.load_json(os.path.join(driver.REPO_PUBLIC, "characters.json"))
    places_json = driver.load_json(os.path.join(driver.REPO_PUBLIC, "places.json"))
    char_ids = {c["id"] for c in chars}
    allowed_place_ids = set(cfg["places"]) | {"place_veranda"}

    used_tags = sorted(set(re.findall(r"\[\[(tag_\d+)\]\]", prose)))
    print(f"tags used in script: {used_tags}")

    ep, errors, fatal = driver.format_episode(
        prose, plan, cfg["ep_id"], used_tags, name_map, char_ids,
        places_json, allowed_place_ids)
    print("ERRORS:")
    for e in errors:
        print("  -", e)
    if fatal:
        print("FATAL:")
        for f in fatal:
            print("  -", f)
        sys.exit(1)
    json.dump(ep, open(a.out, "w"), ensure_ascii=False, indent=1)
    n_thai = sum(1 for c in json.dumps(ep, ensure_ascii=False) if '\u0e00' <= c <= '\u0e7f')
    print(f"wrote {a.out} — acts={len(ep['acts'])} tags={sum(1 for act in ep['acts'] for s in act['segments'] if s['type']=='tag')} thai_chars={n_thai}")

if __name__ == "__main__":
    main()
