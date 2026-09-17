# Sprint 8 — ep_009 SHIPPED (zero FATALs)

## Features
- C (script elicitation): plan beats are speaker-attributed script cues; prose prompt reframed
  "continue this script"; narrator omitted from character beats. Narrator-subject gate = FATAL
  (detection-only; possessive/PP-embedded exempt). Golden replay on ep_008: 18 hits (would have
  aborted — as designed).
- A (motivation inventories): plan lint — WONDER (inventory) needs >=3 concrete items + explicit
  "shows X" clause. ep_009's inventories pass; OR-judge scored motivation-inventory 4/5.
- Infra: line-level repair (regenerate one line, can't break neighbors) wired into segment loop;
  OR-judge scaffold (judge.py, v3.2, scores motivation/flow/anchors — editor adjudicates).

## Lever verdicts
- deepseek-v3.2 for PROSE+EDIT: decisive. v4-flash truncation loops vanished; retries converge
  to 0 problems in one pass. qwen failed the contract (11-line segment, 6/8 markers lost).
- Empty-retry/empty-edit guards: fired and prevented empty-artifact terminal aborts.
- Offline formatter rerun + deterministic prose surgery: shipped without a full rerun.

## What fired (ep_009 run s8f + offline repair)
- Plan: 37 problems -> spot-edit -> clean; STAKES present.
- Prose: a1-segment3 retry -> 0; all other segments <=1 problem.
- Coverage FATAL: 4 choices referenced unestablished objects -> deterministic choice rewrite
  against prose vocabulary -> 0 orphans.
- Deterministic prose repairs: 2 narrator-quoted-speech, 1 narrator-subject, 1 second-person,
  PLACE/header drift, marker redistribution (tag_008 act2->act3), 2 heuristic-tripping sentences
  rephrased (present tense / plain speech).
- Final: segments [5,2,3][6,3,3][4,2,2][4,2,3], 8/8 tags, 4/4 decisions, zero Thai, zero artifacts.
- Remaining non-fatal: 6 anchor-word misses (judge: anchor-semantics 2/5 — sprint-9 item),
  4 title-sanitize notices (titles derived from refrain).

## Cost (OR $)
~$0.14 total sprint 8 (5 full/partial runs ~$0.10 + offline repairs/judge ~$0.04).
