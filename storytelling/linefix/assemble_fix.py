import json, os, sys
sys.path.insert(0, '/mnt/agents/work/epfix')
from epfix_lib import validate_episode
repo = '/mnt/agents/work/epfix/kire321-thai-rpg-content-9d84600'
vc = {c['id'] for c in json.load(open(repo + '/public/characters.json'))}
vp = {p['id'] for p in json.load(open(repo + '/public/places.json'))}
va = {a['id'] for a in json.load(open(repo + '/public/attributes.json'))}
ti = {t['id'] for t in json.load(open(repo + '/public/tags.json'))}
eps = json.load(open(repo + '/public/episodes.json'))
out, edited, kept = [], 0, []
for ep in eps:
    p = f"/mnt/agents/work/epfix/episodes/{ep['id']}.json"
    if os.path.exists(p):
        new = json.load(open(p))
        errs = validate_episode(new, vc, vp, va, ti)
        assert not errs, (ep['id'], errs)
        new['id'] = ep['id']  # guard
        out.append(new); edited += 1
    else:
        out.append(ep); kept.append(ep['id'])
json.dump(out, open(repo + '/public/episodes.json', 'w'), ensure_ascii=False, indent=1)
print('assembled', len(out), 'edited', edited, 'kept-original', kept)
