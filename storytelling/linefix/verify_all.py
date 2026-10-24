import json, glob, sys
sys.path.insert(0, '/mnt/agents/work/epfix')
from epfix_lib import validate_episode, issue_scan, leftover_flags
repo = '/mnt/agents/work/epfix/kire321-thai-rpg-content-9d84600'
vc = {c['id'] for c in json.load(open(repo + '/public/characters.json'))}
vp = {p['id'] for p in json.load(open(repo + '/public/places.json'))}
va = {a['id'] for a in json.load(open(repo + '/public/attributes.json'))}
ti = {t['id'] for t in json.load(open(repo + '/public/tags.json'))}
eps = {e['id']: e for e in json.load(open(repo + '/public/episodes.json'))}
bad, tot, left, before_all, after_all = [], 0, 0, {'boat':0,'meta_anchor':0,'thai':0,'incomplete':0}, {'boat':0,'meta_anchor':0,'thai':0,'incomplete':0}
for f in sorted(glob.glob('/mnt/agents/work/epfix/episodes/*.json')):
    eid = f.split('/')[-1][:-5]
    ep = json.load(open(f))
    errs = validate_episode(ep, vc, vp, va, ti)
    if errs:
        bad.append((eid, errs[:3]))
    lf = leftover_flags(ep)
    left += len(lf)
    b, a = issue_scan(eps[eid]), issue_scan(ep)
    before_all['boat'] += b['boat']; after_all['boat'] += a['boat']
    before_all['meta_anchor'] += b['meta_anchor']; after_all['meta_anchor'] += a['meta_anchor']
    before_all['thai'] += b['thai']; after_all['thai'] += a['thai']
    before_all['incomplete'] += b['incomplete']; after_all['incomplete'] += a['incomplete']
    tot += 1
print('verified:', tot)
print('invalid:', bad)
print('total leftover flags:', left)
print('issue totals before -> after:')
for k in before_all:
    print(f'  {k}: {before_all[k]} -> {after_all[k]}')
