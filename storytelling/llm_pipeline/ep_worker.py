#!/usr/bin/env python3
"""Generate one episode: call deepseek-v4-flash, parse, validate, write JSON.
Usage: python3 ep_worker.py --index N [--packages path] [--outdir dir]
Writes: outdir/episodes/{ep_id}.json, outdir/raw/{ep_id}.md, appends to manifest.jsonl
"""
import argparse, json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ep_lib

def call_model(prompt, max_api_tries=4):
    key = open(ep_lib.KEY_PATH).read().strip()
    body = {"model": ep_lib.MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 16000}
    last_err = None
    for t in range(max_api_tries):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(body).encode(),
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            resp = json.load(urllib.request.urlopen(req, timeout=1800))
            msg = resp["choices"][0]["message"]["content"]
            if msg:
                return msg, resp.get("usage", {})
            last_err = "empty content"
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
        time.sleep(min(60, 15 * (t + 1)))
    raise RuntimeError(f"API failed after {max_api_tries} tries: {last_err}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, required=True)
    ap.add_argument("--packages", default=f"{ep_lib.WORK}/packages.json")
    ap.add_argument("--outdir", default=ep_lib.WORK)
    args = ap.parse_args()

    packages = json.load(open(args.packages))
    package = packages[args.index]
    ep_id = package["episode_id"]
    epdir = os.path.join(args.outdir, "episodes")
    rawdir = os.path.join(args.outdir, "raw")
    os.makedirs(epdir, exist_ok=True)
    os.makedirs(rawdir, exist_ok=True)
    json_path = os.path.join(epdir, f"{ep_id}.json")
    if os.path.exists(json_path):
        print(f"[skip] {ep_id} exists")
        return 0

    prompt = ep_lib.build_prompt(package)
    entry = {"index": args.index, "ep_id": ep_id, "attempts": 0,
             "prompt_tokens": 0, "completion_tokens": 0, "issues": [], "status": "failed"}
    episode, issues = None, []
    for attempt in range(3):
        entry["attempts"] += 1
        try:
            md, usage = call_model(prompt)
            entry["prompt_tokens"] += usage.get("prompt_tokens", 0)
            entry["completion_tokens"] += usage.get("completion_tokens", 0)
        except Exception as e:
            entry["issues"].append(f"api:{e}")
            time.sleep(30)
            continue
        with open(os.path.join(rawdir, f"{ep_id}_try{attempt}.md"), "w") as f:
            f.write(md)
        episode, issues = ep_lib.parse_episode(md, package)
        if episode is not None and not any(i.endswith("blocksize") or "markers" in i or "unparsed" in i for i in issues):
            entry["status"] = "patched" if issues else "ok"
            entry["issues"] = issues
            break
        episode = None
        entry["issues"] = issues or ["unparsed"]
        time.sleep(10)

    if episode is not None:
        tmp = json_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(episode, f, ensure_ascii=False, indent=1)
        os.rename(tmp, json_path)
    with open(os.path.join(args.outdir, "manifest.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[{entry['status']}] {ep_id} attempts={entry['attempts']} issues={entry['issues']}")
    return 0 if episode is not None else 1

if __name__ == "__main__":
    sys.exit(main())
