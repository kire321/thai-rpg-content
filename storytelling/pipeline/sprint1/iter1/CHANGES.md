# Sprint 1, Iteration 1 — Pipeline rewrite (procedural, character-agnostic, single-pass)

Files changed (in `thai-rpg-content`, branch `sprint1-pipeline`):
- `storytelling/pipeline/driver.py` — heavily rewritten
- `storytelling/pipeline/prompts/plan.md` — rewritten
- `storytelling/pipeline/prompts/prose.md` — totally replaced
- `storytelling/pipeline/prompts/format.md` — updated
- `storytelling/pipeline/README.md` — updated to match

Pipeline was NOT run (no API key, per instructions). Dry-run checks only.

## What changed, mapped to the 7 replacement items

### 1. De-Sangwan-ification / secrets come from the private plan
- Deleted `BANNED_SUBSTRINGS` / `BANNED_REGEXES` (death-language, "the late X",
  memory-language, "No. Only", Sangwan-specific technique bans) and every
  reference to Nim, "the concealed person", urns, "the lady", etc. from all
  three prompts and from the driver.
- `driver.py` now loads `storytelling/private/<foreground>_private.md`
  (`load_private_text`) and injects it ONLY into the planner's prompt
  (`{{PRIVATE_PLAN}}` slot). The prose stage receives only the outline plus the
  nickname list; the format stage receives only the prose. Secret facts are
  therefore physically unable to leak downstream — the planner plans around
  them instead of naming them (per the procedural philosophy: don't tell the
  writer to keep a secret; never give the writer the secret).
- Hard-coded nickname map `{"char_pricha": {"lek"}, "char_sangwan": {"wan"}}`
  in the narrator acid test is replaced by `build_name_map()`, which parses
  every character's nickname from `public/characters.json`
  (`"Pricha (Lek)"`, `"Pornchai 'Pom' Boonyakam"` both handled).

