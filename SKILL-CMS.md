# Thai RPG CMS — Content Agent Skill

> **SELF-UPDATE RULE**: Every agent working on this project MUST update this skill file before finishing. Add anything you learned, any user instructions given, any tricky bugs found, and any workflow changes. The next agent starts fresh with only this file and the code. Delete outdated info. This rule applies to YOU right now — update this file before you finish your task.

> **⚠️ SECRETS RULE — NEVER PUBLISH API KEYS**: NEVER commit API keys, tokens, or credentials to this repository or publish them anywhere (code, docs, skill files, comments, git history). If a key appears in any file you are about to push, replace it with a placeholder (e.g. `os.environ["FIREWORKS_API_KEY"]` or `<substitute the real key at runtime>`) before pushing. If a key was ever committed, treat it as compromised: rotate it and scrub it from every branch. This rule applies to YOU right now.

> **2026-10-14 (batch rebuild — CURRENT CANONICAL EPISODE PROCESS)**: All 170 episodes (`ep_011`–`ep_180`) were regenerated in one batch by a NEW pipeline, replacing every previous generation process (sprints 1–6, all `generate_episodes*.py` / `write_episode*.py` / `storytelling/pipeline/` — those scripts are DELETED; this entry + `storytelling/llm_pipeline/` is the whole process now). The pipeline has three stages:
>
> 1. **DEAL** (deterministic, no LLM): `python3 storytelling/schedule_episode_elements.py --start 11 --count 170 --out packages.json`. The scheduler seeds tag usage from the current `public/episodes.json` and rotates foregrounded characters per deal, so tags (each of the 340 used 4–5×) and foregrounds (28–29× each of the 6 cast) distribute evenly across the batch. Each package = episode id + foregrounded character (full private plan) + cast priority order (full plans) + 3 places in dealt order (act 4 is always `place_veranda`) + per-act 2 tags with themes + one priority pair per act.
> 2. **WRITE** (one LLM call per episode): `storytelling/llm_pipeline/ep_lib.py::build_prompt` renders a fully self-contained prompt (world brief, ALL blueprint text inline, fixed anchor words per tag, decision-pair orientations, craft requirements, markdown-script output contract) and calls **`deepseek/deepseek-v4-flash`** via OpenRouter (16k max tokens; ~13.4k prompt + ~6.3k completion tokens ≈ **$0.009/episode**, ~$1.6 for the batch). `ep_worker.py --index N` does up to 3 generation attempts, keeping the first parseable one. `lane_runner.py --start S --end E --parallel P --passes N` runs a resumable local pool (crashes/interrupts: just re-run the same command).
> 3. **PARSE + FIX** (deterministic Python, no LLM): `ep_lib.py::parse_episode` converts the markdown script to CMS JSON — acts split on `## Act`, tag markers, screenplay lines mapped to canonical char/place ids via alias tables, DECISION blocks parsed with tolerant regexes (model deviates: no bullets, missing colons, nested parens, abbreviated attributes, `**bold**` noise — all handled). Then structural fixups guarantee validator compliance: block sizes forced to 4–6/2–3/2–3 (steal lines between blocks, else narrator pad lines), anchor word forced into the last dialogue line before each tag (move a containing line, else append `The word was "X."`), choice attributes forced to the dealt orientation (EASY→2nd priority, MEDIUM→1st, HARD→`attr_word_hoard`), outcome speakers forced to the foregrounded character, Thai Unicode stripped, stage-direction-only lines promoted to dialogue. Every fixup is logged per-episode in `manifest.jsonl` (`ok` vs `patched` vs `failed`).
>
> **Assembly & ship**: `assemble.py` merges all `episodes/*.json` into `public/episodes.json` (ordered), then `python3 validate.py` MUST pass 0 errors, then push this repo, then copy `public/episodes.json` into the site repo `kire321.github.io` under `cms/` and push (or wait for the 04:23 UTC cron). The game frontend natively supports the multi-episode array (controller picks by spaced-repetition: due tags → episodes whose first act uses them, least-played first). Verify the live game by loading `https://kire321.github.io/` in headless Chromium and checking the first episode's first dialogue line renders.
>
> Known quality profile of v4-flash episodes: structurally valid, mechanically compliant; craft is thinner than hand-written episodes (flat outcome lines, thin empathy payloads, repetitive pad lines where the model underfilled blocks). Benchmarked B− (2026-10-14): full spec compliance, weak literary depth. Cost/running-time levers: `--parallel` lanes (20 concurrent streams ≈ 35–50 min for 170).

