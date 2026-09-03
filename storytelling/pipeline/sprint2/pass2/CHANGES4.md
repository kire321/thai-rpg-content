# Sprint 2, Pass 2 — CHANGES4 (fixes mapped to the 8 priority items)

Files changed (branch `sprint1-pipeline`): `driver.py`, `prompts/plan.md`,
`prompts/prose.md`. Outputs: `ep_005.json`, `ep_005.plan.md`,
`ep_005.prose.md`, `ep_005_report.md` in this folder.

## Fix map

### 1. Segment structure as hard contract
- `format_episode()`: any EMPTY segment or segment-1 >6 lines is now FATAL
  (recorded, no JSON, exit 1). Verified against pass-1 prose: 8 fatals
  (4 empty seg-5s, 4 seg-1 blowouts) — would have blocked ep_004.
- Cause attacked: plan step 4 now carries an explicit LINE BUDGET (tag-1
  pair within lines 1–6, tag-2 pair within lines 7–9, 2–3 beats for lines
  10–12); prose.md states the same budget as a hard contract and forbids
  late markers; the prose gate's count check (added post-pass-1) feeds the
  prose spot-edit, which repaired 7 count violations → PASS this run.
- Result: ep_005 segments [6,2,2] [6,3,3] [6,3,2] [4,3,3] — all in contract
  (pass 1: 12/15/20/14-line seg-1s and empty seg-5s in every act).

### 2. Stakes with teeth
- Plan gate: STAKES beat must exist in act 1 (first 6 beats) AND contain an
  or/otherwise/if-not/unless clause naming the concrete cost. Missing or
  cost-less STAKES after the plan spot-edit is FATAL (pipeline aborts,
  recorded) — position issues remain non-fatal errors (refined after one
  over-broad abort).
- Result: ep_005 plan has a costed STAKES beat ("Identify the owner or I
  stamp it for sale in seven days.").

### 3. PC holds the thread
- Plan gate: char_pricha must have an action/dialogue beat in every act
  (decision outcomes don't count); plan.md instructs the foregrounded NPC
  may not solve the central problem single-handedly.

### 4. Thai dramatic pretext + reaction, not gloss
- Plan step 4: each TAG beat-pair is now (a) `TAG tag_xxx:` beat = the
  dramatic pretext — WHO says the phrase, to whom, in what situation
  (plan-gated: a TAG beat naming no character fails); (b) second beat = a
  dramatic REACTION that moves the scene and carries the English anchor
  word — explanations of the Thai line's meaning ("showing X"/"ignoring Y")
  are banned in both plan-step instruction and prose.md STEP 3.

### 5. decision.line freshness
- prose.md: the DECISION beat is not expanded at all (no dilemma line in
  prose); formatter check: decision.line verbatim-equal to any narrative
  line in its act is a format-gate error; validate_episode's duplicate scan
  now includes decision lines.
- Result: ep_005 has zero decision.line duplications (pass 1: 4/4 acts).

### 6. Introductions
- Plan gate: every character in act 1's PRESENT line (PC and foregrounded
  character included) needs an ENTRANCE beat within the first 6 beats;
  act-1 segment-1 speaker budget is now strictly the first 6 beats
  (narrator + PC + one other). Plan step 2 instructs accordingly.

### 7. Urgency / deadline convergence
- Plan gate: if acts 1–2 plant a deadline (noon/dawn/deadline/tomorrow/
  days-hence/mail-boat/...), act 3 must contain a beat where it converges.
  Plan step 2 instructs the convergence beat.

### 8. Subplot plant
- plan.md STEP 1: the beat where the foregrounded character's private-plan
  facet becomes visible is labeled `SUBPLOT:` (concrete event, never the
  secret); plan gate requires exactly such a labeled beat.

## Additional fixes made during pass 2 (from observed failures)
- **Keep-better guard on spot-edits** (both stages): if the edited artifact
  re-gates WORSE than the original, the edit is discarded and the original
  kept. Pass-2 attempt 1 died because the plan spot-edit truncated the
  outline to 2 acts and the cascade destroyed the episode; the guard makes
  spot-editing strictly-safe.
- **Outcome-voice plan gate**: PASS/FAIL outcome texts must begin with "I "
  — pass-2 attempt 3 shipped 21/21 format errors of this single class
  because the rule lived only in the format gate (too late to fix). Moved
  to the plan gate where the spot-edit can repair it. Final run: 1 residual.

## Pass-2 run (ep_005, char_phra_kam) — gate results
- plan: 7 → 4 (spot-edit; residuals: 1 comparison, entrance/order slips)
- prose: 7 → **PASS** (all 7 were marker-position/count issues, repaired)
- format: FAIL (1) — one fail_outcome not beginning with "I "
- Status: COMPLETED WITH GATE FAILURES. All 4 acts in segment contract,
  8/8 tags placed, all decisions present, Thai present in all slots.

## Cost
- Final run: $0.0138 (23,185 in / 41,754 out — v4-flash's reasoning-heavy
  spot-edits dominate output tokens). Two aborted attempts during fix
  development: ~$0.025. Plan stage alone remains ≈ $0.005.

## Defect comparison vs pass 1 (editor's defect list)
| pass-1 defect | ep_005 |
|---|---|
| 1. Empty seg-5 ×4, seg-1 12–20 lines | **FIXED** — all segments in contract; hard FATAL backstop |
| 2. Thai orphan non-sequiturs ≥4/8 | pretext mechanism in place (TAG beats name speaker+situation); dramatic quality is the editor's call |
| 3. PC bystander, ~4 lines | PC-per-act gate; Lek acts in every act of the plan |
| 4. Stakes absent | **FIXED** — costed STAKES beat, FATAL backstop |
| 5. decision.line duplicates ×4 | **FIXED** — 0 duplications |
| 6. Gloss-tells at tag slots | reaction-not-gloss instruction at plan+prose level; no mechanical detector (judgment call) |
| 7. Foreground char unintroduced, 5 speakers seg-1 | ENTRANCE-for-PRESENT gate + strict 6-beat budget |
| 8. Deadline planted, never used | convergence gate (deadline regex acts 1-2 → act 3) |
| 9. Minor (not-X-but-Y, ladders, PC lies) | not addressed this pass |

## Headwinds
- v4-flash spot-edits are the cost center (reasoning tokens: 41k output
  tokens this run) and occasionally destructive — the keep-better guard is
  now load-bearing. A cheaper/less-reasoning editor model would cut episode
  cost ~40%.
- The outcome-voice class needed three attempts to converge (gate added
  only after seeing attempt 3's output) — new rules should land in the
  PLAN gate by default, not the format gate; format is too late to fix.
- No mechanical detector for gloss-tells or Thai pretext quality — these
  remain instruction-level; if the editor still flags them, candidates are
  a banned-verb list in reaction beats ("showing/ignoring/meaning") or a
  reaction-beat-must-contain-a-verb-of-motion heuristic.

## Tailwinds
- First run with prose gate PASS after spot-edit AND all segments in
  contract AND zero decision duplications AND costed stakes — the
  gate-with-authority pattern (detect → one edit → re-gate → keep-better →
  hard-fatal on contracts) keeps converting editor defects into one-line
  mechanical checks.
