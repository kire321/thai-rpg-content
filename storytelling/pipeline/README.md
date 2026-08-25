# Episode pipeline (plan → prose → format + probe)

3-stage episode generator for the Thai-language educational RPG. A Python driver
moves data between three separate LLM prompts and enforces quality with
mechanical gates plus a reader-comprehension probe. The driver never hand-edits
generated content; every fix is done by re-prompting the responsible model.

## Layout

- `prompts/plan.md` — stage 1: structured Markdown plan (sticky situation,
  per-character motivations shown-not-told, central object + ownership, act map,
  reader questions, secret handling, tag plan with 8 Thai anchor phrases).
- `prompts/prose.md` — stage 2: 4 acts of flowing prose (~250–400 words/act),
  Thai anchors with dash-glosses, decision moments inline as
  `[easy]/[medium]/[hard]` + `PASS:`/`FAIL:` first-person lines.
- `prompts/format.md` — stage 3 (cheap model): reformats prose into the exact
  episode JSON schema (segment pattern `narrative 4–6 / tag / narrative 2–3 /
  tag / narrative 2–3`, decision schema with 3 choices, delta ranges).
- `driver.py` — orchestrator (Python 3, stdlib + urllib only).

## Usage

```bash
export OPENROUTER_API_KEY=sk-or-...
python3 driver.py \
  --ep-id ep_002 \
  --foreground char_sangwan \
  --places place_letter_writers_landing,place_pawnshop \
  --tags tag_254,tag_083,tag_167,tag_154,tag_337,tag_120,tag_197,tag_041 \
  --model-plan  anthropic/claude-sonnet-4 \
  --model-prose anthropic/claude-sonnet-4 \
  --model-format openai/gpt-4o-mini \
  --out  /path/ep_002.json \
  --report /path/ep_002_report.md
```

Exactly 8 tag ids (2 per act, resolved to id+name from
`thai-rpg-content/public/tags.json`). Character/place context is read from
`/mnt/agents/output/world/char_*.{md,json}` / `place_*.{md,json}` (falling back
to `public/characters.json` / `places.json`).

## Stage gates

1. **plan gate** — all 7 mandatory section headers exist; WHY IT MATTERS has
   entries for Pricha and the foregrounded character; CENTRAL OBJECT names an
   owner. Else re-prompt (max 3).
2. **prose gate** — zero hits on banned strings/patterns ("as if", "forg",
   death-family words, "not ... but", "Or X. Or both.", sentence-opener
   "Not X", "not the ", "No. Only"); all 8 Thai anchor phrases from the plan
   appear. Else re-prompt (max 3).
3. **format gate** — full mechanical JSON validation: parses; id matches; 4
   acts with id/title; exact segment pattern and line counts; decision schema
   exact (3 choices easy/medium/hard, descriptions 10–20 words, deltas pass
   1–2 / fail −1..0); all character/place ids exist; narration only
   char_narrator (heuristic); outcomes first-person non-narrator; no duplicate
   dialogue; no duplicate choice descriptions; pass≠fail; tag set matches.
   Else re-prompt format (max 3); if still failing, regenerate prose once with
   the errors attached and reformat.
4. **reader probe** — a zero-context reader call (ids stripped) answers 4
   questions; a judge call compares against the plan's READER QUESTIONS section
   (PASS/FAIL per question). Any FAIL restarts the whole pipeline from stage 1
   with a deficiency note (max 2 restarts).

## Cost notes

Temperatures: plan 0.7, prose 0.8, format 0.2. Max tokens: 6000 / 9000 / 16000.
Token usage is taken from API responses and priced via the `MODEL_PRICES` dict
in `driver.py` ($/M tokens, prompt/completion) — update it for the models you
use. Typical successful run: 3 generation calls + 2 probe calls; worst case is
bounded (3+3+3 + prose regen + probe, ×3 full restarts).
`report.md` records per-stage attempts, probe verdicts, tokens, and cost.
