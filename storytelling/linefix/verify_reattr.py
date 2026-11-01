import json, glob, sys, collections
sys.path.insert(0, '/mnt/agents/work/epfix')
from epfix_lib import validate_episode, iter_line_paths
REPO = '/mnt/agents/work/epfix/kire321-thai-rpg-content-806803f'
vc = {c['id'] for c in json.load(open(REPO + '/public/characters.json'))}
vp = {p['id'] for p in json.load(open(REPO + '/public/places.json'))}
va = {a['id'] for a in json.load(open(REPO + '/public/attributes.json'))}
ti = {t['id'] for t in json.load(open(REPO + '/public/tags.json'))}
eps = {e['id']: e for e in json.load(open(REPO + '/public/episodes.json'))}
bad, tot, moves = [], 0, collections.Counter()
narr_left = 0
for f in sorted(glob.glob('/mnt/agents/work/epfix/reattr_episodes/*.json')):
    eid = f.split('/')[-1][:-5]
    ep = json.load(open(f))
    errs = validate_episode(ep, vc, vp, va, ti)
    # ep_059 has a pre-existing choice-order quirk; tolerate 'bad choices' there
    if eid == 'ep_059':
        errs = [e for e in errs if 'bad choices' not in e]
    if errs:
        bad.append((eid, errs[:3]))
    old = eps[eid]
    po = {p: ln for p, ln in iter_line_paths(old)}
    for p, ln in iter_line_paths(ep):
        if 'character' not in ln or p not in po or 'character' not in po[p]:
            continue
        if po[p]['character'] != ln['character']:
            moves[(po[p]['character'], ln['character'])] += 1
    tot += 1
print('outputs:', tot, 'invalid:', bad)
print('top speaker moves:')
for (a, b), n in moves.most_common(15):
    print(f'  {a} -> {b}: {n}')
print('total moves:', sum(moves.values()))
print('moves to char_old_lady:', sum(n for (a, b), n in moves.items() if b == 'char_old_lady'))
# remaining voiced narrator lines
import re
FP = re.compile(r'\b(I|me|my|mine|myself|we|us|our|ours)\b')
SP = re.compile(r'\b(you|your|yours|yourself)\b', re.I)
left = 0
for f in sorted(glob.glob('/mnt/agents/work/epfix/reattr_episodes/*.json')):
    ep = json.load(open(f))
    for p, ln in iter_line_paths(ep):
        if 'character' not in ln or ln['character'] != 'char_narrator':
            continue
        d = ln.get('dialogue') or ''
        if FP.search(d) or SP.search(d):
            left += 1
print('narrator lines still with first/second person:', left)
