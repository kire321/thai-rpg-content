# Thai RPG CMS — Content Agent Skill

> **SELF-UPDATE RULE**: Every agent working on this project MUST update this skill file before finishing. Add anything you learned, any user instructions given, any tricky bugs found, and any workflow changes. The next agent starts fresh with only this file and the code. Delete outdated info. This rule applies to YOU right now — update this file before you finish your task.

> **⚠️ SECRETS RULE — NEVER PUBLISH API KEYS**: NEVER commit API keys, tokens, or credentials to this repository or publish them anywhere (code, docs, skill files, comments, git history). If a key appears in any file you are about to push, replace it with a placeholder (e.g. `os.environ["FIREWORKS_API_KEY"]` or `<substitute the real key at runtime>`) before pushing. If a key was ever committed, treat it as compromised: rotate it and scrub it from every branch. This rule applies to YOU right now.

## Project Overview

You manage the **content CMS** for "Chantara," a Thai language-learning RPG. The CMS is a static React app. It generates, edits, and curates all game content: episodes (narrative + choices), characters, places, tags, and vocabulary items.

> **DEPLOYMENT STATUS (2026-07-28)**: CMS content is published as a **same-origin mirror at `https://kire321.github.io/cms/`** (GitHub Pages, durable, no Kimi-agent dependency). The old `*.kimi.page` CMS URLs are agent-instance-tied legacy — do not use or reference them. The Cloudflare plans below are obsolete. The CMS **editor UI** (the React app in this repo) currently has no durable deployment — only `public/` data is mirrored.

**Repo**: `https://github.com/kire321/thai-rpg-content`  
**Frontend repo (reference)**: `https://github.com/kire321/thai-rpg`

### Content Types

| Type | File | Count | Notes |
|------|------|-------|-------|
| Episodes | `public/episodes.json` | 340 | 4 acts each — the big one |
| Tags | `public/tags.json` | 340 | Each links to 5 vocab items |
| Vocab Items | `public/vocab_items.json` | 340 | Thai word + phonetics + English |
| Characters | `public/characters.json` | 20 | 4 party + 5 generic NPC types + 10 named NPCs + 1 narrator |
| Places | `public/places.json` | 20 | Locations in the Chantara world |
| Subplots | `public/subplots.json` | 5 | Recurring story threads |

### Episode Structure

```typescript
interface Episode {
  id: string;       // "ep_NNN" (001-340)
  title: string;
  acts: Act[];      // Exactly 4 acts
}

interface Act {
  id: string;              // "act_1" through "act_4"
  title: string;
  lines_before: Line[];    // 5-7 lines
  tag: string;             // "tag_NNN" — vocab tag
  lines_after: Line[];     // 3-4 lines
  decision: Decision;
}

interface Line {
  character: string;       // e.g. "char_pichit"
  place: string;           // e.g. "place_khrueang_market"
  dialogue: string;
  stage_directions: string;
}

interface Decision {
  line: Line;
  choices: Choice[];       // Exactly 3 choices
}

interface Choice {
  description: string;     // Specific action (10-20 words)
  difficulty: "easy" | "medium" | "hard";
  subplot: string;
  pass_outcome: Outcome;
  fail_outcome: Outcome;
}

interface Outcome {
  line: Line;
  subplot: string;
  delta: number;           // +1 to +2 (pass), -1 to 0 (fail)
}
```

## Git Workflow

**Branch strategy:**
- `master` — production CMS content. Cloudflare deployment: pending (not yet deployed as of 2026-07-14)
- `staging` — development/staging. Cloudflare deployment: being set up (first agent deployment in progress)
- `segments_failed` — archive of the failed v2 segments migration (do not delete; ACT_FORMAT_V2.md spec recovered from here)
- `bad_merge` — archive of failed merges (do not delete)
- Feature branches — for large changes, branch from staging

**Branch reality (2026-07-28) — READ CAREFULLY:** `main` is the repo's DEFAULT branch but its content history diverged: `main` has **510 episodes** (ep_001–ep_510, v2 expansion output) while `master` has **340 episodes** plus newer quality work (Fireworks choice regeneration "97.2% unique choices", storytelling/ refs, this skill file's updates). `master` is ahead of `main` by 9 real commits; `main`'s only unique commits are 2 obsolete workflow-file commits from 2026-07-28. **Which branch is canonical for publishing is an OPEN QUESTION — ask the user before switching the mirror source.** The publisher currently mirrors `main` (510 episodes).

**Rules:**
- Do work on `staging`. Push to `staging` frequently.
- Only push to `master` when staging is verified and the user approves.
- Push auth: the user provides a fine-grained PAT (contents/actions/workflows/pages RW on all three repos). Shell `git clone/push` to github.com is FLAKY from the sandbox (HTTP/2 framing errors); `api.github.com` REST is reliable — use the Contents/Git-Trees APIs (single-commit trees for multi-file changes). The GitHub MCP plugin's identity cannot see these repos (404) — do not rely on it.
- Update this skill file on every task. Push skill file changes with your code.

