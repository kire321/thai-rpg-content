# Sprint 2, Pass 1 — Structural rebuild (CHANGES3)

Files changed (branch `sprint1-pipeline`, commits `8677901` + follow-up):
`driver.py`, `prompts/plan.md`, `prompts/plan_step.md` (new),
`prompts/prose.md`, `prompts/format.md` (deleted), `README.md`.

## Map to the PO's 5 greenlit items

### 1. Deterministic formatter (no LLM)
- `format_episode()` in driver.py: pure-Python parser. The writer now emits
  STRUCTURED PROSE LINES (`## Act N` headers, `PLACE:` lines, `NARRATOR:` /
  `<Nickname>:` prefixed lines, `[[tag_xxx]]` markers trailing the line they
  follow). The formatter splits at markers into narrative 4–6 / tag /
  narrative 2–3 / tag / narrative 2–3, maps speaker prefixes → char ids and
  PLACE names → place ids (exact, then a unique-token fuzzy fallback),
  assigns tag ids in marker order, and builds each act's decision JSON
  VERBATIM from the plan's DECISION beats (`parse_decisions()` — dilemma
  speaker, 3 attributed options, PASS/FAIL outcome events, delta +1/0).
- Hard-fail behavior: any unmappable speaker/place/marker-count → recorded
  as FATAL in the report, no episode JSON written, exit 1. It never invents
  content. (First pass-1 attempt demonstrated this: 4 unmappable PLACE
  variants → clean failure.)
- `prompts/format.md` deleted; `--model-format` CLI arg replaced by
  `--model-edit`.

### 2. Editor subsubagent replacing gate+retry
- `spot_edit()`: artifact + exact gate-failure list → "fix exactly these,
  change nothing else" (temp 0.3, v4-flash). Applied after the plan gate and
  after the prose gate. ONE pass per stage; the gate re-runs once and
  whatever remains is recorded. No loops anywhere.
- Pass-1 evidence: prose gate 2 problems → **PASS** after spot-edit; plan
  gate 10 → 5 (3 of the original 10 were detector false positives, see
  headwinds).

### 3. Atomic plan decomposition
- 4 incremental calls, all deepseek-v3.2: (1) `plan.md` base outline
  (sticky situation + concrete beats + PRESENT lines, full context incl.
  private plan); (2–4) `plan_step.md` "here's the outline, give it back with
  X added": +STAKES/ENTRANCEs/speaker budget, +DECISION beats (new
  machine-parsed shape with dilemma speaker and per-option attribute),
  +TAG PLAN (English anchor words + TAG-marked beat pairs).
- Cost: 4 calls ≈ $0.0049 (12k in / 7.3k out tokens) — inside the ~$0.01
  budget with room for the spot-edit pass.

### 4. Thai rule clarification (PO verbatim)
- Plan step 4 creates, per tag, a pair of ADJACENT beats: first beat
  (prefixed `TAG tag_xxx:`) carries the Thai phrase verbatim in context; the
  next beat carries the English anchor word and becomes the last line before
  the tag. prose.md STEP 3 implements exactly that; nothing Thai elsewhere,
  nothing glossed after a tag. Gates unchanged (Thai in the stretch before
  the marker; English word in the immediately preceding line).
- Pass-1 evidence: prose passed the Thai/anchor checks after one spot-edit
  (2 anchor-word misses → 0).

### 5. Gates as detectors + single-pass discipline
- All iter2 gates kept. Additions this pass: prose gate now checks segment
  line counts (4–6/2–3/2–3) so count blowouts feed the spot-edit pass
  instead of surfacing at format time; plan gate strips echoed nickname-guide
  lines before the full-name scan (false-positive fix); plan gate requires
  the DECISION beat's new shape (dilemma speaker + 3 attributes).
- Pipeline order: plan steps → plan gate → ≤1 spot-edit → prose → prose
  gate → ≤1 spot-edit → deterministic format → format gate → report.

## Pass-1 run (ep_004, char_phum) — results

Gate results (before → after spot-edit):
- plan: 10 → 5 (real residual: 2 out-of-episode place names mentioned in
  dialogue beats — gate arguably over-strict there; 3 of the 10 were the
  false-positive name-guide flags, since fixed)
- prose: 2 → **PASS**
- format: FAIL (27) — dominant class: segment line counts (writer put both
  markers late: segment 1 has 12–20 lines, segment 5 has 0). This failure
  class is now caught at the PROSE gate (added post-run) where the spot-edit
  can fix it; also 2 narration-attribution slips, 1 dilemma line containing
  its speaker's name.

Cost breakdown (this run, $0.0091 total):
- plan steps (v3.2): $0.0049 (12,008 in / 7,330 out)
- plan spot-edit (v4-flash): $0.0016 (3,527 in / 7,363 out — v4-flash
  reasons heavily before re-emitting)
- prose (v4-flash): $0.0007 (4,910 in / 1,371 out; 3 empty/truncated
  attempts retried by the API layer first)
- prose spot-edit (v4-flash): $0.0007 (1,514 in / 3,030 out)
- format: $0 (deterministic)

Outputs: `/mnt/agents/output/sprint2/pass1/ep_004.json` (+ .plan.md,
.prose.md, ep_004_report.md). Status: COMPLETED WITH GATE FAILURES.

## Headwinds
1. v4-flash burns most of its completion budget on reasoning: an 8000-token
   cap truncated full-outline re-emission (crash, one lost run ~$0.009);
   spot-edit caps raised to 16000. Also 3 empty/truncated prose attempts
   before a good one (API-layer retry absorbed them).
2. Latent pre-existing bug found: `run_stage_once` referenced `probs`
   instead of `problems` — crashed the first time a prose gate failed in
   the new pipeline. Fixed.
3. Writer places both tag markers late in the act (count blowout) — the new
   prose-gate count check + spot-edit should repair this on the next pass;
   if not, the plan's TAG beat pairs may need explicit "lines 1-6 / 7-9 /
   10-12" budgeting.
4. Place gate over-strictness: dialogue beats mentioning "The Pawnshop"
   (not the scene location) are flagged. Candidate: restrict the scan to
   PRESENT/travel beats.

## Tailwinds
- First-ever prose gate PASS (after one spot-edit); first end-to-end run
  with zero LLM inventing JSON content — every format-stage error is now a
  measurable count/attribution issue, not silent corruption.
- Decisions come verbatim from the plan: the entire iter1/iter2 class of
  "formatter paraphrased/dropped/duplicated decisions" is structurally gone.
- Plan decomposition works: base outline passed its checks immediately, and
  each additive step kept the outline intact.
