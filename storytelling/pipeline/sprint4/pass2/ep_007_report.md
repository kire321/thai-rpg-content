# Pipeline report — ep_007
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=21270, completion=13587
- cost estimate: $0.0096 (MODEL_PRICES in driver.py; update per model)
- final status: FAILED (hard contract violation — see report)
- tags picked by planner: tag_121, tag_113, tag_146, tag_215, tag_252, tag_046, tag_065, tag_303
- shortlist tags NOT used (for PO balancing): tag_317, tag_329, tag_029, tag_007

## Gate results
- plan (before spot-edit): FAIL (34 problem(s))
  - outline contains 2 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - refrain arc: need exactly 3 REFRAIN beats spread across at least 2 acts (found 2)
  - act 1: no DECISION beat (every act needs exactly one, ending the act)
  - act 1: char_monk is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 2: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 4: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 5: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1: no beat labeled 'STAKES:' (one early beat must be a character stating aloud what they want and what it costs)
  - no beat labeled 'SUBPLOT:' — one beat must show the facet of the foregrounded character's private plan this episode reveals or plants (as a concrete event, never stating the secret)
  - act 1 beat 3: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 beat 4: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 beat 6: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 beat 8: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 beat 10: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_district_officer', 'char_monk']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: beat budget seg2 has 7 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 2: no DECISION beat (every act needs exactly one, ending the act)
  - act 2 beat 8: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 9: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: beat budget seg1 has 8 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2: beat budget seg2 has 7 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 2: beat budget seg3 has 0 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: no DECISION beat (every act needs exactly one, ending the act)
  - act 3 beat 10: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 3 beat 12: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3: beat budget seg1 has 11 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg2 has 7 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 0 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4: no DECISION beat (every act needs exactly one, ending the act)
  - act 4 beat 11: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 4: beat budget seg1 has 12 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: beat budget seg3 has 1 beats (need 2-3) — place each TAG pair so segment line counts land
- plan (after spot-edit): FAIL (27 problem(s))
  - outline contains 2 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - refrain arc: need exactly 3 REFRAIN beats spread across at least 2 acts (found 2)
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1: STAKES beat names no concrete cost — it must say what happens if the characters fail ("X, or Y happens")
  - act 1 beat 5: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_district_officer', 'char_monk']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: beat budget seg1 has 7 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: beat budget seg2 has 7 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 1: DECISION beat does not name the dilemma speaker — expected 'DECISION — dilemma line (<nickname>): "..."'
  - act 1: DECISION beat must have exactly 3 options [easy]/[medium]/[hard], each with an (attr_...) — found 0 options, 0 attributes
  - act 2: beat budget seg1 has 8 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2: beat budget seg2 has 7 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 2: beat budget seg3 has 0 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 2: DECISION beat does not name the dilemma speaker — expected 'DECISION — dilemma line (<nickname>): "..."'
  - act 2: DECISION beat must have exactly 3 options [easy]/[medium]/[hard], each with an (attr_...) — found 0 options, 0 attributes
  - act 3 beat 10: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 3: beat budget seg1 has 11 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg2 has 7 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 0 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: DECISION beat does not name the dilemma speaker — expected 'DECISION — dilemma line (<nickname>): "..."'
  - act 3: DECISION beat must have exactly 3 options [easy]/[medium]/[hard], each with an (attr_...) — found 0 options, 0 attributes
  - act 4: beat budget seg1 has 12 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: beat budget seg3 has 1 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4: DECISION beat does not name the dilemma speaker — expected 'DECISION — dilemma line (<nickname>): "..."'
  - act 4: DECISION beat must have exactly 3 options [easy]/[medium]/[hard], each with an (attr_...) — found 0 options, 0 attributes
- plan FATAL: FAIL (1 problem(s))
  - act 1: STAKES beat names no concrete cost — it must say what happens if the characters fail ("X, or Y happens")
- prose: FAIL (1 problem(s))
  - skipped: plan FATAL (no costed STAKES beat)
- format: FAIL (1 problem(s))
  - skipped: plan FATAL (no costed STAKES beat)

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4869 out=1297
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2256 out=1352
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2215 out=2182
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=3137 out=2468
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=4484 out=3011
[plan] GATE FAILED (34 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (36 problem(s) to fix)
[api] plan-spot-edit: empty content or length-truncated (finish=length, attempt 1/8)
[api] plan-spot-edit: empty content or length-truncated (finish=None, attempt 2/8)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=4309 out=3277
[plan] after spot-edit: 27 problem(s) remain — recorded, continuing
[plan] FATAL: no costed STAKES beat after spot-edit — aborting episode
```