## Deployment

### GitHub Pages mirror (durable, current as of 2026-07-28)

CMS **content** (`public/`) is published to `https://kire321.github.io/cms/` — same origin as the game app (`https://kire321.github.io/`), so no CORS is needed. The game fetches content via `DEFAULT_CMS_BASE='/cms'`; picture paths in the JSONs (`/characters/*.png`) resolve against that base.

**Publisher**: `.github/workflows/deploy-app.yml` in repo `kire321/kire321.github.io`. On each run it: checks out `kire321/thai-rpg@master` + builds the game, copies `kire321/thai-rpg-content@<branch>/public/` into the site folder `cms/`, commits everything to that repo's `master` — and legacy branch-based GitHub Pages redeploys automatically on that push. No secrets: checkouts of the public repos need no token, and the push uses `GITHUB_TOKEN`.

**Deploy procedure for content changes:**
1. `python validate.py` — must pass.
2. Push content to the canonical content branch (see Git Workflow — **branch canonicality is an OPEN QUESTION as of 2026-07-28, confirm with the user before large publishes**).
3. Trigger the publisher:
   ```
   curl -X POST -H "Authorization: Bearer <user's fine-grained PAT>" \
     https://api.github.com/repos/kire321/kire321.github.io/actions/workflows/deploy-app.yml/dispatches \
     -d '{"ref":"master"}'
   ```
   (or wait for its daily 04:23 UTC scheduled run). The workflow file must exist on `kire321.github.io`'s DEFAULT branch for dispatch to work.
4. Verify (GitHub Pages CDN caches 404s — use a cache-buster and expect ~1-2 min build lag):
   `https://kire321.github.io/cms/episodes.json?cb=$(date +%s)` → 200, and one image, e.g. `/cms/characters/ampa.png`.

**Pitfalls (verified live):**
- On a user Pages site (`*.github.io`), URL path `/<reponame>/` is RESERVED for that repo's project site. A folder named `thai-rpg-content/` would be entirely shadowed (every file 404s) — that is why the mirror lives at `/cms`. Never use repo-named paths.
- The old flow (`mshtools-deploy_website` -> kimi.page URL -> Cloudflare `_worker.js` proxy) is OBSOLETE: kimi.page URLs die with the Kimi agent instance that created them, and `api.workers.cloudflare.com` has had a GLOBAL HTTP 522 outage since ~2026-07-26 (verified from 6 networks incl. Azure — Cloudflare-side, unlisted on their status page).
- A `thai-rpg.pages.dev` proxy URL still fronts the game; when Cloudflare's host recovers it will be repointed as a plain passthrough to `https://kire321.github.io` (cron-automated; see the app repo's `skill 2.md`).

### Deployment Checklist

1. `python validate.py` — pass
2. Push content branch
3. Dispatch the publisher workflow (or wait for the daily run)
4. Verify `https://kire321.github.io/cms/` JSONs + an image with cache-busters

## Episode Generation

### Narrative Quality Standards (Critical)

From hard-won experience, generated episodes MUST meet these standards:

**1. Choice descriptions** — Concrete, specific actions (10-20 words):
```
GOOD: "Chanida reroutes all power to the port-side crystal, accepting starboard damage"
BAD:  "Use Chanida's abilities to solve the problem"
BAD:  "Pichit acts (choice 1)."
```

**2. Outcomes** — Character speaks in first person, concrete result:
```
GOOD: "I'm routing everything to port! Hold on — the lattice will respond to one strong frequency even if the other side is dead!"
BAD:  "Success. The approach proves effective and the situation shifts."
BAD:  "Pichit succeeds. The lattice responds to the harmonic manipulation."
```

**3. NO superposition in dialogue** — Narrative lines describe ONE concrete event:
```
BAD:  "He either attacks or flees into the shadows"
BAD:  "The crystal might shatter or it might sing"
GOOD: "He attacks without warning, his disruptor aimed at the crystal core"
GOOD: "The crystal sings — a high clear note that makes everyone's teeth ache"
```
Multiple possibilities belong ONLY in choices and outcomes.

**4. Character-specific outcomes** — Outcomes reference the character who made the choice:
```
GOOD: "Pichit: My staff pulses with clarity. The lattice is showing us a path no chart has ever recorded."
GOOD: "Malee: The prosthetic locks onto a buried harmonic node. There's structure down there — something built."
```

**5. Subplot specificity** — Each choice advances a specific subplot:
- `subplot_frequency_map` — Chanida's open map, hidden frequencies
- `subplot_haunted_ship` — Arthit's lost ship echoes
- `subplot_crystal_leg` — Malee's prosthetic resonance
- `subplot_listener_warning` — Pichit's dismissed lattice warning
- `subplot_groundless` — surface colonization movement