> **2026-08-20 (user decision)**: The world has been REBUILT on `master`. The old Chantara world is preserved as a museum on the `vibe-world` branch (do not delete). Work happens directly on `master` now; the old "staging first" rule is suspended for the rebuild. New world: canal-side Siam ~1910s–1950s, six orthogonal dialectics (face, merit-ledger, gratitude-debt, fate-chart, heart-temperature, guest-soul) — see `storytelling/research_dialectics.md`, `storytelling/SKILL_CHECKLIST.md` (mandatory writing rubric), `storytelling/prompts/` (generation prompt templates), `storytelling/private/` (private narrative plans). Cast: 6 recurring characters (type "party", one per dialectic) × 3 places each; 18 extras (type "npc", generic, one per place); place_veranda is the hub available in every episode but never foregrounded. `subplots` are RENAMED to `attributes` everywhere (public/attributes.json; episode choice/outcome field is `attribute`); the PC's five attributes have initial scores. Episodes use the ACT_FORMAT_V2 `segments` format, 4 acts × 2 tags. Generation model: qwen/qwen3-235b-a22b-2507 via OpenRouter (see storytelling/prompts + /model_shopping.md decision 2026-08-20; DeepSeek 3.2 is the fallback).

> **2026-09-03 (sprint 1, pipeline iteration)**: The 3-stage pipeline in `storytelling/pipeline/` was procedurally revised (branch `sprint1-pipeline`, pushed via REST as a squashed commit — shell git push remains flaky HTTP/2). Changes: all retry/restart loops REMOVED per product-owner decision (single pass per stage; gates RECORD failures in the report but do not block — editor flagged this as the #1 bulk-readiness issue; needs PO decision); planner now emits a narrative-order OUTLINE (PRESENT/ENTRANCE/STAKES/DECISION beat grammar) + TAG PLAN (one English anchor word per tag, placed in the line immediately BEFORE the tag segment — replaces Thai-phrase-with-gloss); writer prompt fully replaced (dumb outline-expander, no technique vocab — simile flood fixed 7+→0 by keeping comparisons out of the outline); secrets routed planner-only from `storytelling/private/char_*_private.md`; nicknames always (parsed from characters.json; no more name bridges). New gates: transcription diff (formatter inventions), place/character allow-lists, Thai-phrase placement, stakes beat, speaker budget. KNOWN OPEN DEFECTS after 2 iterations (see storytelling/pipeline/sprint1/iter2/EDITOR_FEEDBACK_2.md): zero Thai shipped in both iterations (model paraphrases/drops phrases — may need code post-insertion); first-person narrator POV regression (ungated); pass/fail outcomes perform the same action; choice 10-20-word rule never yet satisfied; formatter is the least trustworthy stage (dropped best lines, hallucinated char_kam). Generation cost: ~$0.006/episode on qwen/qwen3-235b-a22b-2507 (3 calls). `public/episodes.json` on master is currently a 1-episode PREVIEW (ep_003) for the CMS GUI per sprint demo procedure; ep_001/ep_002 remain in git history and on branch sprint1-pipeline.

> **2026-09-03 (sprint 2, model shopping + structural rebuild)**: Pipeline rebuilt again on branch `sprint1-pipeline` (see storytelling/pipeline/sprint2/ for benchmark data, both passes, editor feedback). MODEL MIX (benchmarked per-step, /mnt data in sprint2/model_shopping.md): plan = deepseek/deepseek-v3.2, prose + spot-edit = deepseek/deepseek-v4-flash, format = DETERMINISTIC PYTHON (no LLM — splits at [[tag]] markers, decisions verbatim from plan beats, FATAL on empty/oversize segments or unmappable ids). GLM-5.3-flash is operationally unusable (reasoning model, hangs); google/* and openai/* are region-blocked on the current OpenRouter key. STRUCTURE: atomic 4-step plan (base → stakes/entrances → decisions → tag plan) → plan gate → ONE v4-flash spot-edit (keep-better guard: a re-gate-worse edit is discarded) → prose → prose gate → ONE spot-edit → deterministic format → report. Hard FATALs: empty segment, segment-1 >6 lines, missing/cost-less STAKES beat. Cost ~$0.014/episode (v4-flash reasoning tokens in spot-edits are ~40-65% — a cheaper editor model is the next saving). ep_005 passed editor as CONDITIONALLY BULK-READY; known open debts: Thai phrase/episode semantic mismatch (~half orphan — needs selection-side fit, not prompts), run-on beat-cramming, menu-voice dilemma lines, refrain machinery never implemented (4 episodes), near-duplicate narration scan gap. `public/episodes.json` on master is the 1-episode PREVIEW (now ep_005).

> **2026-09-03 (sprint 3, tag pivot + literary machinery)**: PO DIRECTIVE (overrides earlier Thai rules): the story must contain ZERO Thai — the frontend inserts a bilingual vocab quiz at each tag, so in-story Thai gives away the answer. The story-tag link is ENTIRELY ENGLISH (vibe-world model: "I heard everything. Every tone, every overtone." before hearing-vocab tag_091): the lines before each tag evoke the tag's theme with the English word(s) that best unify it (derived from the tag's linked vocab_items "english" fields). Driver passes a 12-tag least-used shortlist with theme summaries; the planner picks 8 and assigns acts; unused shortlist tags are reported for balancing. Hard gate: zero Thai Unicode in episode JSON. LITERARY MACHINERY: plan steps now build thesis noun phrase, refrain arc (3 occurrences, meaning-change, cosmic final), and one wonder beat per act (4 shapes, planner supplies concrete content) into the outline as beats; plan gates check presence; keep-better guard is WEIGHTED (an edit that strips machinery or drops sections/acts is auto-rejected — an unweighted guard amputated the machinery in pass 1). STATUS after sprint 3: refrain survives plan->prose (delivered as exact quoted lines); THESIS phrase fails at the prose channel (writer ignores woven-in machinery; needs a prose-side survival gate — the known next fix); editor rates validity "high but imperfect, good enough to move on". Known quality debts: tag links prime tokens not fields in ~half of slots; menu-voice "Do I X, or Y?" dilemma lines; "I see..." outcome monoculture; false re-arrivals at segment boundaries. Marker positions are now repaired DETERMINISTICALLY by the formatter (v4-flash cannot count). `public/episodes.json` on master is the 1-episode PREVIEW (now ep_006).

> **2026-09-03 (sprint 4)**: New features: actions live in stage_directions and dialogue with its speaker (narrator never quotes speech — gated); plan beats are annotated with the plan elements they carry (act-1 seg-1 beats must carry 2+; no 3+ consecutive single-element beats); dilemma-line syntax-diversity gate; lints (markdown asterisks, narrator spoiler words forged/fake/stolen, junk stage directions, orphaned objects, double entrances). FORMATTER HONESTY RULE: the deterministic formatter NEVER merges, reorders, or repositions lines — any out-of-contract segment (too few/many lines incl. 1-liners) or act outside 8-12 lines is FATAL and ships nothing; repair only via prose spot-edit. Consequence: the full gate suite has outgrown one generic spot-edit pass (raw plans carry 19-34 failures); sprint-5 direction per CHANGES8.md: fold the top FATAL classes back into the atomic plan-step instructions so raw plans need less editing. ep_007 (sprint4/pass1) shipped with the first editor-confirmed REFRAIN arc and best tag priming so far. 'of' allowed in thesis phrases when object/descriptor share properties; only 'like'/'as if' banned. Preview on master: ep_007.

> **2026-09-03 (sprint 5)**: FATAL classes folded into atomic plan-step instructions (raw plan failures 48->17). Dialectical phrases now DRAWN from char+place private-plan pools with a variety gate (>=2 distinct phrases per episode, <=2 beats each). Prose stage is now PER-ACT (4 calls with carryover glue, act-scoped gates + 1 act-only retry). Transport: 16000-token caps fixed v4-flash truncation deaths (verified effective); reasoning:effort=low is IGNORED by the provider (v4-flash burns full reasoning tokens regardless — cost accordingly); temp-0.6 and qwen fallback levers exist but were never triggered. STANDING BLOCKER: v4-flash cannot hold act-scale segment line budgets (1-in-4 acts blows counts and spot-edit can't count it back; formatter FATALs per the no-merge rule). Sprint-6 candidates in sprint5/pass3 notes: generate segment-by-segment, or a hard numbered-line template in the per-act prompt.  ep_008 unshipped; preview remains ep_007.

> **2026-09-10 (sprint 6)**: Prose stage rebuilt SEGMENT-BY-SEGMENT (3 budgeted calls per act; numbered-line template as the segment retry) — the act-scale counting blocker is BEATEN at the generation layer (editor ticked the segment contract on pass 1: [6,3,3] across acts). New verified gates, all loud-abort: empty decision.line / PLACE-leak titles / blank dialogue fields are now FATAL (pass-1 ship had silently dropped all four decision lines; quarantined as ep_008.PARTIAL-do-not-ship.json); plan-beat coverage gate FATALs when a dropped beat orphans a choice (the almanac-toss case); refrain integrity gate (no verbatim repeat; final occurrence must differ in wording); speaker-prefix fuzzy canonicalization + invented-speaker/marker-loss HARD VETO (never tie-able in keep-better); terminal segment-fatal abort; prose stage now honors ALL plan FATAL classes (was silently ignoring STAKES/budget). Beat-budget FATAL recalibrated to [4-8]/[2-4]/[2-4] after 3 consecutive plan aborts — but that recalibration exposed the SPRINT-7 BLOCKER: letting the writer combine adjacent beats degrades wording enough that the coverage gate FATALs on orphaned beats (13 in the last run). Root fix planned: make plan beat budgets binding at generation time (planner ignores them ~80% of runs; restate per-act beat counts mechanically at the plan tags step). Editor pass-1 verdicts: segment contract TICK, wonder beats TICK (best yet), refrain REGRESSION, attribution REGRESSION, POV REGRESSION, dense beats NO-TICK (3rd). Sprint cost ~$0.35 OR.  ep_008 STILL unshipped; preview remains ep_007.

> **2026-09-11 (sprint 7)**: Beat budgets now BINDING at plan generation — the tags step emits machine-parsed ALLOCATION lines (authoritative segment split, scaled to beat count; sanity range [4-8]/[2-4]/[2-4]; planner-model repair at v3.2, not prose). ep_008 SHIPPED and editor-verified for preview: segments [5,3,3]x3+[6,2,3], 8/8 tags, 4/4 dilemmas, zero Thai. REGRESSION SUITE adopted: pipeline-artifact scan (ALLOCATION/TAG PLAN/segN=M/literal backslash-n), bare 'Act N' titles, narrator-carries-speech, misattributed narration, empty dialogue/decision are all FATAL AT SHIP; every string scanned. Title fallback derives from the plan's refrain phrase. Editor verdicts this sprint: POV re-ticked, speech/SD attribution re-ticked (post-repair), THESIS PHRASES TICKED (deployed in-text, first time), segment contract + wonder hold. OUTSTANDING: refrain arc still not reproduced (no verbatim repeat but no 3-occurrence arc), dense beats 4th no-tick, 2 tag anchors broke during attribution repair (tag_244, tag_279 — post-repair full-suite rerun is now mandatory procedure), act titles collapse to one fallback string, tag anchor selection must become SEMANTIC ('I graduate from that assumption', 'love yourself' broke character/era), dilemma speaker=PC + syntax entropy. Preview on master: ep_008.

> **2026-09-11 (sprint 8)**: ELICITATION PIVOT (PO experiment, confirmed): deepseek-v3.2 prompted cold for "a 1-page skit" produces flawless script format — the pipeline was making it underperform by emitting story-format outline beats and converting story->script per beat. Now: planner emits speaker-attributed SCRIPT beats; prose prompt is "continue this script, add 1-2 lines involving X"; narrator omitted from character beats (fix-by-omission). PROSE MODEL SWITCHED to deepseek-v3.2 for prose+edit (v4-flash reasoning-truncation loops vanished; qwen fails the contract outright). New: narrator-subject detection-only FATAL (no auto-rewrite; possessive/PP exempt); WONDER-inventory plan lint (>=3 concrete items + explicit "shows X" motivation clause); line-level repair (regenerate ONE line, can't break neighbors); OR-JUDGE scaffold (judge.py, v3.2, ~$0.005/ep, scores motivation/flow/anchors — editor adjudicates; judge validated as trustworthy pre-reader; fix its 'parsed scores: {}' output-contract bug before bulk telemetry). ep_009 SHIPPED, editor verdict BEST-OF-PIPELINE: script-feel TICK, motivation-inventory TICK. Open: 6 anchor-word misses (3/8 quizzes unprimed — sprint-9 #1), act titles all derive from one refrain phrase (2nd episode), dropped-subplot orphan class ungated (veiled-pupil plan dropped after act 2), outcome verbs drifting to I-see/I-watch, PC agency sliding (Lek 2 lines), refrain arc absent 5th episode running. Sprint cost ~$0.14 OR. Preview on master: ep_009.

## Project Overview

You manage the **content CMS** for a Thai vocabulary-learning RPG (current world: canal-side Siam ~1910s–1950s; "Chantara" was the old world, preserved on branch `vibe-world`). The CMS is a static React app. It generates, edits, and curates all game content: episodes (narrative + choices), characters, places, tags, and vocabulary items.

> **DEPLOYMENT STATUS (2026-07-30)**: CMS content is published as a **same-origin mirror at `https://kire321.github.io/cms/`** and the CMS **editor UI** is durably deployed at **`https://kire321.github.io/cms-ui/`** (GitHub Pages, no Kimi-agent dependency). Both mirror `master` of this repo. The old `*.kimi.page` CMS URLs are agent-instance-tied legacy — do not use or reference them. The Cloudflare plans below are obsolete.

**Repo**: `https://github.com/kire321/thai-rpg-content`  
**Frontend repo (reference)**: `https://github.com/kire321/thai-rpg`

### Content Types

| Type | File | Count | Notes |
|------|------|-------|-------|
| Episodes | `public/episodes.json` | 170 | ep_011–ep_180, 4 acts each, ACT_FORMAT_V2 segments (2026-10-14 batch) |
| Tags | `public/tags.json` | 340 | Each links to 5–10 vocab items |
| Vocab Items | `public/vocab_items.json` | 340 | Thai word + phonetics + English |
| Characters | `public/characters.json` | 29 | 6 party + narrator + PC (char_pricha) + 21 NPCs |
| Places | `public/places.json` | 20 | Canal-side Siam; hub is place_veranda |
| Attributes | `public/attributes.json` | 5 | Thai-concept attributes (see Episode Generation section) |

### Episode Structure

Episodes use the ACT_FORMAT_V2 `segments` format (5 segments per act: narrative/tag/narrative/tag/narrative,
4–6 / 2–3 / 2–3 line budgets). The full annotated schema lives in `ACT_FORMAT_V2.md` and in the
Episode Generation section below — those are canonical; ignore any older lines_before/tag/lines_after
documentation you may find in git history or on the vibe-world branch.

## Git Workflow

**Branch strategy (resolved 2026-07-30, per user decision):**
- `master` — **canonical published content** (DEFAULT branch; 340 episodes + Fireworks quality fixes). The publisher mirrors this branch.
- `510_episodes` — preserved v2 expansion output (ep_001–ep_510). Renamed from `main` on 2026-07-30 (user decision; `main` no longer exists). A project the user will get back to later — do NOT merge into master and do NOT delete.
- `staging` — parked WIP (its `public/episodes.json` is a 52-byte tool-insertion stub, not real episode data). Do not treat as publishable.
- `segments_failed` — archive of the failed v2 segments migration (do not delete; ACT_FORMAT_V2.md spec recovered from here)
- `bad_merge` — archive of failed merges (do not delete)
- Feature branches — for large changes, branch from staging

**Rules:**
- Do work on `staging`. Push to `staging` frequently.
- Only push to `master` when staging is verified and the user approves.
- Push auth: the user provides a fine-grained PAT (contents/actions/workflows/pages RW on all three repos). Shell `git clone/push` to github.com is FLAKY from the sandbox (HTTP/2 framing errors); `api.github.com` REST is reliable — use the Contents/Git-Trees APIs (single-commit trees for multi-file changes). The GitHub MCP plugin's identity cannot see these repos (404) — do not rely on it.
- Update this skill file on every task. Push skill file changes with your code.

## Deployment

### GitHub Pages mirror (durable, current as of 2026-07-28)

CMS **content** (`public/`) is published to `https://kire321.github.io/cms/` — same origin as the game app (`https://kire321.github.io/`), so no CORS is needed. The game fetches content via `DEFAULT_CMS_BASE='/cms'`; picture paths in the JSONs (`/characters/*.png`) resolve against that base.

**Publisher**: `.github/workflows/deploy-app.yml` in repo `kire321/kire321.github.io`. On each run it: checks out `kire321/thai-rpg@master` + builds the game, copies `kire321/thai-rpg-content@master/public/` into the site folder `cms/`, builds the CMS editor UI from `kire321/thai-rpg-content@master` into `cms-ui/` (with duplicated data JSONs stripped — the UI fetches from `/cms/*.json`), commits everything to that repo's `master` — and legacy branch-based GitHub Pages redeploys automatically on that push. No secrets: checkouts of the public repos need no token, and the push uses `GITHUB_TOKEN`.

**Deploy procedure for content changes:**
1. `python validate.py` — must pass.
2. Push content to `master` (the canonical branch).
3. Trigger the publisher:
   ```
   curl -X POST -H "Authorization: Bearer <user's fine-grained PAT>" \
     https://api.github.com/repos/kire321/kire321.github.io/actions/workflows/deploy-app.yml/dispatches \
     -d '{"ref":"master"}'
   ```
   (or wait for its daily 04:23 UTC scheduled run). The workflow file must exist on `kire321.github.io`'s DEFAULT branch for dispatch to work.
4. Verify (GitHub Pages CDN caches 404s — use a cache-buster and expect ~1-2 min build lag):
   `https://kire321.github.io/cms/episodes.json?cb=$(date +%s)` → 200, and one image, e.g. `/cms/characters/ampa.png`. CMS UI: `https://kire321.github.io/cms-ui/` → 200 and its `assets/*.js` bundle → 200.
5. To confirm the mirror is byte-identical to the source without downloading 11MB, compare blob SHAs:
   `GET /repos/kire321/thai-rpg-content/contents/public/episodes.json?ref=master` vs `GET /repos/kire321/kire321.github.io/contents/cms/episodes.json?ref=master` — the `sha` fields must match.

**Pitfalls (verified live):**
- On a user Pages site (`*.github.io`), URL path `/<reponame>/` is RESERVED for that repo's project site. A folder named `thai-rpg-content/` would be entirely shadowed (every file 404s) — that is why the mirror lives at `/cms`. Never use repo-named paths.
- The CMS UI is served from the `/cms-ui/` subpath, so all its data fetches must be absolute to `/cms/...` (e.g. `fetch('/cms/episodes.json')`), never `fetch('/episodes.json')` — a root-relative fetch would silently load the GAME app's bundled 1-episode fixture from the site root. Fixed in commit `0f144599` (2026-07-30); keep this invariant when adding new pages/fetches.
- The old flow (`mshtools-deploy_website` -> kimi.page URL -> Cloudflare `_worker.js` proxy) is OBSOLETE: kimi.page URLs die with the Kimi agent instance that created them, and `api.workers.cloudflare.com` has had a GLOBAL HTTP 522 outage since ~2026-07-26 (verified from 6 networks incl. Azure — Cloudflare-side, unlisted on their status page).
- A `thai-rpg.pages.dev` proxy URL still fronts the game; when Cloudflare's host recovers it will be repointed as a plain passthrough to `https://kire321.github.io` (cron-automated; see the app repo's `skill 2.md`).

### Deployment Checklist

1. `python validate.py` — pass
2. Push content branch
3. Dispatch the publisher workflow (or wait for the daily run)
4. Verify `https://kire321.github.io/cms/` JSONs + an image with cache-busters

## Episode Generation

> **CANONICAL PROCESS (2026-10-14)**: the sprint 1–6 pipeline, the Fireworks/GLM scripts, and every
> `generate_episodes*.py` / `write_episode*.py` helper described in older revisions of this file are
> DELETED. The whole process is the three-stage batch pipeline summarized in the 2026-10-14 journal
> entry above and implemented in `storytelling/llm_pipeline/` (deal → one v4-flash call per episode →
> deterministic parse/fix → assemble → validate → push). The narrative-standards notes below still
> apply as quality goals; the parser's fixups enforce structure only, not these.

### Narrative Quality Standards (quality goals — not parser-enforced)

1. Choice descriptions: concrete first-person actions, each sacrificing something real; none obviously right.
2. Outcomes: the foregrounded character speaks; regard changes (warmth, trust, distance); NEVER new plot facts — the world's state after the decision is identical on every branch.
3. No superposition in dialogue ("either/or", "might") — one concrete event per line. Superposition lives only in choices/outcomes.
4. Situation-relevant inventories: collections shown must bear on the episode's cross-purposes conflict.
5. Distinct voices: every speaker identifiable from dialogue alone (tics, address-forms, pricing habits).
6. Dialectical noun phrases: ~1 per act, no "like"/"as if", one in the first line; everything else literal.
7. No Thai script anywhere in episode JSON (the frontend inserts the bilingual quiz at each tag).
8. Anchor rule: each tag's fixed English anchor word appears in the last dialogue line before the tag.

### Canonical cast / places / attributes (canal-side Siam world)

Party (foregroundable, one per episode, appears in all 4 acts, delivers all outcome lines):
`char_sangwan` (Wan, letter-writer — love is a debt), `char_phum` (disgraced scribe — voice without consequence),
`char_phra_kam` (monk — goodness is a ledger), `char_mor_duang` (Kamnan Noi, star-reader — fate-chart),
`char_pornchai` (Pom — heart-temperature), `char_rangsri` (spirit-medium — the self is a guest).
PC: `char_pricha` (Lek). Narrator: `char_narrator`.

Attributes: `attr_heart_water`, `attr_deference`, `attr_ledger`, `attr_merit_water`, `attr_word_hoard`.
Places/NPCs: see `public/places.json` / `public/characters.json` (20 places incl. hub `place_veranda`;
NPC specialists such as `char_tax_clerk`, `char_fire_stoker`, `char_type_monitor` come with their place's act).

### Episode schema (ACT_FORMAT_V2 segments — enforced by validate.py)

```jsonc
{
  "id": "ep_011", "title": "…",
  "acts": [{
    "id": "act_001", "title": "…",
    "segments": [                    // EXACTLY 5, types in this order
      {"type": "narrative", "lines": [ /* 4–6 lines */ ]},
      {"type": "tag", "tag": "tag_NNN"},
      {"type": "narrative", "lines": [ /* 2–3 lines */ ]},
      {"type": "tag", "tag": "tag_NNN"},
      {"type": "narrative", "lines": [ /* 2–3 lines */ ]}
    ],
    "decision": {
      "line": {"character": "…", "place": "…", "dialogue": "…", "stage_directions": ""},
      "choices": [                   // 3: EASY, MEDIUM, HARD
        {"description": "…", "difficulty": "easy|medium|hard", "attribute": "attr_…",
         "pass_outcome": {"line": {"character": "…", "place": "…", "dialogue": "…", "stage_directions": ""},
                          "attribute": "attr_…", "delta": 1},
         "fail_outcome":  {"line": {"character": "…", "place": "…", "dialogue": "…", "stage_directions": ""},
                          "attribute": "attr_…", "delta": 0}}
      ]
    }
  }]
}
```

Decision-pair orientation per act (dealt): EASY checks the pair's SECOND priority, MEDIUM the FIRST,
HARD bypasses (attribute `attr_word_hoard`). All character/place/tag/attribute ids must exist in the
respective public/*.json tables. Run `python3 validate.py` before every push — 0 errors required.

### Files

- `storytelling/schedule_episode_elements.py` — the dealer (deterministic; seeds tag usage from current `public/episodes.json`; never edit mid-batch).
- `storytelling/llm_pipeline/ep_lib.py` — prompt builder + markdown parser + fixups (alias tables, caps, anchors, orientation, Thai-strip).
- `storytelling/llm_pipeline/ep_worker.py` — one episode: generate (≤3 attempts) → parse → write `episodes/{id}.json` + `raw/`. Resume-safe (skips existing).
- `storytelling/llm_pipeline/lane_runner.py` — parallel range runner: `--start S --end E --parallel P --passes N`.
- `storytelling/llm_pipeline/assemble.py` — merge `episodes/*.json` → `public/episodes.json` (ordered by ep id).
- LLM: `deepseek/deepseek-v4-flash` on OpenRouter; key supplied at runtime via env/secret file — NEVER commit it.
- Working state (packages, manifest, raw, per-episode json) lives OUTSIDE the repo in persistent scratch (e.g. `/mnt/agents/work/ep170/`); only assembled `public/episodes.json` + pipeline scripts are committed.

### Operating the batch

```bash
python3 storytelling/schedule_episode_elements.py --start 11 --count 170 --out packages.json
python3 storytelling/llm_pipeline/lane_runner.py --start 0 --end 170 --parallel 4 --passes 3   # per lane; swarm multiple lanes for speed
python3 storytelling/llm_pipeline/assemble.py --episodes-dir <work>/episodes --out public/episodes.json
python3 validate.py && git push   # then mirror cms/episodes.json into kire321.github.io and push (or wait for the 04:23 UTC cron)
```

## Known CMS Data Issues

| Issue | Where | Fix |
|-------|-------|-----|
| `dialogue: "[None]"` | 250/340 episodes | Check `line` and `text` alternate fields; never use "[None]" string literal as fallback |
| `character: "char_bandit"` | Corrupted episodes | Use original `char` field; don't remap through name_map |
| `stage_directions` as array `[]` | Some episodes | Convert to string `""` |
| `char_` IDs in dialogue text | ~47 instances | Regex replace with character names |
| Foreign fields leaked | `attribute`, `tag`, `voice` in lines | Remove all keys except `character`, `place`, `dialogue`, `stage_directions` |
| Superposition in narrative | "either X or Y" | Rewrite to single concrete event |
| Placeholder choices | "Pichit acts (choice N)." | Regenerate via Fireworks, never use template fallback |

## Content Generation Prompts

### For New Places

Use existing places as style reference. Each needs: `id`, `name`, `picture`, `description` (2-3 sentences about acoustic environment and story beats).

### For New Characters

**Generic NPCs only** — types the party can encounter repeatedly. Each needs: `id`, `name`, `type` (`party`/`npc`/`narrator`), `description`.

### For New Episodes

Use the batch pipeline (see Episode Generation). Key prompt elements (all rendered by `ep_lib.py::build_prompt`):
- World context (canal-side Siam, the veranda hub, records/letters/ledgers/rites/debts)
- Full private blueprints inline for the foregrounded character, the cast, the dealt places and their NPCs
- The dealt tags with theme sentences and fixed anchor words; decision-pair orientations per act
- Craft requirements (cross-purposes sticky situation, situation-relevant inventories, two-sided empathy,
  distinct voices, ~1 dialectical phrase per act with one in the first line, literal register otherwise)
- Markdown-script output contract ( screenplay lines, `[TAG: …]` markers, DECISION blocks with EASY/MEDIUM/HARD)
- Explicit: "Return only the markdown episode."

## Storytelling Reference

The `storytelling/` folder contains world-building documents:
- `world_building.md` — The Lattice, skycities, resonance ships, the Silencing
- `characters.md` — Party members and NPC types
- `places.md` — Locations with acoustic characteristics
- `recurring_attributes.md` — The 5 recurring story threads

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
