#!/usr/bin/env python3
"""Run a range of episode indices through ep_worker.py with P parallel subprocesses.
Resumable: skips episodes whose JSON already exists. Repeats up to --passes times
to retry failures. Usage: python3 lane_runner.py --start 0 --end 34 --parallel 4 --passes 3
"""
import argparse, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ep_lib

def run_one(idx):
    r = subprocess.run([sys.executable, os.path.join(ep_lib.WORK, "ep_worker.py"),
                        "--index", str(idx)],
                       capture_output=True, text=True, timeout=2400)
    out = (r.stdout + r.stderr).strip().splitlines()
    return idx, r.returncode, out[-1] if out else "no-output"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)  # exclusive
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--passes", type=int, default=3)
    args = ap.parse_args()

    packages = json.load(open(f"{ep_lib.WORK}/packages.json"))
    epdir = f"{ep_lib.WORK}/episodes"
    os.makedirs(epdir, exist_ok=True)

    for p in range(args.passes):
        pending = [i for i in range(args.start, args.end)
                   if not os.path.exists(os.path.join(epdir, f"{packages[i]['episode_id']}.json"))]
        if not pending:
            break
        print(f"pass {p+1}: {len(pending)} episodes pending", flush=True)
        done_ok = 0
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            for idx, rc, msg in ex.map(run_one, pending):
                if rc == 0:
                    done_ok += 1
                print(f"  idx={idx} rc={rc} {msg}", flush=True)
        print(f"pass {p+1} done: {done_ok}/{len(pending)} succeeded", flush=True)

    final_pending = [packages[i]["episode_id"] for i in range(args.start, args.end)
                     if not os.path.exists(os.path.join(epdir, f"{packages[i]['episode_id']}.json"))]
    total = args.end - args.start
    print(f"FINAL: {total - len(final_pending)}/{total} complete; missing: {final_pending}", flush=True)

if __name__ == "__main__":
    main()