### Characters

**Party members** (4): `char_chanida` (singer), `char_pichit` (ex-monk), `char_malee` (engineer), `char_arthit` (ex-captain)

**NPC types** (5 — GENERIC, not named individuals):
- `char_villager` — ordinary islanders (farmers, craftspeople, children)
- `char_bandit` — sky pirates with modified resonance ships
- `char_merchant` — trade negotiators between skycities
- `char_monk` — Listener order members who study the lattice
- `char_scavenger` — surface harvesters from Tha Khwae

**Narrator**: `char_narrator` — scene transitions only

When adding new NPCs, they should be **generic types** the party can encounter in many episodes (e.g., "Sky City Guard", "Lattice Fisher", "Tonal Order Enforcer"), NOT named individuals.

### Places (20 on master)

`place_khrueang_market`, `place_anchor_spire`, `place_phrao_monastery`, `place_lattice_surface`, `place_resonance_ship`, `place_tha_khwae_scrapyard`, `place_the_hollow`, `place_mae_rim_gardens`, `place_silent_zone`, `place_tonal_archives`, `place_sri_thep_ruins`, `place_wharf_of_echoes`, `place_crystal_core_depths`, `place_floating_necropolis`, `place_resonance_forge`, `place_skybridge_terminals`, `place_order_citadel`, `place_the_shimmering_sea`, `place_wind_shear_cliffs`, `place_chromatic_grotto`

### Fireworks API — Episode Generation

**API**: `https://api.fireworks.ai/inference/v1/chat/completions`  
**Key**: NOT STORED IN THIS FILE — substitute the real Fireworks API key at runtime (the user provides it in the task prompt; pass it via env var `FIREWORKS_API_KEY`). **Never commit or publish the key.**  
**Model**: `accounts/fireworks/models/glm-5p2` — best narrative quality on Fireworks  
**Rate limits**: High enough for 10 parallel workers  
**Cost**: ~$0.0025 per episode (12 choices via 4 API calls)

GLM 5.2 produces excellent first-person character dialogue for outcomes. It does chain-of-thought reasoning internally but the final output is clean markdown (CHOICE/PASS/FAIL format).

**Why not DeepSeek 3.2?** DeepSeek v3.2 is available on OpenRouter but Fireworks doesn't have it. GLM 5.2 ($4.4/M output) produces better narrative quality than Qwen 3.7 Plus ($1.6/M output) which wastes tokens on thinking tags. For budget: Qwen 3.7 Plus works but needs thinking-tag cleanup. Use GLM 5.2 for quality, Qwen 3.7 Plus if budget is tight.

### Fast Parallel Generation

Use threaded workers for speed. 10 workers calling Fireworks in parallel processes ~10 episodes/minute.

```python
import json, re, requests, time, os, threading, queue

FIREWORKS_KEY = os.environ["FIREWORKS_API_KEY"]  # real key provided by user at runtime; NEVER commit it
NUM_WORKERS = 10

def generate_act_choices(episode, act_idx):
    """Generate 3 choices for one act via Fireworks"""
    act = episode['acts'][act_idx]
    lines = []
    for line in act.get('lines_before', []):
        char = line['character'].replace('char_', '')
        if char != 'narrator':
            lines.append(f"{char}: {line['dialogue'][:55]}")
    if act.get('decision', {}).get('line'):
        dl = act['decision']['line']
        dc = dl['character'].replace('char_', '')
        lines.append(f"DECIDE {dc}: {dl['dialogue'][:65]}")
    context = " | ".join(lines[:4])

    prompt = f"""Scene: {episode['id']} Act {act_idx+1} ({act['title']}) | {context}

Write 3 choices:

CHOICE 1: [specific action, 15 words]
PASS: [character speaks, 1 sentence]
FAIL: [character speaks, 1 sentence]

CHOICE 2: ...

CHOICE 3: ..."""

    payload = {
        "model": "accounts/fireworks/models/glm-5p2",
        "max_tokens": 450,
        "temperature": 0.85,
        "messages": [
            {"role": "system", "content": "Write vivid RPG choices. Characters speak in first person. Be specific."},
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post("https://api.fireworks.ai/inference/v1/chat/completions",
        headers={"Authorization": f"Bearer {FIREWORKS_KEY}", "Content-Type": "application/json"},
        json=payload, timeout=30)
    if resp.status_code == 200:
        return resp.json()['choices'][0]['message']['content']
    return None

def parse_choices(text):
    """Parse CHOICE N / PASS / FAIL blocks"""
    choices = []
    current = None
    for line in text.split('\n'):
        line = line.strip()
        if not line: continue
        m = re.search(r'CHOICE\s+(\d+)[:\.]\s*\*?\*?\s*\[?([^\]]+)\]?', line, re.IGNORECASE)
        if m:
            if current and 'description' in current:
                choices.append(current)
            current = {'description': m.group(2).strip().strip('*').strip()}
            continue
        m = re.match(r'\*?\*?PASS:?\s*\*?\*?\s*(.+)', line, re.IGNORECASE)
        if m and current is not None:
            val = m.group(1).strip().strip('*').strip()
            val = re.sub(r'^\w+:\s*["\']?', '', val).strip().strip('"').strip("'")
            current['pass_outcome'] = val
            continue
        m = re.match(r'\*?\*?FAIL:?\s*\*?\*?\s*(.+)', line, re.IGNORECASE)
        if m and current is not None:
            val = m.group(1).strip().strip('*').strip()
            val = re.sub(r'^\w+:\s*["\']?', '', val).strip().strip('"').strip("'")
            current['fail_outcome'] = val
            continue
    if current and 'description' in current:
        choices.append(current)
    return choices
```

