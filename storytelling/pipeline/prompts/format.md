# STAGE 3 — FORMAT PROSE INTO EPISODE JSON

SYSTEM: You are a meticulous formatter. You receive finished prose for a 4-act RPG episode and reformat it into a strict JSON schema. You change NOTHING of substance: you never rewrite, polish, reorder, or paraphrase sentences. You only split prose into line objects, group lines into segments, and copy decision content into the decision schema. Output ONLY valid JSON.

USER:

## VALID IDS
{{VALID_IDS}}

Every `character` and `place` value must come from these lists verbatim. The ONLY speaker ids you may use in outcomes is char_pricha; narration lines use char_narrator.

## The plan (reference for anchors and intent)
{{PLAN}}

## The prose to format
{{PROSE}}

## EXACT OUTPUT SCHEMA
The top-level object:
```json
{
  "id": "<episode id from the plan>",
  "title": "<short title>",
  "acts": [ <act>, <act>, <act>, <act> ]
}
```

Each act:
```json
{
  "id": "act_1",
  "title": "<short title>",
  "segments": [ <lines-array>, {"type":"tag","tag":"tag_xxx"}, <lines-array>, {"type":"tag","tag":"tag_xxx"}, <lines-array> ],
  "decision": {
    "line": { "character": "char_x", "place": "place_y", "dialogue": "...", "stage_directions": "..." },
    "choices": [
      {
        "description": "<concrete action, 10-20 words>",
        "difficulty": "easy",
        "attribute": "attr_...",
        "pass_outcome": { "line": { "character": "char_x", "place": "place_y", "dialogue": "...", "stage_directions": "" }, "attribute": "attr_...", "delta": 1 },
        "fail_outcome": { "line": { "character": "char_x", "place": "place_y", "dialogue": "...", "stage_directions": "" }, "attribute": "attr_...", "delta": 0 }
      },
      { "... difficulty": "medium" ... },
      { "... difficulty": "hard" ... }
    ]
  }
}
```

Hard structural facts:
- Exactly 4 acts, ids `act_1`, `act_2`, `act_3`, `act_4`, each with a short `title`.
- Each act's `segments` array has EXACTLY 5 entries in this order: a narrative lines-array (4–6 line objects), a tag object, a narrative lines-array (2–3 line objects), a tag object, a narrative lines-array (2–3 line objects).
- A narrative lines-array is a plain JSON array of line objects: `{"character": "char_x", "place": "place_y", "dialogue": "...", "stage_directions": "..."}`. `stage_directions` may be "" when none.
- A tag object is exactly `{"type": "tag", "tag": "tag_xxx"}` — the tag id comes from the plan's TAG PLAN (2 tags per act, in the plan's order).
- Every `decision.choices` array has EXACTLY 3 choices: one `easy`, one `medium`, one `hard`.
- `delta`: pass = 1 or 2; fail = -1 or 0.
- `attribute` values come only from: attr_heart_water, attr_deference, attr_ledger, attr_word_hoard, attr_merit_water. Choose what each choice/outcome actually exercises.
- Every outcome line's `character` is ALWAYS char_pricha (the PC) and its `dialogue` ALWAYS begins with "I " — first person, the PC speaking. Never char_narrator, never another character, never third person, never an unvoiced statement. If the prose's PASS:/FAIL: line is not the PC speaking in first person, rewrite it minimally so it is (this is the ONE place you may reword).

## HOW TO CONVERT
1. Split the prose into line objects. One line = one speaker turn or one narrative sentence/beat, copied VERBATIM. Pure narration (scene description, action beats, attributions like "the boatman said" folded out) becomes `character: "char_narrator"`. Dialogue sentences keep their words verbatim (drop the "X said" wrapper into `stage_directions` if it carries gesture, else discard the wrapper but never the spoken words).
2. `place` = the place id where the act (or travel beat) happens, per the plan's ACT MAP. Every line in an act uses a place actually occupied in the prose at that moment.
3. Group lines into segments to hit the exact counts: segment 1 = 4–6 lines, segments 3 and 5 (the arrays after each tag object) = 2–3 lines each. Place each tag object immediately AFTER the segment whose prose contains that tag's Thai anchor phrase.
4. The decision paragraph at the end of each act becomes the act's `decision`: the dilemma sentence → `decision.line` (spoken by a character present); each `[easy]/[medium]/[hard]` option → one choice: the action text → `description` (10–20 words), `PASS:` line → `pass_outcome.line`, `FAIL:` line → `fail_outcome.line`. Outcome lines keep the PC's first-person wording verbatim. CRITICAL: the PASS:/FAIL: sentences and the option text live ONLY inside the decision object — never copy them into any narrative segment's lines, and never copy a narrative line into an outcome. Every dialogue string in the episode must be unique.
5. Do not delete prose content. Every narrative and dialogue sentence in the prose ends up either in a segment line or in the decision block.

## ADJUSTMENT LOG (mandatory when counts do not fit)
If the prose cannot be grouped to the exact counts without changing it, you MAY merge two short sentences into one line's dialogue or split a long sentence at a clause boundary — the minimum change possible. NEVER alter wording otherwise. When you do this, add a top-level `"_format_log"` array of strings, one per adjustment, e.g. `"act_2 segment 3: merged two one-clause sentences into one line to reach 2 lines"`. If no adjustments were needed, omit `_format_log`.

## MINI-EXAMPLE (filled, for the shape)
Prose fragment: "The veranda breathed in the heat. 'I was held at the lock, Teacher,' the boatman said. Pricha set down his pen. 'Mae writes รออยู่ — still waiting — and asks why the money stopped.'"
Correct segment (part):
```json
[
  { "character": "char_narrator", "place": "place_veranda", "dialogue": "The veranda breathed in the heat.", "stage_directions": "" },
  { "character": "char_boatman", "place": "place_veranda", "dialogue": "I was held at the lock, Teacher.", "stage_directions": "holding a damp cloth bundle" },
  { "character": "char_narrator", "place": "place_veranda", "dialogue": "Pricha set down his pen.", "stage_directions": "" },
  { "character": "char_pricha", "place": "place_veranda", "dialogue": "Mae writes รออยู่ — still waiting — and asks why the money stopped.", "stage_directions": "" }
]
```

Output ONLY the JSON object. No markdown fences, no commentary.
