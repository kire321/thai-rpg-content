# Pipeline report — ep_004
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=21959, completion=19094
- cost estimate: $0.0091 (MODEL_PRICES in driver.py; update per model)
- final status: COMPLETED WITH GATE FAILURES (see report)

## Gate results
- plan (before spot-edit): FAIL (10 problem(s))
  - plan: full name 'Pricha' used for char_pricha — use the nickname 'Lek' (...'cha: call them "Lek" — NEVER "Pricha".\n- char_rain_gauge_keeper: c'...)
  - plan: full name 'Sangwan' used for char_sangwan — use the nickname 'Wan' (...'wan: call them "Wan" — NEVER "Sangwan".\n- char_tax_clerk: call them'...)
  - plan: full name 'Pornchai' used for char_pornchai — use the nickname 'Pom' (...'hai: call them "Pom" — NEVER "Pornchai".\n- char_pricha: call them "L'...)
  - outline uses place 'The Pawnshop', which is not in this episode's allowed places (['The Ash Urn', "The Letter-Writer's Landing", 'The School Veranda'])
  - outline uses place 'The Mirror Mender', which is not in this episode's allowed places (['The Ash Urn', "The Letter-Writer's Landing", 'The School Veranda'])
  - act 1: no beat labeled 'STAKES:' (one early beat must be a character stating aloud what they want and what it costs)
  - act 1 [medium] PASS outcome 'I see a faint registry number surface on the wet g' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 2 beat 5: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 9: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 12: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
- plan (after spot-edit): FAIL (5 problem(s))
  - plan: full name 'Pricha' used for char_pricha — use the nickname 'Lek' (...'cha: call them "Lek" — NEVER "Pricha".\n- char_rain_gauge_keeper: c'...)
  - plan: full name 'Sangwan' used for char_sangwan — use the nickname 'Wan' (...'wan: call them "Wan" — NEVER "Sangwan".\n- char_tax_clerk: call them'...)
  - plan: full name 'Pornchai' used for char_pornchai — use the nickname 'Pom' (...'hai: call them "Pom" — NEVER "Pornchai".\n- char_pricha: call them "L'...)
  - outline uses place 'The Pawnshop', which is not in this episode's allowed places (['The Ash Urn', "The Letter-Writer's Landing", 'The School Veranda'])
  - outline uses place 'The Mirror Mender', which is not in this episode's allowed places (['The Ash Urn', "The Letter-Writer's Landing", 'The School Veranda'])
- prose (before spot-edit): FAIL (2 problem(s))
  - marker [[tag_020]]: the line immediately before it does not use the English anchor word 'call' (prev line: 'NARRATOR: Lek calls to him, but receives no answer.')
  - marker [[tag_339]]: the line immediately before it does not use the English anchor word 'use' (prev line: 'NARRATOR: Phum does not reach for it, ignoring that it can still be us')
