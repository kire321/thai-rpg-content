#!/usr/bin/env python3
"""Merge per-episode JSONs into public/episodes.json, ordered by episode number.
Usage: python3 assemble.py --episodes-dir /path/to/episodes --out public/episodes.json
"""
import argparse, json, os, re, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    eps = []
    for fn in os.listdir(args.episodes_dir):
        if fn.endswith(".json"):
            with open(os.path.join(args.episodes_dir, fn), encoding="utf-8") as f:
                eps.append(json.load(f))
    eps.sort(key=lambda e: int(re.search(r"\d+", e["id"]).group()))
    tmp = args.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(eps, f, ensure_ascii=False, indent=1)
    os.rename(tmp, args.out)
    print(f"wrote {len(eps)} episodes -> {args.out}")
    print("first:", eps[0]["id"], eps[0]["title"], "| last:", eps[-1]["id"], eps[-1]["title"])

if __name__ == "__main__":
    main()
