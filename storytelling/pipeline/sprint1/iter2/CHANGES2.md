# Sprint 1, Iteration 2 — Procedural fixes mapped to editor feedback defects

Files changed (branch `sprint1-pipeline`, commits `e21b302` + `20c1d33`):
`storytelling/pipeline/driver.py`, `prompts/plan.md`, `prompts/prose.md`,
`prompts/format.md`, `README.md`.

## Defect → fix map

### 1. Outcomes were generic stock phrases
- Planner now writes each PASS/FAIL as ONE CONCRETE EVENT resulting from THAT
  option's action, naming the scene's objects (plan.md STEP 6, with a worked
  example). Writer copies the DECISION block EXACTLY (prose.md STEP 4);
  formatter copies outcomes verbatim (format.md, transcription-checked).
- Mechanical gate (plan): every PASS/FAIL must share ≥1 content word with its
  choice text or the act's beats; choices must share ≥2 content words with the
  established page (sticky situation + beats so far).
- Result iter2: outcomes are concrete and bound ("I file the correction and
  the Timekeeper bows, hand over heart."). 2 outcome-binding failures remain
  recorded in the plan gate (model non-compliance, not missing machinery).

### 2. Zero Thai — tag mechanic non-functional
- `assign_thai_phrases()` in driver.py deterministically fixes one Thai phrase
  per tag from `public/tags.json` vocab items (1–6 Thai words, no trailing
  ellipsis). Routed: driver → planner (TAG PLAN bullet must contain it
  verbatim, plan-gated) → writer (ANCHOR_CHEAT checklist + prose gate:
  phrase must appear in the stretch preceding its marker) → JSON gate:
  phrase must appear in the segment preceding its tag. English anchor word
  stays in the line immediately before the tag (PO rule), checked as before.
- Result iter2: Thai present in prose and JSON (iter2a: all 8 phrases placed;
  iter2b: writer paraphrased/dropped 6 assigned phrases — caught by the gate,
  recorded; stochastic model non-compliance).

### 3. "like"/"as if" simile flood (7+ in iter1)
- Procedural source fix: outline beats must be DIRECT ASSERTIONS; the words
  "like"/"as if" are machine-rejected in the plan (0 allowed), so the writer
  never sees a comparison to expand. Prose gate: ≤2 allowed.
- Result iter2: **0 similes in prose and JSON** (was 7+).

### 4. Stakes never stated in act 1
- Mandatory labeled beat: `STAKES:` — a character says aloud, in quotes, what
  they want and what it costs; must land by beat 6 of act 1. Plan-gated.
- Result iter2: STAKES beat present in both runs ("Correct the time or the
  land goes to the district.").

### 5. Characters speaking without introduction / act-1 speaker budget
- Outline grammar: each act opens with `PRESENT: <nicknames>`; any character
  not in act-1 PRESENT needs an `ENTRANCE <nickname>:` beat (with concrete
  description) before their first speech beat; opening stretch (up to STAKES
  beat, max beat 6) allows PC + ONE other speaker. All plan-gated
  (`_names_in` matches nicknames and "The X" name variants).
- Result iter2: entrances present in prose; plan gate recorded remaining
  violations (boatman speaking pre-entrance, one budget overflow in iter2a).

### 6. Choices referencing unestablished facts
- Plan gate: choice content-word overlap with established page (≥2) +
  choice may reference only characters on stage or entered.
- Result iter2: gate catches and records violations (e.g. "Demand the
  boatman's testimony" with boatman never entered — iter2b plan gate).

### 7. Format stage regenerating content
- format.md rewritten as "transcription machine": verbatim copy only, markers
  are hard boundaries (inline or own-line), tag ids never substituted,
  decisions mandatory per act, sentence-count self-check.
- New driver gate `transcription_problems()`: every dialogue/description
  string in the JSON must appear verbatim in the prose (normalizing quotes/
  whitespace); invented strings are hard-fail recorded.
- Plan gate now requires a DECISION beat in EVERY act (iter2a root cause of
  the formatter duplicating act-1's decision into act 4).
- Result iter2b: transcription diff caught 15 invented strings (formatter
  still invents when the prose is malformed — now visible in the report
  instead of silent).

### Own iter1 observations
- Writer ignoring anchor words: `ANCHOR_CHEAT` slot restates all 8
  marker→Thai-phrase→English-word bindings OUTSIDE the plan. Partial success
  (iter2a: 2/8 word misses; iter2b: 1 word miss + 6 Thai paraphrases).
- Places constraint: planner gets ALLOWED_PLACES slot; plan gate rejects
  outlines naming other places from places.json; JSON gate rejects lines
  whose place is outside --places + place_veranda. iter2b caught
  place_river_post in act 4.

### Lower priority (cheap ones taken)
- Temporal inversion / telling captions / PC characterization / key-handoff
  charge / refrain machinery: NOT addressed this iteration (need planner
  ordering constraints and PC-beat requirements — candidates for iter3).

## Hotfix during iteration (commit 20c1d33)
- Writer emits `[[tag]]` markers trailing a sentence, not on their own line;
  the gate's full-line regex missed all 8 and the formatter couldn't split
  (74 format errors in iter2a). Made marker matching position-based and
  taught format.md that a marker ends its sentence's segment.

## Runs
- iter2a (before hotfix): plan FAIL 14 / prose FAIL 1 (markers invisible) /
  format FAIL 74. Cost $0.0062.
- iter2b (final, saved outputs): plan FAIL 12 / prose FAIL 9 / format FAIL 58.
  Cost $0.0058. All failures recorded in ep_003_report.md; JSON parses; all
  4 acts have correct 5-segment shape and decision objects.
