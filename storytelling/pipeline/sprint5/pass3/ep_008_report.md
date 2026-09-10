# Pipeline report — ep_008
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=48190, completion=115066
- cost estimate: $0.0302 (MODEL_PRICES in driver.py; update per model)
- final status: FAILED (hard contract violation — see report)
- tags picked by planner: tag_045, tag_161, tag_209, tag_269, tag_131, tag_087, tag_278, tag_244
- shortlist tags NOT used (for PO balancing): tag_132, tag_081, tag_288, tag_279

## Gate results
- plan (before spot-edit): FAIL (17 problem(s))
  - technique vocabulary 'thesis' in the outline: ...'l posting. — carries: intro:Kamnan Noi, thesis\n\n7. The Pawnshop Appraiser asks i'... (the outline lists concrete events only — the writer must never see technique words)
  - wonder beats: need one WONDER beat per act (found acts [1, 2, 4])
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The River Post', 'The Salt Store', 'The School Veranda'])
  - act 1: char_mor_duang is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 2: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 beat 1: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_district_officer', 'char_mor_duang']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 3 beat 4: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3 beat 11: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3 beat 15: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 4: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
- plan (after spot-edit): FAIL (17 problem(s))
  - technique vocabulary 'thesis' in the outline: ...'l posting. — carries: intro:Kamnan Noi, thesis\n\n7. The Pawnshop Appraiser asks i'... (the outline lists concrete events only — the writer must never see technique words)
  - wonder beats: need one WONDER beat per act (found acts [1, 2, 4])
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The River Post', 'The Salt Store', 'The School Veranda'])
  - act 1: char_mor_duang is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 2: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 beat 1: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_district_officer', 'char_mor_duang']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 3 beat 4: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3 beat 11: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3 beat 15: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 3: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 4: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
- prose act 1 (before spot-edit): FAIL (4 problem(s))
  - act 1: PLACE 'place_veranda (The School Veranda)' is not one of the allowed places ['the river post', 'the salt store', 'the school veranda']
  - act 1: NARRATOR narrates speech ('X asks/says'): 'NARRATOR: The Pawnshop Appraiser asks if the salt is forfeit'
  - act 1 segment 1: has 9 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 5: has 0 prose lines (expected 2-3) — rebalance lines around the markers
- prose act 1 (after spot-edit): PASS
- prose act 2 (before spot-edit): FAIL (10 problem(s))
  - act 2: line has no 'Speaker:' prefix: '```'
  - act 2: junk stage direction [says] — physical content or empty
  - act 2: speaker prefix "The Boatman's son" maps to no character — use a nickname from the Names list or NARRATOR
  - act 2: junk stage direction [asks] — physical content or empty
  - act 2: line has no 'Speaker:' prefix: '```'
  - act 2: 14 prose lines (contract 8-12)
  - act 2 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2: marker [[tag_269]]'s preceding line lacks the English anchor word 'works' (prev: 'NARRATOR: Lek examines the notice; the District Officer’s si')
  - act 2: marker [[tag_209]]'s preceding line lacks the English anchor word 'stop' (prev: 'NARRATOR: Kamnan Noi takes out his brass compass and aligns ')
- prose act 2 (after spot-edit): FAIL (2 problem(s))
  - act 2: NARRATOR line contains quoted speech: 'NARRATOR: "Will we have to move the boat?"'
  - act 2: marker [[tag_209]]'s preceding line lacks the English anchor word 'stop' (prev: 'NARRATOR: Kamnan Noi takes out his brass compass and aligns ')
- prose act 3 (before spot-edit): FAIL (2 problem(s))
  - act 3 segment 1: has 3 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 6 prose lines (expected 2-3) — rebalance lines around the markers
- prose act 3 (after spot-edit): PASS
- prose act 4 (before spot-edit): FAIL (6 problem(s))
  - act 4: line has no 'Speaker:' prefix: '```'
  - act 4: NARRATOR line contains quoted speech: 'NARRATOR: The boatman opens the slip and sees a string of nu'
  - act 4: line has no 'Speaker:' prefix: '```'
  - act 4: 14 prose lines (contract 8-12)
  - act 4 segment 1: has 10 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
- prose act 4 (after spot-edit): FAIL (5 problem(s))
  - act 4: junk stage direction [says] — physical content or empty
  - act 4: junk stage direction [asks] — physical content or empty
  - act 4 segment 1: has 10 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
- prose act 4 (retry): FAIL (5 problem(s))
  - act 4: junk stage direction [says] — physical content or empty
  - act 4: junk stage direction [asks] — physical content or empty
  - act 4 segment 1: has 10 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
- prose (assembled, full-document checks): FAIL (7 problem(s))
  - junk stage direction [says] — it merely restates the speech act; give it physical content or drop the brackets
  - junk stage direction [asks] — it merely restates the speech act; give it physical content or drop the brackets
  - NARRATOR line contains quoted speech: 'NARRATOR: "Will we have to move the boat?"' — give the speech to the speaking character as '<Nickname>: [action] "words"'
  - act 4 segment 1: has 10 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - marker [[tag_209]]: the line immediately before it does not use the English anchor word 'stop' (prev line: 'NARRATOR: Kamnan Noi takes out his brass compass and aligns it silentl')
