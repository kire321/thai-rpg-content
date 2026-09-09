# Sprint 5, Pass 1 — CHANGES9 (plan fold-in, density, wonder content, phrase variety)

**Outcome: NO EPISODE SHIPPED.** Both allowed attempts aborted FATAL
(loud abort over silent repair). ep_008 remains unproduced; ep_007
(sprint4/pass1) is still the current shipped artifact.

## Implemented (committed, gate-tested)

1. **PLAN FOLD-IN** — the top FATAL classes moved into the atomic
   step instructions:
   - step 2: required STAKES sentence shape `<want>, or <concrete cost>`
     with the 'or' clause called out as machine-checked, beats 1-6;
   - step 3: "EVERY one of the six PASS/FAIL texts begins with the word
     'I' (machine-checked)";
   - step 5: the beat budget stated AS the segment contract (one beat =
     one prose line; seg1 4-6 / seg3 2-3 / seg3 2-3 beats; total 8-12 +
     DECISION), with merge-beats-here instruction;
   - plan.md: 8-12 beats per act stated at outline time.
   RESULT: raw plan failure count 24 (attempt 1) / 37 (attempt 2) —
   improved from sprint-4's 48 but NOT the <10 target. Dominant
   remaining classes: dilemma voice (~8/run), ENTRANCE coverage,
   place-mention noise, carries coverage. The fold-in moved ~half the
   failures; the classes that survive are ones the steps can't fully
   pre-empt (they depend on cross-step interactions: step-5 tag
   insertion un-balances step-2 budgets; dilemma voice is a v3.2 habit
   that instruction alone hasn't broken).
2. **DENSITY**: act-1 seg-1 beats each 2+ annotated elements; no 3+
   consecutive single-element beats (gate kept from sprint 4; fold-in
   instruction unchanged). Attempt-2 plan carries annotations from beat 1.
3. **WONDER content**: machinery step already requires shape + concrete
   content per act; verified present in both attempts' plans (4 shapes).
4. **DIALECTICAL PHRASE VARIETY** (new): place private plans are now
   loaded and fed to the planner's machinery step as a second phrase
   pool; the instruction requires ≥2 DISTINCT phrases (char + place)
   when available, no phrase on >2 beats, no coining when the private
   plans provide. GATE: THESIS beats — ≥3 occurrences incl. act 1,
   ≥2 distinct quoted phrases, ≤2 beats per phrase (smoke-tested).
   VISIBLE IN ATTEMPT-2 PLAN: `THESIS "delivery gone sideways"` (the
   character's) and `THESIS "debt held in grain"` (the place's) — 2
   beats each, exactly at the gate's limit, drawn from BOTH pools as
   the PO directive required.
5. Kept: weighted keep-better guard (fired correctly attempt 2 —
   DISQUALIFIED a machinery-stripping edit), full gate suite, no-merge
   formatter, 2-attempt cap.

## The two attempts
- Attempt 1 ($0.011): raw plan 24 failures; the plan spot-edit kept
  TRUNCATING at the 16000 cap (8/8 retries, transport); the surviving
  plan picked 7/8 tags → FATAL.
- Attempt 2 ($0.0144; spot-edit cap raised to 24000): raw plan 37
  failures; spot-edit disqualified by the weighted guard; prose draw
  truncated after act 3 even at 24000 tokens → FATAL "acts 1-3 only".
  No JSON either attempt.

## Headwinds
- **v4-flash can no longer fit a full 4-act prose generation in one
  call** now that plans carry machinery + carries annotations + phrase
  pools: reasoning + 4 acts exceeds even 24000 output tokens. Two
  consecutive attempts died on transport, not gates. RECOMMENDATION
  (sprint 6): generate prose PER ACT (4 calls, each with the full
  outline but instructed to write only act N) — mechanically trivial,
  halves peak tokens, and per-act calls are independently gateable
  before assembly. Alternatively a non-reasoning prose model.
- The spot-edit restore-retry for machinery has never yet succeeded;
  the guard's disqualify-and-keep-original path is doing all the work.

## Tailwinds
- Phrase variety worked on the first try: both pools mined, gate-shaped
  distribution (2+2 beats), zero coining.
- The plan-side pipeline is stable and cheap ($0.005); every failure
  this pass was downstream transport.
- Fold-in direction confirmed: raw plan failures dropped 48 → 24-37;
  further folding (dilemma voice examples in step 3; ENTRANCE checklist
  derived from PRESENT in step 2) is the same lever again.
