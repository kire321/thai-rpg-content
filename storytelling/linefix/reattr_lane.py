#!/usr/bin/env python3
"""Speaker-reattribution lane. Usage: reattr_lane.py --start N --end M [--force]"""
import argparse, json, os, re, sys, time

sys.path.insert(0, '/mnt/agents/work/epfix')
from epfix_lib import (apply_diff, parse_diff, validate_episode, build_hints)
from reattr_lib import detect, build_reattr_prompt
from fix_lane import call_llm, MODELS

WORK = '/mnt/agents/work/epfix'
REPO = os.path.join(WORK, 'kire321-thai-rpg-content-806803f')
OUT = os.path.join(WORK, 'reattr_episodes')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, required=True)
    ap.add_argument('--end', type=int, required=True)
    ap.add_argument('--manifest', default=os.path.join(WORK, 'reattr_manifest.jsonl'))
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--relax', action='store_true',
                    help='ignore pre-existing choice-order errors (ep_059 class)')
    args = ap.parse_args()

    chars = json.load(open(f'{REPO}/public/characters.json'))
    places = json.load(open(f'{REPO}/public/places.json'))
    valid_chars = {c['id'] for c in chars}
    valid_places = {p['id'] for p in places}
    valid_attrs = {a['id'] for a in json.load(open(f'{REPO}/public/attributes.json'))}
    tag_ids = {t['id'] for t in json.load(open(f'{REPO}/public/tags.json'))}
    eps = json.load(open(f'{REPO}/public/episodes.json'))
    os.makedirs(OUT, exist_ok=True)
    mlock = open(args.manifest, 'a')
    for idx in range(args.start, args.end):
        ep = eps[idx]
        eid = ep['id']
        out_path = os.path.join(OUT, f'{eid}.json')
        if os.path.exists(out_path) and not args.force:
            continue
        flags, mentioned = detect(ep)
        if not flags:
            # nothing suspicious; copy through
            json.dump(ep, open(out_path, 'w'), ensure_ascii=False, indent=1)
            mlock.write(json.dumps({'id': eid, 'status': 'clean', 'flags': 0}) + '\n')
            mlock.flush()
            print(eid, 'clean', flush=True)
            continue
        prompt = build_reattr_prompt(ep, chars, places, flags, mentioned)
        status, model_used, nops, err = 'failed', None, 0, ''
        new_ep = None
        for model in MODELS:
            for attempt in range(2):
                try:
                    text, usage = call_llm(prompt, model)
                    text = '\n'.join(l for l in text.splitlines()
                                     if re.match(r'^(PATCH|NONE)', l.strip()))
                    ops = parse_diff(text)
                    # speaker-only pass: enforce
                    ops = [(o, lid, spk, '-', '-') for o, lid, spk, dlg, st in ops]
                    # no outcome-speaker reassignments
                    ops = [t for t in ops if not (t[0] == 'PATCH' and re.match(r'a\d+s[PF]', t[1]))]
                    patched = apply_diff(ep, ops, valid_chars, valid_places)
                    errs = validate_episode(patched, valid_chars, valid_places, valid_attrs, tag_ids)
                    if args.relax:
                        errs = [e for e in errs if 'bad choices' not in e]
                    if errs:
                        raise ValueError('validation: ' + '; '.join(errs[:4]))
                    new_ep, model_used, nops = patched, model, len(ops)
                    status = 'ok' if ops else 'kept'
                    break
                except Exception as e:
                    err = f'{model}#{attempt}: {str(e)[:180]}'
                    time.sleep(5)
            if new_ep is not None:
                break
        if new_ep is not None:
            json.dump(new_ep, open(out_path, 'w'), ensure_ascii=False, indent=1)
        mlock.write(json.dumps({'id': eid, 'status': status, 'model': model_used,
                                'flags': len(flags), 'mentioned': mentioned, 'ops': nops,
                                'err': err}) + '\n')
        mlock.flush()
        print(eid, status, model_used, f'flags={len(flags)} ops={nops}', err[:110], flush=True)
    mlock.close()

if __name__ == '__main__':
    main()