- format: FAIL (3 problem(s))
  - FATAL: act 4 segment 1: has 10 lines (contract 4-6) — FATAL; the prose spot-edit is the only repair path
  - FATAL: act 4 segment 3: has 1 lines (contract 2-3) — FATAL; the prose spot-edit is the only repair path
  - FATAL: act 4 segment 5: has 1 lines (contract 2-3) — FATAL; the prose spot-edit is the only repair path

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4787 out=1254 reasoning=0
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2225 out=1396 reasoning=0
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2278 out=2305 reasoning=0
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=4095 out=2563 reasoning=0
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=4610 out=2920 reasoning=0
[plan] GATE FAILED (17 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (19 problem(s) to fix)
[api] plan-spot-edit: empty content or length-truncated (finish=length, attempt 1/8)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=3768 out=14486 reasoning=11069
[plan] spot-edit DISCARDED (would leave 35 problems vs 17 before) — keeping the original, failures recorded
[prose-act1] single generation call
[api] prose-act1: model=deepseek/deepseek-v4-flash tokens in=4735 out=7148 reasoning=6733
[prose-act1] GATE FAILED (4 problem(s) — recorded, continuing without regeneration):
  - act 1: PLACE 'place_veranda (The School Veranda)' is not one of the allowed places ['the river post', 'the salt store', 'the school veranda']
  - act 1: NARRATOR narrates speech ('X asks/says'): 'NARRATOR: The Pawnshop Appraiser asks if the salt is forfeit'
  - act 1 segment 1: has 9 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 5: has 0 prose lines (expected 2-3) — rebalance lines around the markers
[prose-act1-spot-edit] one spot-edit pass (4 problem(s) to fix)
[api] prose-act1-spot-edit: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose-act1-spot-edit: model=deepseek/deepseek-v4-flash tokens in=601 out=12075 reasoning=11665
[prose-act1] done: 0 problem(s)
[prose-act2] single generation call
[api] prose-act2: model=deepseek/deepseek-v4-flash tokens in=4785 out=12883 reasoning=12594
[prose-act2] GATE FAILED (10 problem(s) — recorded, continuing without regeneration):
  - act 2: line has no 'Speaker:' prefix: '```'
  - act 2: junk stage direction [says] — physical content or empty
  - act 2: speaker prefix "The Boatman's son" maps to no character — use a nickname from the Names list or NARRATOR
  - act 2: junk stage direction [asks] — physical content or empty
  - act 2: line has no 'Speaker:' prefix: '```'
  - act 2: 14 prose lines (contract 8-12)
  - act 2 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2: marker [[tag_269]]'s preceding line lacks the English anchor word 'works' (prev: 'NARRATOR: Lek examines the notice; the District Officer’s si')
  - act 2: marker [[tag_209]]'s preceding line lacks the English anchor word 'stop' (prev: 'NARRATOR: Kamnan Noi takes out his brass compass and aligns ')
[prose-act2-spot-edit] one spot-edit pass (10 problem(s) to fix)
[api] prose-act2-spot-edit: model=deepseek/deepseek-v4-flash tokens in=599 out=7467 reasoning=7186
[prose-act2] done: 2 problem(s)
[prose-act3] single generation call
[api] prose-act3: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose-act3: model=deepseek/deepseek-v4-flash tokens in=4773 out=6783 reasoning=6480
[prose-act3] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 3 segment 1: has 3 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 6 prose lines (expected 2-3) — rebalance lines around the markers
[prose-act3-spot-edit] one spot-edit pass (2 problem(s) to fix)
[api] prose-act3-spot-edit: empty content or length-truncated (finish=None, attempt 1/8)
[api] prose-act3-spot-edit: model=deepseek/deepseek-v4-flash tokens in=412 out=13473 reasoning=13170
[prose-act3] done: 0 problem(s)
[prose-act4] single generation call
[api] prose-act4: model=deepseek/deepseek-v4-flash tokens in=4772 out=8468 reasoning=7769
[prose-act4] GATE FAILED (6 problem(s) — recorded, continuing without regeneration):
  - act 4: line has no 'Speaker:' prefix: '```'
  - act 4: NARRATOR line contains quoted speech: 'NARRATOR: The boatman opens the slip and sees a string of nu'
  - act 4: line has no 'Speaker:' prefix: '```'
  - act 4: 14 prose lines (contract 8-12)
  - act 4 segment 1: has 10 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
[prose-act4-spot-edit] one spot-edit pass (6 problem(s) to fix)
[api] prose-act4-spot-edit: model=deepseek/deepseek-v4-flash tokens in=496 out=5217 reasoning=4908
[prose-act4] FATAL-class failures remain — ONE act-only retry
[prose-act4-retry] single generation call
[api] prose-act4-retry: model=deepseek/deepseek-v4-flash tokens in=4772 out=7139 reasoning=6829
[prose-act4-retry] GATE FAILED (5 problem(s) — recorded, continuing without regeneration):
  - act 4: junk stage direction [says] — physical content or empty
  - act 4: junk stage direction [asks] — physical content or empty
  - act 4 segment 1: has 10 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
[prose-act4-spot-edit] one spot-edit pass (5 problem(s) to fix)
[api] prose-act4-spot-edit: model=deepseek/deepseek-v4-flash tokens in=482 out=9489 reasoning=9183
[prose-act4] done: 5 problem(s)
[format] FATAL (3 unmappable item(s)) — no episode written:
  - act 4 segment 1: has 10 lines (contract 4-6) — FATAL; the prose spot-edit is the only repair path
  - act 4 segment 3: has 1 lines (contract 2-3) — FATAL; the prose spot-edit is the only repair path
  - act 4 segment 5: has 1 lines (contract 2-3) — FATAL; the prose spot-edit is the only repair path
```
