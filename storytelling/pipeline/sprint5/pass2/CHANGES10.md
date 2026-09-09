# Sprint 5, Pass 2 — CHANGES10 (per-act prose generation)

**Outcome: NO EPISODE SHIPPED.** Both allowed attempts died on v4-flash
TRANSPORT (token-cap truncations), not on gates. The per-act mechanism
itself worked wherever transport cooperated.

## Implemented (committed)

1. **Per-act prose stage** (`prompts/prose_act.md` + driver rework):
   - 4 calls, one per act; each receives the FULL outline (coherence),
     an act-scoped instruction ("Write ONLY act N"), the act's own 2-tag
     anchor checklist, and a mechanical CARRYOVER (the previous act's
     last two content lines, verbatim) to glue transitions.
   - max_tokens 8000/call (retry at 12000) — a full act's prose is
     ~2-4k tokens; the budget is reasoning headroom.
   - Acts assembled in order; the assembled document still passes through
     the full-document `check_prose` (cross-act marker set, global
     similes) before formatting.
2. **Per-act gate** (`check_prose_act`): segment pattern 4-6/2-3/2-3,
   act length 8-12, PLACE presence+validity, this-act's exact 2 markers,
   anchor word before each marker, zero Thai, narrator-speech ban,
   speaker-prefix mapping, all cheap lints (asterisks, spoiler words,
   junk stage directions), similes, full names, technique vocab.
   Unit-tested: clean act passes; bad place / missing marker flagged.
3. **Per-act failure containment**: gate on arrival → ≤1 spot-edit
   (keep-better) → if FATAL-class failures remain, ONE act-only retry
   (fresh draw, keep the better); transport failures (RuntimeError) now
   keep the best available text instead of crashing the episode — the
   no-merge FATAL contract at format decides, loudly.

## The two attempts (cap respected)
- **Attempt 1**: plan 39 failures, spot-edit DISQUALIFIED by the weighted
  guard (machinery-stripping). Act 1: 3 → 0 via spot-edit. Act 2: needed
  its act-only retry (mechanism worked). Act 3 retry: v4-flash truncated
  8/8 at 8000 tokens → RuntimeError crashed the run (pre-fix).
- **Attempt 2**: plan 26 failures, spot-edit discarded (not better).
  Act 1: 1 → 0 via spot-edit. Act 2 initial generation: truncated 8/8
  at 8000 → RuntimeError (the crash guard covered retries but not the
  initial act call; fixed afterwards, one run too late).

## Cost
~$0.02-0.03 across both attempts (no completed run; per-call pattern:
plan ~$0.005, each act gen ~$0.002-0.004 incl. reasoning waste).

## Evidence the mechanism works (when transport cooperates)
- Act 1 of attempt 2 gated at 1 problem and reached 0 after its single
  spot-edit — the per-act gate/edit loop closes at act scale.
- Act 2 of attempt 1 exercised the act-only retry exactly as designed
  (FATAL-class → regenerate just that act).

## Headwind (the real one)
v4-flash's reasoning token burn is UNBOUNDED and now routinely exceeds
8-12k on prose calls — truncation frequency has grown across sprints as
prompts grew. Per-act generation shrank the payload but not the
reasoning blowup probability (~1-in-3 calls at current prompt sizes).
Sprint-6 options, in order of preference:
1. Raise per-act cap to 16000 AND cap reasoning where the API allows
   (`reasoning: {effort: "low"}` on OpenRouter) — cheapest fix if the
   provider honors it.
2. Switch prose+edit to a non-reasoning model (benchmark: qwen3-235b
   was stable in sprint 1 at $0.09/$0.55 per Mtok; ~4x v4-flash cost
   but no truncation tax; minimax-m2.5 ignored all Thai machinery in the
   sprint-2 benchmark — but there is no Thai machinery anymore, so it
   is eligible for re-testing).
3. Drop the temperature for prose acts (0.8 → 0.6) to shorten reasoning.

## Tailwinds
- The architecture change is done and correct: per-act calls, carryover
  glue, per-act gates, act-scoped retries, transport-failure containment.
  What remains is a model/runtime parameter problem, not a design one.
- Plan stage remained stable and cheap throughout (5 calls, ~$0.005).
