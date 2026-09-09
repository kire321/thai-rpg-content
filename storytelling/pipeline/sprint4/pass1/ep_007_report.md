# Pipeline report — ep_007
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=28706, completion=41286
- cost estimate: $0.0150 (MODEL_PRICES in driver.py; update per model)
- final status: COMPLETED WITH GATE FAILURES (see report)
- tags picked by planner: tag_146, tag_113, tag_029, tag_252, tag_215, tag_065, tag_007, tag_303
- shortlist tags NOT used (for PO balancing): tag_121, tag_317, tag_329, tag_046

## Gate results
- plan (before spot-edit): FAIL (48 problem(s))
  - outline contains 1 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - refrain arc: need exactly 3 REFRAIN beats spread across at least 2 acts (found 2)
  - a PRESENT line stages the scene at 'The Mirror Mender', which is not in this episode's allowed places (['The Rice Ledger', 'The Salt Store', 'The School Veranda'])
  - act 1: char_rangsri is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_district_officer is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - no beat labeled 'SUBPLOT:' — one beat must show the facet of the foregrounded character's private plan this episode reveals or plants (as a concrete event, never stating the secret)
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_district_officer', 'char_salt_clerk']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: beat budget seg1 has 8 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: beat budget seg3 has 0 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 1 [medium] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 1 [hard] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 1 [hard] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 beat 14: char_grain_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 16: char_tax_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 18: char_grain_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 19: char_grain_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 19: char_mirror_mender speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 21: char_grain_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 24: char_grain_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: beat budget seg1 has 9 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2 [easy] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 [easy] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 [medium] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 [medium] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 [hard] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 [hard] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 3 beat 37: char_delivery_boy speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3 beat 38: char_delivery_boy speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3: beat budget seg1 has 9 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg2 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3 [easy] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 3 [easy] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 3 [medium] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 3 [medium] PASS outcome 'The Boy recalls a red cover and a brass clasp.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 3 [medium] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 3 [medium] FAIL outcome 'The Boy becomes confused and contradicts himself.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 3 [hard] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 3 [hard] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 4: beat budget seg1 has 8 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: beat budget seg2 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4 [easy] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 4 [easy] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 4 [medium] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 4 [medium] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 4 [hard] PASS outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 4 [hard] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
- plan (after spot-edit): FAIL (23 problem(s))
  - outline contains 1 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - refrain arc: the three occurrences must never be verbatim twice — each rewords the refrain's core words
  - act 1: missing 'PRESENT: ...' line naming who is on stage
  - act 1 beat 1: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 beat 9: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_district_officer', 'char_salt_clerk']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: beat budget seg1 has 9 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: beat budget seg3 has 1 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 1 [medium] choice references char_salt_clerk, who is not on stage and never entered
  - act 2: missing 'PRESENT: ...' line naming who is on stage
  - act 2 beat 16: char_grain_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 23: char_mirror_mender speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: beat budget seg1 has 11 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: missing 'PRESENT: ...' line naming who is on stage
  - act 3: beat budget seg1 has 9 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg2 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3 [easy] choice references char_salt_clerk, who is not on stage and never entered
  - act 4: missing 'PRESENT: ...' line naming who is on stage
  - act 4: beat budget seg1 has 8 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: beat budget seg2 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4 [easy] choice references char_salt_clerk, who is not on stage and never entered
- prose (before spot-edit): FAIL (10 problem(s))
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: The Delivery Boy runs up from the landing, out of breath, an' — the words belong to the speaking character's own line
  - act 1 segment 1: has 9 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 11 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 5 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
- prose (after spot-edit): FAIL (10 problem(s))
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: The Delivery Boy runs up from the landing, out of breath, an' — the words belong to the speaking character's own line
  - act 1 segment 1: has 9 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 11 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 5 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