### 2. Nicknames only (name bridges deleted)
- Old rules 18/24/36 (full-name + nickname bridges) are gone from every prompt.
- All three prompts get a `{{NICKNAMES}}` slot ("char_sangwan: call them 'Wan'
  — NEVER 'Sangwan'") generated from `characters.json`.
- Enforced procedurally: `full_name_problems()` word-boundary scan runs in the
  plan gate, the prose gate, and per-line (dialogue + stage_directions) in
  `validate_episode`. The formatter is additionally authorized to substitute
  nickname-for-full-name as its one free word-level fix.

### 3. Retry loops removed
- `MAX_TRIES`, `MAX_RESTARTS`, `REPAIR_STAGES`, the `run_stage()` re-prompt
  loop, the targeted repair pass, the prose-regeneration fallback, and the
  probe-restart `for restart in ...` loop are all deleted.
- New `run_stage_once()`: one generation call, one gate check. Failures are
  logged and written into the report's "Gate results" section; the pipeline
  continues with the best-effort output. If the format stage's JSON cannot be
  parsed at all, the driver records it and exits 1 cleanly.
- The reader-comprehension probe (PROBE_QUESTIONS / JUDGE_PROMPT / strip_ids /
  judge calls) is removed entirely — it existed only to trigger restarts, and
  its Q5 was Sangwan-specific. A run is now exactly 3 API calls.
- Report now ends with `SUCCESS` / `COMPLETED WITH GATE FAILURES` /
  `FAILED (no parseable JSON)` plus per-stage problem lists for later triage.

### 4. Planner output = outline in narrative order
- `plan.md` rewritten as a 6-step procedure whose output is `## STICKY
  SITUATION`, `## OUTLINE` (`### Act 1..4`, numbered beats in narrative order),
  `## TAG PLAN`. Beats are constrained to five concrete shapes (event /
  entrance+description / object detail / dialogue content / sensory detail) —
  the mechanism that keeps character-sheet sections and theme essays out.
  WHY IT MATTERS, CENTRAL OBJECT, REFRAIN, ACT MAP, READER QUESTIONS, SECRET
  HANDLING sections are gone (they were essays/character sheets; their work is
  now done inside beats, e.g. STEP 3 "invent a concrete event that shows it,
  pass only the event").
- `check_plan()` verifies the three headers, the four act subsections, and
  rejects technique vocabulary (see item 5).

### 5. Writer totally replaced; no technique vocabulary downstream
- `prose.md` is a from-scratch "dumb writer": expand the outline beat by beat,
  in order; add nothing; six mechanical steps + a short self-check.
- `TECHNIQUE_VOCAB` in the driver ("wonder", "refrain", "thesis", "theme",
  "show don't tell", "numinous", "elegiac", "connoisseur", "loving inventory",
  "dialectic", "symbol", "stakes", ...) is machine-rejected in BOTH the plan
  gate and the prose gate, so the writer cannot receive technique words from
  the outline and cannot produce them itself. This kills the "writer mentions
  techniques instead of implementing them" bug at the source.
- All technique decisions (what shows what, what the opening sentence is) moved
  into the planner's procedure; the outline's Act-1 beat 1 is the opening
  sentence written out verbatim, preserving the charged-first-sentence
  discipline procedurally.

### 6. Tag/vocab procedure: English anchor word before each tag
- Replaced the Thai-anchor-phrase + dash-gloss machinery (`assign_anchors`,
  `extract_anchor_phrases`, verbatim-Thai gates, gloss rules 26/38).
- Planner picks ONE English anchor word per tag (strict bullet shape
  `- tag_xxx — English anchor word: "word" ...`, machine-parsed by
  `extract_english_anchors()`; all 8 must differ).
- Writer places that English word in the sentence immediately preceding a
  `[[tag_xxx]]` marker line. The marker gives the formatter a mechanical split
  point (no more "move the anchor sentence" instruction).
- Gates: prose gate checks each marker's preceding line contains the word;
  `validate_episode` checks the LAST line of the narrative segment preceding
  each tag segment contains the word. No Thai phrases appear in the prose at
  all — the tag itself is the Thai quiz.

### 7. No leakage of old Sangwan-specific rules; generic rules kept procedurally
- Kept (all enforced by `validate_episode`, not by exhortation): segment
  pattern narrative 4–6 / tag / narrative 2–3 / tag / narrative 2–3 (which also
  guarantees the required 8–12 narrative lines per act), decision schema
  (3 choices easy/medium/hard, 10–20-word concrete descriptions, pass delta
  1–2 / fail −1..0, outcomes first-person PC speech beginning "I "), narration
  only via char_narrator (acid test + third-person heuristic), no duplicate
  dialogue/choices, pass≠fail, tag set matches assigned set, valid ids.
- Deleted as Sangwan-specific or contradicting the brief: name bridges,
  death/ghost/memory word-bans, refrain machinery (`extract_refrain_words`,
  refrain-per-act gate), wonder-beat requirements, "SECRET IS NEVER THE
  SUBJECT" sections, fact-ledger rules naming Nim/the PC's class, simile bans
  tied to the old style guide (the general "no technique vocab" gate covers the
  failure mode they guarded).

## Design decisions where the brief was ambiguous
- **Probe removed rather than kept informational.** The brief says keep three
  stages and record gate failures; the probe's only downstream effect was
  restarts, and its questions were Sangwan-flavored. Removing it makes a run
  exactly 3 calls (budget-friendly). Easy to re-add later as a report-only
  stage if the PO wants comprehension telemetry.
- **Exit code:** 0 whenever parseable episode JSON was written (even with gate
  failures, since the brief says continue anyway and triage later); 1 only when
  no parseable JSON exists. Status string in the report distinguishes the cases.
- **English anchor word enforced on the LAST line before the tag** (the
  strictest reading of "the line immediately preceding the tag segment"), with
  word-boundary case-insensitive matching. If the planner fails to emit a
  parseable word for a tag, that tag's anchor check is skipped (recorded as a
  plan-gate failure) rather than crashing the run.
- **Tag markers (`[[tag_xxx]]`)** were introduced as the writer→formatter
  interface so segment splitting is mechanical; without them the formatter had
  to infer tag positions from Thai anchors, which no longer exist in the prose.
- **Private plan goes to the planner only** (not "planner + writer with
  instructions to hide it") — the strongest procedural reading of the
  philosophy section.
- **`char_*_private.md` no longer picked up by `find_world_file`** for the
  public character texts (it previously preferred `_private` files for ALL
  stages — that was the original secret-leak path).

## Checks performed (dry run, no API calls)
- `python3 -c "import driver"` and `py_compile` — OK.
- `python3 driver.py --help` — OK (argparse; `--model-probe` removed).
- Gate unit smoke tests (in-memory): `check_plan` passes a clean outline and
  flags full names / missing anchor words / technique words;
  `extract_english_anchors` parses the strict bullet shape; `check_prose`
  validates marker set + preceding-line anchor word; `validate_episode` flags a
  last-line-before-tag missing the English anchor word and accepts one that
  has it; `build_name_map` parses both nickname formats in characters.json.

## Headwinds / tailwinds
- Headwind: the old driver's gate code was deeply intertwined with the retry
  machinery (checkers called per attempt, format checker with side-channel
  error list); a near-wholesale rewrite of driver.py was cleaner than surgical
  edits. Also the anchor-word English gloss in `tags.json` vocab items is
  phrase-level, so the planner (not code) picks the single unifying word.
- Tailwind: `characters.json` names carry nicknames in a parseable format, so
  nickname enforcement is fully mechanical and character-agnostic; the private
  files on master follow a uniform `char_*_private.md` naming, so secret
  routing needs no per-character configuration.