- prose (after spot-edit): PASS
- format: FAIL (27 problem(s))
  - act 1 segment 1: has 12 lines (expected 4-6)
  - act 1 segment 3: has 7 lines (expected 2-3)
  - act 1 segment 5: has 0 lines (expected 2-3)
  - act 2 segment 1: has 15 lines (expected 4-6)
  - act 2 segment 3: has 4 lines (expected 2-3)
  - act 2 segment 5: has 0 lines (expected 2-3)
  - act 3 segment 1: has 20 lines (expected 4-6)
  - act 3 segment 3: has 4 lines (expected 2-3)
  - act 3 segment 5: has 0 lines (expected 2-3)
  - act 4 segment 1: has 14 lines (expected 4-6)
  - act 4 segment 3: has 4 lines (expected 2-3)
  - act 4 segment 5: has 0 lines (expected 2-3)
  - act 1 segment 1: has 12 lines (expected 4-6)
  - act 1 segment 3: has 7 lines (expected 2-3)
  - act 1 segment 5: has 0 lines (expected 2-3)
  - act 2 segment 1: has 15 lines (expected 4-6)
  - act 2 segment 1 line 5: third-person narration attributed to 'char_phum' (narration must be char_narrator)
  - act 2 segment 3: has 4 lines (expected 2-3)
  - act 2 segment 3 line 1: line voiced by char_district_officer mentions 'The District Officer' in third person — this is narration; reassign to char_narrator
  - act 2 segment 5: has 0 lines (expected 2-3)
  - act 2 decision.line: line voiced by char_district_officer mentions 'The District Officer' in third person — this is narration; reassign to char_narrator
  - act 3 segment 1: has 20 lines (expected 4-6)
  - act 3 segment 3: has 4 lines (expected 2-3)
  - act 3 segment 5: has 0 lines (expected 2-3)
  - act 4 segment 1: has 14 lines (expected 4-6)
  - act 4 segment 3: has 4 lines (expected 2-3)
  - act 4 segment 5: has 0 lines (expected 2-3)

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=5080 out=924
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=1694 out=997
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=1802 out=2370
[plan-4-tags] single generation call
[api] plan-4-tags: model=deepseek/deepseek-v3.2 tokens in=3432 out=3039
[plan] GATE FAILED (10 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (10 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=3527 out=7363
[plan] after spot-edit: 5 problem(s) remain — recorded, continuing
[prose] single generation call
[api] prose: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose: empty content or length-truncated (finish=length, attempt 2/8)
[api] prose: empty content or length-truncated (finish=length, attempt 3/8)
[api] prose: model=deepseek/deepseek-v4-flash tokens in=4910 out=1371
[prose] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - marker [[tag_020]]: the line immediately before it does not use the English anchor word 'call' (prev line: 'NARRATOR: Lek calls to him, but receives no answer.')
  - marker [[tag_339]]: the line immediately before it does not use the English anchor word 'use' (prev line: 'NARRATOR: Phum does not reach for it, ignoring that it can still be us')
[prose-spot-edit] one spot-edit pass (2 problem(s) to fix)
[api] prose-spot-edit: model=deepseek/deepseek-v4-flash tokens in=1514 out=3030
[prose] after spot-edit: 0 problem(s) remain — recorded, continuing
[format] GATE FAILED (27 problem(s) — recorded, episode kept as-is):
  - act 1 segment 1: has 12 lines (expected 4-6)
  - act 1 segment 3: has 7 lines (expected 2-3)
  - act 1 segment 5: has 0 lines (expected 2-3)
  - act 2 segment 1: has 15 lines (expected 4-6)
  - act 2 segment 3: has 4 lines (expected 2-3)
  - act 2 segment 5: has 0 lines (expected 2-3)
  - act 3 segment 1: has 20 lines (expected 4-6)
  - act 3 segment 3: has 4 lines (expected 2-3)
  - act 3 segment 5: has 0 lines (expected 2-3)
  - act 4 segment 1: has 14 lines (expected 4-6)
  - act 4 segment 3: has 4 lines (expected 2-3)
  - act 4 segment 5: has 0 lines (expected 2-3)
  - act 1 segment 1: has 12 lines (expected 4-6)
  - act 1 segment 3: has 7 lines (expected 2-3)
  - act 1 segment 5: has 0 lines (expected 2-3)
  - act 2 segment 1: has 15 lines (expected 4-6)
  - act 2 segment 1 line 5: third-person narration attributed to 'char_phum' (narration must be char_narrator)
  - act 2 segment 3: has 4 lines (expected 2-3)
  - act 2 segment 3 line 1: line voiced by char_district_officer mentions 'The District Officer' in third person — this is narration; reassign to char_narrator
  - act 2 segment 5: has 0 lines (expected 2-3)
  - act 2 decision.line: line voiced by char_district_officer mentions 'The District Officer' in third person — this is narration; reassign to char_narrator
  - act 3 segment 1: has 20 lines (expected 4-6)
  - act 3 segment 3: has 4 lines (expected 2-3)
  - act 3 segment 5: has 0 lines (expected 2-3)
  - act 4 segment 1: has 14 lines (expected 4-6)
  - act 4 segment 3: has 4 lines (expected 2-3)
  - act 4 segment 5: has 0 lines (expected 2-3)
[out] wrote /mnt/agents/output/sprint2/pass1/ep_004.json
[out] wrote /mnt/agents/output/sprint2/pass1/ep_004.plan.md
[out] wrote /mnt/agents/output/sprint2/pass1/ep_004.prose.md
```