- format: FAIL (14 problem(s))
  - act 1 segment 1: has 7 lines (expected 4-6) after mechanical merging
  - act 1 segment 5: has 1 lines (expected 2-3) after mechanical merging
  - act 2 segment 1: has 7 lines (expected 4-6) after mechanical merging
  - act 3 segment 3: has 5 lines (expected 2-3) after mechanical merging
  - act 3 segment 5: has 4 lines (expected 2-3) after mechanical merging
  - act 1 segment 1: has 7 lines (expected 4-6)
  - act 1 segment 5: has 1 lines (expected 2-3)
  - act 2 segment 1: has 7 lines (expected 4-6)
  - act 2 segment 1 line 2: third-person narration attributed to 'char_tax_clerk' (narration must be char_narrator)
  - act 2 segment 1 line 5: third-person narration attributed to 'char_grain_clerk' (narration must be char_narrator)
  - act 3 segment 3: has 5 lines (expected 2-3)
  - act 3 segment 3 line 1: narrator line carries quoted/narrated speech — speech belongs to the speaking character (actions go in stage_directions)
  - act 3 segment 5: has 4 lines (expected 2-3)
  - act 3 segment 5 line 3: third-person narration attributed to 'char_rangsri' (narration must be char_narrator)

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4869 out=1186
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2145 out=1302
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2106 out=2034
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=2989 out=2345
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=4361 out=2961
[plan] GATE FAILED (48 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (50 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=4654 out=8076
[plan] after spot-edit: 23 problem(s) remain — recorded, continuing
[prose] single generation call
[api] prose: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose: empty content or length-truncated (finish=length, attempt 2/8)
[api] prose: model=deepseek/deepseek-v4-flash tokens in=5458 out=11255
[prose] GATE FAILED (10 problem(s) — recorded, continuing without regeneration):
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: The Delivery Boy runs up from the landing, out of breath, an' — the words belong to the speaking character's own line
  - act 1 segment 1: has 9 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 11 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 5 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
[prose-spot-edit] one spot-edit pass (10 problem(s) to fix)
[api] prose-spot-edit: empty content or length-truncated (finish=None, attempt 1/8)
[api] prose-spot-edit: empty content or length-truncated (finish=length, attempt 2/8)
[api] prose-spot-edit: empty content or length-truncated (finish=length, attempt 3/8)
[api] prose-spot-edit: empty content or length-truncated (finish=length, attempt 4/8)
[api] prose-spot-edit: model=deepseek/deepseek-v4-flash tokens in=2124 out=12127
[prose] spot-edit DISCARDED (would leave 10 problems vs 10 before) — keeping the original, failures recorded
[format] GATE FAILED (14 problem(s) — recorded, episode kept as-is):
  - act 1 segment 1: has 7 lines (expected 4-6) after mechanical merging
  - act 1 segment 5: has 1 lines (expected 2-3) after mechanical merging
  - act 2 segment 1: has 7 lines (expected 4-6) after mechanical merging
  - act 3 segment 3: has 5 lines (expected 2-3) after mechanical merging
  - act 3 segment 5: has 4 lines (expected 2-3) after mechanical merging
  - act 1 segment 1: has 7 lines (expected 4-6)
  - act 1 segment 5: has 1 lines (expected 2-3)
  - act 2 segment 1: has 7 lines (expected 4-6)
  - act 2 segment 1 line 2: third-person narration attributed to 'char_tax_clerk' (narration must be char_narrator)
  - act 2 segment 1 line 5: third-person narration attributed to 'char_grain_clerk' (narration must be char_narrator)
  - act 3 segment 3: has 5 lines (expected 2-3)
  - act 3 segment 3 line 1: narrator line carries quoted/narrated speech — speech belongs to the speaking character (actions go in stage_directions)
  - act 3 segment 5: has 4 lines (expected 2-3)
  - act 3 segment 5 line 3: third-person narration attributed to 'char_rangsri' (narration must be char_narrator)
[out] wrote /mnt/agents/output/sprint4/pass1/ep_007.json
[out] wrote /mnt/agents/output/sprint4/pass1/ep_007.plan.md
[out] wrote /mnt/agents/output/sprint4/pass1/ep_007.prose.md
```
