import json, os, sys, shutil
sys.path.insert(0, '/mnt/agents/work/epfix')
from epfix_lib import validate_episode
REPO = '/mnt/agents/work/epfix/kire321-thai-rpg-content-806803f'
vc = {c['id'] for c in json.load(open(REPO + '/public/characters.json'))}
vp = {p['id'] for p in json.load(open(REPO + '/public/places.json'))}
va = {a['id'] for a in json.load(open(REPO + '/public/attributes.json'))}
ti = {t['id'] for t in json.load(open(REPO + '/public/tags.json'))}
eps = json.load(open(REPO + '/public/episodes.json'))
out, n = [], 0
for ep in eps:
    p = f"/mnt/agents/work/epfix/reattr_episodes/{ep['id']}.json"
    if os.path.exists(p):
        new = json.load(open(p))
        errs = validate_episode(new, vc, vp, va, ti)
        if ep['id'] == 'ep_059':
            errs = [e for e in errs if 'bad choices' not in e]
        assert not errs, (ep['id'], errs[:3])
        out.append(new); n += 1
    else:
        out.append(ep)
json.dump(out, open(REPO + '/public/episodes.json', 'w'), ensure_ascii=False, indent=1)
print('assembled', len(out), 'reattr-applied', n)
shutil.copy('/mnt/agents/work/epfix/old_lady.png', REPO + '/public/characters/old_lady.png')
print('portrait copied')
