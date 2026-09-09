# Sprint 4, Pass 2 — CHANGES8 (formatter honesty, composed density, dilemma diversity, lints)

**Outcome: NO EPISODE SHIPPED.** Both allowed attempts aborted on FATAL
contracts, per rule 1 (the PO prefers a loud abort over a silently
repaired episode). ep_007's current artifact remains sprint4/pass1's.

## Fixes implemented (all committed, gate-tested via unit smoke tests)

1. **Formatter honesty** (`format_episode`): verbatim
   concatenation/merging and marker repositioning are REMOVED. The
   formatter never merges, reorders, or repositions anything. Every
   segment outside contract (too few OR too many, 1-line segments
   included) and every act outside 8-12 lines is FATAL — no JSON, loud
   report. The only repair path is the prose spot-edit (one pass, per
   the standing rule), which receives the count failures verbatim.
2. **Composed density at the plan level** (not merging): plan gate now
   requires every act-1 segment-1 beat (up to the first TAG pair) to
   carry 2+ plan elements via `carries:` annotations, and rejects any
   run of 3+ consecutive single-element beats anywhere in the outline.
   Writer prompt unchanged in kind: one beat = one line, beats arrive
   pre-loaded.
3. **Dilemma-line diversity**: plan gate compares the first 3 words of
   the four DECISION dilemma lines; 4-of-4 identical = failure. Plan
   step 3 now requires each dilemma as in-character dialogue by a NAMED
   character reacting to the immediate situation ("a clerk frets about
   his ledger; a boatman talks weather"), no two opening alike.
4. **Cheap lints** (prose gate + validate_episode where applicable):
   (a) markdown asterisks anywhere in prose/shipped text;
   (b) narrator spoiler words (forged/forgery/fake/stolen) — verdict
   words banned from narration for unrevealed facts;
   (c) junk stage directions that restate the speech act ([asks],
   [responds], [frowns], [sighs], [nods], [smiles], [murmurs], …) —
   physical content or empty brackets;
   (d) orphaned-object gate (plan side): pockets/tucks/hides/stows/
   slips/steals + article + noun ⇒ the noun must reappear in a later
   beat, else failure (catches the stolen-chit class);
   (e) double-entrance gate: a character gets at most one ENTRANCE beat.
   Smoke-tested: all lints fire on synthetic bad prose.
5. **Act length**: 8-12 lines per act enforced as FATAL at format.

## The two attempts (cap respected)

- **Attempt 1**: plan gate 19 problems; the weighted guard DISQUALIFIED
  the plan spot-edit (machinery stripped / FATAL class grew) — the guard
  worked as designed. Prose draw came back truncated (only act 1); the
  prose spot-edit would have made it worse (22 vs 6) and was discarded;
  formatter FATAL ("prose does not have exactly acts 1-4"). No JSON.
- **Attempt 2**: plan gate 34 → 27 after spot-edit, but no costed STAKES
  beat survived — plan FATAL, episode aborted before prose. (A mid-run
  transport failure — v4-flash exhausting 8 retries at the 14000-token
  prose cap on the annotation-heavier plan — was fixed by raising the
  prose cap to 24000; that fix ships regardless.)

## Cost
~$0.030 across the two attempts (attempt 1 ≈$0.016, attempt 2 ≈$0.014).
No episode JSON was produced; intermediates (reports) are in this folder.

## Evidence the new machinery works (from the runs' logs)
- Weighted guard disqualified a machinery-stripping plan edit in
  attempt 1 — the sprint-3 pass-2 fix holding under load.
- Formatter FATAL fired loudly on both contract violations (truncated
  acts; missing STAKES) — the honesty contract does what the PO asked.
- The orphaned-object gate's target class (pass-1's stolen chit) is now
  mechanically detectable at plan time.

## Headwinds
- **The plan spot-edit is now the bottleneck.** With the full gate suite
  (machinery + density + budgets + outcomes + lints), raw plans carry
  19-34 failures; one v4-flash edit pass lands at 18-27 — and this pass
  it twice failed to clear a FATAL class (truncation, then STAKES). The
  suite has outgrown a single generic edit pass. Procedural candidates
  for sprint 5: (a) per-class targeted edit prompts (the editor gets ONE
  failure class at a time, still one pass total per class? — conflicts
  with single-pass discipline; alternatively (b) fold the highest-failure
  classes (STAKES cost clause, outcome voice, beat budgets) back into the
  atomic plan steps' instructions so the raw plan needs less editing;
  (c) accept plan-side FATAL aborts as the cost of honesty and budget
  2 plan-stage retries within an attempt.
- v4-flash truncation on long inputs: mitigated by the 24000 cap, but
  reasoning-heavy calls remain the cost/reliability center.

## Tailwinds
- All five fix areas are mechanically gated and unit-verified; the gates
  fired on cue in both attempts. When a clean plan draw lands (attempt-1
  plans have repeatedly come within one edit of the FATAL classes), the
  pipeline now ships honestly-formatted JSON with density, dilemma
  diversity, and clean stage directions — or ships nothing.
