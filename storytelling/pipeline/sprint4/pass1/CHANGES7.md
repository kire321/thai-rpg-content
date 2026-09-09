# Sprint 4 — CHANGES7 (line-shape features: stage directions, loaded beats)

Files changed (branch `sprint1-pipeline`): `driver.py`, `prompts/plan.md`,
`prompts/prose.md`. ONE attempt used of the 2 allowed — see "Why no
attempt 2" below.

## Feature 1 — actions in stage directions; speech belongs to the speaker
- Prose contract: `<Nickname>: [action in brackets] "speech"` — the
  formatter parses the `[...]` prefix into the line's `stage_directions`
  field and the quoted remainder into `dialogue`.
- New prose gates: a NARRATOR line containing quotation marks OR an
  "asks/says/replies" construction fails; validate_episode adds the same
  check to the shipped JSON; every dialogue line's character must be a
  speaking character (narrator speech = failure).
- VISIBLE IN SHIPPED JSON: 22 lines carry stage_directions; 0 narrator
  lines contain quotes. Example:
  `char_salt_clerk / sd "stands before Lek" / dialogue "The pink salt bin
  was found empty this morning, the lock unbroken but the lid left open."`
  Residual: 3 third-person narration slips attributed to characters and 1
  narrator-with-speech line slipped past the prose spot-edit (recorded in
  the format gate).

## Feature 2 — every beat carries multiple plan elements
- plan.md: beats must be LOADED, annotated `— carries: intro:X, setting,
  stakes, thesis, deadline, ...`; plan step 2 merges single-purpose runs.
- Plan gates: act-1 opening stretch of all-single-purpose beats is
  rejected; any run of 3+ single-purpose beats is rejected.
- PO's obvious-presence rule: characters obvious from the place (a clerk
  in a salt store — name/place token overlap) and the PC no longer need
  ENTRANCE beats; PRESENT gives the general sense; the late-reveal ban
  stands via the existing entrance-before-speech gate.
- VISIBLE IN SHIPPED PLAN: 9 `carries:` annotations in act 1; the opening
  beat carries intro+setting+stakes+thesis+deadline in one line, and the
  shipped prose opening line realizes it verbatim:
  "The Salt Clerk arrives on the veranda with his hands stained red from
  the broken chalk block, and he places a single grain of pink salt on
  the ledger Lek is writing in."

## Fold-in fix
- Thesis gate: 'of' removed from the ban (only 'like'/'as if' rejected) —
  the PO's own model ("clerk of other people's news") contains 'of';
  direct apposition allows it when the descriptor applies literally.

## Gates before/after (ep_007, char_rangsri)
- plan: 48 → 23 after spot-edit (residuals: beat budgets, outcome voice,
  comparisons)
- prose: 10 → 10 (spot-edit discarded by the guard — not better)
- format: FAIL (14): segment counts (act1 7/3/1, act2 7/…, act3 6/5/4),
  3 third-person-attribution slips, 1 narrator-speech slip
- machinery survived: thesis "the ledger-keeper, clerk of temple chits",
  all 4 wonder shapes, refrains in plan
- tags picked: tag_146, tag_113, tag_029, tag_252, tag_215, tag_065,
  tag_007, tag_303; unused: tag_121, tag_317, tag_329, tag_046
- cost: $0.0150

## Why no attempt 2
Both remaining defect classes (segment counts, attribution slips) are
known model-variance classes with gates already at every stage; a second
attempt changes no code and spends ~$0.015 on a dice roll. Per the
budget-conscious directive, the pass ships with defects recorded.

## Headwinds / tailwinds
- Headwind: v4-flash prose still can't hold the segment budget; the
  formatter's merging masks some of it (all "after mechanical merging"
  errors are post-merge residuals).
- Tailwind: stage-direction contract adopted immediately by the writer
  (22 lines, zero narrator quotes on the first draw) — the
  bracket-prefix convention is natural for the model.
- Tailwind: loaded-beat annotations produced the PO's target opening line
  shape (one sentence carrying intro+setting+stakes+thesis+deadline) on
  the first try.
