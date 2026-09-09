# Episode pipeline (atomic plan → prose lines → deterministic format)

Episode generator for the Thai-language educational RPG. Sprint-2 architecture:

1. **PLAN (atomic decomposition, 4 LLM calls)** — step 1 (`prompts/plan.md`)
   produces a base outline (sticky situation + numbered concrete beats in
   narrative order, PRESENT: staging lines) from the full context including
   the foregrounded character's private plan (`storytelling/private/`,
   planner's eyes only). Steps 2–4 (`prompts/plan_step.md`) are small
   "here's the outline, give it back with X added" calls: (2) STAKES: beat +
   ENTRANCE beats + act-1 speaker budget, (3) one DECISION beat per act
   (dilemma speaker, 3 attributed options, verbatim PASS/FAIL outcome
   events), (4) TAG PLAN with one English anchor word per tag + TAG-marked
   beat pairs (Thai-phrase beat, then English-anchor-word beat).
2. **PLAN GATE** (mechanical) → if failures, ONE spot-edit pass
   (`--model-edit`) with the artifact + the specific failure list; re-gate
   once; record whatever remains. No loops.
3. **PROSE (1 LLM call)** — `prompts/prose.md` turns the outline into
   STRUCTURED PROSE LINES: `## Act N` headers, `PLACE:` lines, and
   `NARRATOR:` / `<Nickname>:` prefixed lines with `[[tag_xxx]]` markers.
   The writer never sees the private plan or the world files — only the
   outline, the nickname list, and the tag-anchor checklist.
4. **PROSE GATE** → one spot-edit pass if failures → re-gate → record.
5. **FORMAT (deterministic, NO LLM)** — `format_episode()` in driver.py
   parses the prose lines mechanically: splits at markers into the exact
   segment pattern (narrative 4–6 / tag / narrative 2–3 / tag /
   narrative 2–3), maps speaker prefixes and PLACE names to ids, and builds
   each act's decision JSON VERBATIM from the plan's DECISION beats. It
   hard-fails (record + exit 1, no episode written) on anything it cannot
   map — it never invents content.
6. **FORMAT GATE** — full mechanical validation (schema, counts, ids,
   anchors, Thai phrases, decision rules, duplicates, narrator heuristics)
   as a detector; failures are recorded in the report.

Tag/vocab rule (PO): the Thai phrase (fixed per tag by
`assign_thai_phrases()` from `public/tags.json` vocab) appears earlier in
the segment preceding its tag, worked into context; the line IMMEDIATELY
before the tag carries the English anchor word; nothing glossed after a tag.

## Usage

```bash
export OPENROUTER_API_KEY=sk-or-...
python3 driver.py \
  --ep-id ep_004 \
  --foreground char_phum \
  --places place_ash_urn,place_letter_writers_landing \
  --tags tag_020,tag_284,tag_317,tag_141,tag_219,tag_153,tag_339,tag_325 \
  --model-plan  deepseek/deepseek-v3.2 \
  --model-prose deepseek/deepseek-v4-flash \
  --model-edit  deepseek/deepseek-v4-flash \
  --out  /path/ep_004.json \
  --report /path/ep_004_report.md
```

Exactly 8 tag ids. Character/place context: `/mnt/agents/output/world/`
(falling back to `public/characters.json` / `places.json`); private plans:
`storytelling/private/char_*_private.md` (planner only).

## Cost notes

A run is 4 plan calls + up to 1 plan spot-edit + 1 prose call + up to 1
prose spot-edit; the format stage is free. Temperatures: plan base 0.7,
plan steps 0.4, prose 0.8, spot-edits 0.3. Token usage and cost (via
`MODEL_PRICES` in driver.py) are recorded in the report, along with gate
results before/after each spot-edit.