### Episode Structure Template

Each episode follows a 4-act dramatic arc:
- **Act 1**: Introduce challenge — establish situation, introduce NPCs
- **Act 2**: Escalate — complications arise, stakes increase
- **Act 3**: Crisis — turning point, hardest decisions
- **Act 4**: Transform — resolution and aftermath (avoid cheesy moral endings)

Per act: 5-7 `lines_before`, TAG (vocab word used naturally), 3-4 `lines_after`, then decision with 3 choices.

### Tag Distribution

Each of the 340 tags must be used exactly 4 times across 4 different episodes. Each episode uses 4 different tags (one per act). When adding episodes:
1. Calculate tag usage counts
2. Assign the least-used tags to new episodes
3. Validate every tag is used exactly 4 times

### Validation

Run `python validate.py` from the project root before every deploy. It checks:
- All IDs reference valid entities
- 3 choices per decision
- Correct delta values
- Tag distribution (each tag used 4 times)

## Known CMS Data Issues

| Issue | Where | Fix |
|-------|-------|-----|
| `dialogue: "[None]"` | 250/340 episodes | Check `line` and `text` alternate fields; never use "[None]" string literal as fallback |
| `character: "char_bandit"` | Corrupted episodes | Use original `char` field; don't remap through name_map |
| `stage_directions` as array `[]` | Some episodes | Convert to string `""` |
| `char_` IDs in dialogue text | ~47 instances | Regex replace with character names |
| Foreign fields leaked | `subplot`, `tag`, `voice` in lines | Remove all keys except `character`, `place`, `dialogue`, `stage_directions` |
| Superposition in narrative | "either X or Y" | Rewrite to single concrete event |
| Placeholder choices | "Pichit acts (choice N)." | Regenerate via Fireworks, never use template fallback |

## Content Generation Prompts

### For New Places

Use existing places as style reference. Each needs: `id`, `name`, `picture`, `description` (2-3 sentences about acoustic environment and story beats).

### For New Characters

**Generic NPCs only** — types the party can encounter repeatedly. Each needs: `id`, `name`, `type` (`party`/`npc`/`narrator`), `description`.

### For New Episodes

See `generate_episodes.py` for the full script. Key prompt elements:
- World context (crystalline lattice, floating islands, tonal language)
- Character voice guide (who speaks how)
- Place descriptions
- Assigned tags (least-used first)
- 4-act dramatic structure
- JSON template with exact schema
- Explicit: "Output ONLY JSON. No markdown code blocks."

## Storytelling Reference

The `storytelling/` folder contains world-building documents:
- `world_building.md` — The Lattice, skycities, resonance ships, the Silencing
- `characters.md` — Party members and NPC types
- `places.md` — Locations with acoustic characteristics
- `recurring_subplots.md` — The 5 recurring story threads

Use these as reference when generating new content to maintain world consistency.

## Agent Workflow

1. Read this skill file
2. Read the current state of the relevant JSON files
3. Make changes (generate, edit, fix)
4. Run `python validate.py`
5. `npm run build` from the repo root — must succeed
6. Push to GitHub (staging unless user says otherwise)
7. Publish: dispatch the `kire321.github.io` publisher workflow and verify `https://kire321.github.io/cms/` (see Deployment)
9. **Update this skill file** with anything you learned
10. Push skill file changes
11. Write your reply following the **Writing Your Reply** section below.

## Writing Your Reply

When you reply, don't claim to have completed the user's objective. Instead:

* describe in technical detail what you did (most of your reply should be dedicated to this section)
* [if you think the task isn't finished yet] ask the user for information to help you complete the task
* [if you think the task is finished] ask the user if their objective was completed (briefly restate the objective from the prompt to avoid referring to "your objective" in abstract terms)
* suggest further actions you could do that might help the user's objective
