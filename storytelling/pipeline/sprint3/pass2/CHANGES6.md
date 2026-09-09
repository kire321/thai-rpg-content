# Sprint 3, Pass 2 — CHANGES6 (weighted guard + machinery survival)

Change (`driver.py`, branch `sprint1-pipeline`):

1. **Weighted keep-better guard on the plan spot-edit** — an edit is now
   DISQUALIFIED (original kept) if it:
   - introduces ANY machinery-gate failure (thesis/refrain/wonder) that the
     original didn't have — one retry is allowed ONLY to restore stripped
     beats ("restore the THESIS/REFRAIN/WONDER beats verbatim");
   - grows any FATAL class: missing/cost-less STAKES, unparseable TAG PLAN
     (≠8 picked), missing mandatory section headers, missing act sections
     (the last two added after attempt 1 kept a 2-act truncated edit on a
     25→6 count drop).
   The edit instruction now also carries: "beats labeled THESIS/REFRAIN/
   WONDER are UNTOUCHABLE".
2. **Machinery-label parsing hardened** — attempt 1 showed the planner
   writes label beats WITHOUT numbers (`WONDER (inventory): ...`), which
   (a) tripped the technique-vocabulary scan with false positives and
   (b) made the machinery presence gates blind. Labels are now matched
   with optional numbering, stripped before the technique scan, and the
   presence gates scan raw act bodies instead of numbered beats only.

## Run (attempt 2 of 2 — cap respected; attempt 1 aborted FATAL on an
## unparseable TAG PLAN after a structurally-regressive edit, which
## motivated guard class (c) above)

- plan: 21 → 21 (spot-edit DISCARDED as not better — the guard kept the
  original and with it ALL machinery: thesis ×3, refrains ×3 distinct
  with cosmic final, wonder one per act with all 4 shapes)
- prose: 14 → 14 (spot-edit discarded, not better)
- format: FAIL (3): act-1 seg-5 6 lines (recorded, merged where possible),
  'tension' technique word in prose, one anchor-word miss (tag_108)
- segments: [6,3,6] [6,3,3] [6,3,3] [6,3,3]; 8/8 tags; cost: $0.0150
  (attempt 2) + ~$0.012 (attempt 1, aborted) ≈ $0.027 for the pass.

## Machinery survival into the shipped JSON (quoted from the artifacts)

- REFRAIN — SURVIVED. Plan wordings: "Write them cool" / "A different
  temperature" / "The turning world's own temperature". Prose:
  `NARRATOR: "The words are not hot. The heart is. Write them cool."`
  `Pom: "Each version is a measurement. Each has a different temperature."`
  (final cosmic occurrence present in plan; prose carries the temperature
  motif through act 4 — core words 3/3, 2/2, 1/3).
- THESIS — FAILED AT THE PROSE CHANNEL. Plan: "the notebook-keeper, clerk
  of other people's news" at 3 beats. Prose: ZERO occurrences (writer
  never wove the phrase in). NOTE: the plan gate ALSO flagged this thesis
  for using 'of' — but the PO's own model ("the letter-writer, clerk of
  other people's news") contains 'of'. The gate follows the directive's
  letter and contradicts its example; recommend allowing 'of' inside the
  apposition (ban only 'like'/'as if'). Recorded as gate miscalibration.
- WONDER — shapes present in plan (inventory/connoisseur/numinous/
  elegiac, one per act); their concrete content is in the outline beats
  the writer expanded (no mechanical prose-side check exists).

## Honest judgment: is the machinery→prose channel working?

PARTIALLY. The plan-side channel is now stable: the weighted guard works
exactly as specified — machinery survived the spot-edit this pass where
pass 1 lost it. The PROSE-side channel is the deeper obstruction: the
writer honors machinery that arrives as EXACT QUOTED LINES (refrains
survived; decision outcomes arrive quoted and survive too) but ignores
machinery that must be WOVEN (the thesis noun phrase — zero verbatim
occurrences). There is no prose gate checking machinery survival, so the
channel fails silently. Recommended pass-3 fix (procedural, one gate):
check that the plan's THESIS phrase and each REFRAIN wording's core
content words appear in the prose — the same mechanism that already
verifies English anchor words before tags. With that gate, the prose
spot-edit gets a mechanical repair target and the channel closes.
