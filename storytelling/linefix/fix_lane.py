#!/usr/bin/env python3
"""Fix a range of episodes via OpenRouter diffs.

Usage: python3 fix_lane.py --start N --end M [--episodes-dir D] [--manifest F]
Reads/writes individual episode files so lanes run in parallel safely.
"""
import argparse, json, os, re, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from epfix_lib import (build_prompt, parse_diff, apply_diff, validate_episode,
                       issue_scan, iter_line_paths)

def try_apply(ep, ops, valid_chars, valid_places, valid_attrs, tag_ids):
    """Apply ops, dropping ops of segments that violate line budgets (recovery).
    Returns (patched_episode_or_None, dropped_segments)."""
    current = list(ops)
    dropped = set()
    for _ in range(6):
        try:
            patched = apply_diff(ep, current, valid_chars, valid_places)
        except ValueError:
            return None, dropped
        errs = validate_episode(patched, valid_chars, valid_places, valid_attrs, tag_ids)
        if not errs:
            return patched, dropped
        bad = set()
        for e in errs:
            m = re.match(r'act(\d+) seg(\d+)', e)
            if m and 'outside' in e:
                bad.add(f'a{m.group(1)}s{m.group(2)}')
        if not bad:
            return None, dropped
        dropped |= bad
        # in offending segments keep PATCHes (count-preserving), drop DELETEs/SPLITs
        kept = []
        for o in current:
            m = re.match(r'(a\d+s(?:\d|D|C|P|F))', o[1])
            if m and m.group(1) in bad and o[0] in ('DELETE', 'SPLIT'):
                continue
            kept.append(o)
        if len(kept) == len(current):
            return None, dropped  # no progress possible
        current = kept
    return None, dropped

KEY = os.environ.get('OPENROUTER_KEY', open('/mnt/agents/work/epfix/.or_key').read().strip())
MODELS = ['deepseek/deepseek-v3.2', 'deepseek/deepseek-v4.1-flash']
WORK = '/mnt/agents/work/epfix'
LOCK = os.path.join(WORK, 'lanes.lock')

def call_llm(prompt, model):
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.2,
        'max_tokens': 16000,
    }).encode()
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.load(r)
    msg = data['choices'][0]['message']
    content = msg.get('content')
    if not content or not content.strip():
        content = msg.get('reasoning')
    if not content or not content.strip():
        raise ValueError(f'empty content from {model}: {json.dumps(data["choices"][0])[:200]}')
    return content, data.get('usage', {})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, required=True)
    ap.add_argument('--end', type=int, required=True)
    ap.add_argument('--episodes-dir', default=os.path.join(WORK, 'episodes'))
    ap.add_argument('--manifest', default=os.path.join(WORK, 'manifest.jsonl'))
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()

    repo = os.path.join(WORK, 'kire321-thai-rpg-content-9d84600')
    chars = json.load(open(f'{repo}/public/characters.json'))
    places = json.load(open(f'{repo}/public/places.json'))
    tags = json.load(open(f'{repo}/public/tags.json'))
    valid_chars = {c['id'] for c in chars}
    valid_places = {p['id'] for p in places}
    valid_attrs = {a['id'] for a in json.load(open(f'{repo}/public/attributes.json'))}
    tag_ids = {t['id'] for t in tags}

    eps = json.load(open(f'{repo}/public/episodes.json'))
    os.makedirs(args.episodes_dir, exist_ok=True)
    mlock = open(args.manifest, 'a')
    for idx in range(args.start, args.end):
        ep = eps[idx]
        eid = ep['id']
        out_path = os.path.join(args.episodes_dir, f'{eid}.json')
        if os.path.exists(out_path) and not args.force:
            continue
        before_issues = issue_scan(ep)
        dropped_segs = []
        prompt = build_prompt(ep, chars, places)
        status, model_used, ops_n, err = 'failed', None, 0, ''
        new_ep = None
        new_ep2 = p2_model = None
        ops2_n = 0
        for model in MODELS:
            for attempt in range(2):
                try:
                    text, usage = call_llm(prompt, model)
                    # keep only well-formed diff lines (reasoning blobs carry prose)
                    text = '\n'.join(l for l in text.splitlines()
                                     if re.match(r'^(PATCH|DELETE|SPLIT|NONE)', l.strip()))
                    ops = parse_diff(text)
                    # never allow deleting structurally-required decision/outcome lines
                    ops = [o for o in ops
                           if not (o[0] == 'DELETE' and re.match(r'a\d+s[DPF]', o[1]))]
                    patched, dropped = try_apply(ep, ops, valid_chars, valid_places, valid_attrs, tag_ids)
                    if patched is None:
                        raise ValueError('validation failed, unrecoverable')
                    dropped_segs = sorted(dropped)
                    new_ep, model_used, ops_n = patched, model, len(ops)
                    status = 'ok' if ops else 'clean'
                    # pass 2: targeted rewrite of leftover flagged lines
                    from epfix_lib import leftover_flags, build_leftover_prompt
                    flags = leftover_flags(new_ep)
                    if flags:
                        p2_prompt = build_leftover_prompt(new_ep, chars, places, flags)
                        for m2 in MODELS:
                            if new_ep2 is not None:
                                break
                            for _a in range(2):
                                try:
                                    t2, _ = call_llm(p2_prompt, m2)
                                    t2 = '\n'.join(l for l in t2.splitlines()
                                                   if re.match(r'^(PATCH|NONE)', l.strip()))
                                    ops2 = [o for o in parse_diff(t2) if o[0] == 'PATCH']
                                    p2, _ = try_apply(new_ep, ops2, valid_chars, valid_places, valid_attrs, tag_ids)
                                    if p2 is not None:
                                        new_ep2, p2_model, ops2_n = p2, m2, len(ops2)
                                        break
                                except Exception:
                                    time.sleep(5)
                        if new_ep2 is not None:
                            new_ep = new_ep2
                            ops_n += ops2_n
                    break
                except Exception as e:
                    err = f'{model}#{attempt}: {str(e)[:200]}'
                    time.sleep(5)
            if new_ep is not None:
                break
        if new_ep is not None:
            json.dump(new_ep, open(out_path, 'w'), ensure_ascii=False, indent=1)
        rec = {'id': eid, 'status': status, 'model': model_used, 'ops': ops_n,
               'p2_model': p2_model, 'p2_ops': ops2_n,
               'issues_before': before_issues, 'err': err}
        mlock.write(json.dumps(rec) + '\n'); mlock.flush()
        print(eid, status, model_used, ops_n, err[:120], flush=True)
    mlock.close()

if __name__ == '__main__':
    main()
