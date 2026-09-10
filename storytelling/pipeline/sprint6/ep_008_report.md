# Pipeline report — ep_008
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=52286, completion=85958
- cost estimate: $0.0258 (MODEL_PRICES in driver.py; update per model)
- final status: FAILED (hard contract violation — see report)
- tags picked by planner: tag_045, tag_131, tag_161, tag_209, tag_269, tag_288, tag_278, tag_081
- shortlist tags NOT used (for PO balancing): tag_132, tag_244, tag_087, tag_279

## Gate results
- plan (before spot-edit): FAIL (14 problem(s))
  - technique vocabulary 'symbol' in the outline: ...' traces a line to a column of red-inked symbols.\n8. The monk leans in, squints a'... (the outline lists concrete events only — the writer must never see technique words)
  - wonder beats: need one WONDER beat per act (found acts [1, 3, 4])
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The River Post', 'The Salt Store', 'The School Veranda'])
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_mor_duang is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_monk', 'char_mor_duang']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2 beat 14: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2 [medium] FAIL outcome 'I see her crumple it tighter and turn away.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 3: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 3 [easy] FAIL outcome 'I see him laugh and say the fee just doubled.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 4: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
- plan (after spot-edit): FAIL (14 problem(s))
  - technique vocabulary 'symbol' in the outline: ...' traces a line to a column of red-inked symbols.\n8. The monk leans in, squints a'... (the outline lists concrete events only — the writer must never see technique words)
  - wonder beats: need one WONDER beat per act (found acts [1, 3, 4])
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The River Post', 'The Salt Store', 'The School Veranda'])
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_mor_duang is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_monk', 'char_mor_duang']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2 beat 14: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2 [medium] FAIL outcome 'I see her crumple it tighter and turn away.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 3: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 3 [easy] FAIL outcome 'I see him laugh and say the fee just doubled.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 4: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
- prose-a1-segment1 (before spot-edit): FAIL (2 problem(s))
  - act 1 segment 1: missing '## Act 1 —' header line
  - act 1 segment 1: no 'PLACE:' line
- prose-a1-segment1 (after spot-edit): FAIL (1 problem(s))
  - act 1 segment 1: PLACE 'Temple veranda' is not one of the allowed places ['river post', 'salt store', 'school veranda']
- prose-a1-segment1 (retry): FAIL (1 problem(s))
  - act 1 segment 1: NARRATOR narrates speech: 'NARRATOR: The boatman stands on the temple veranda holding a'
- prose-a1-segment3 (before spot-edit): FAIL (1 problem(s))
  - act 1 segment 3: technique vocabulary 'symbol'
- prose-a1-segment3 (after spot-edit): PASS
- prose-a1-segment5 (before spot-edit): FAIL (3 problem(s))
  - act 1 segment 5: markdown asterisk in prose
  - act 1 segment 5: NARRATOR narrates speech: 'NARRATOR: Lek asks to see the ledger entry; Kamnan Noi slide'
  - act 1 segment 5: technique vocabulary 'symbol'
- prose-a1-segment5 (after spot-edit): PASS
- prose-a2-segment1 (before spot-edit): FAIL (4 problem(s))
  - act 2 segment 1: missing '## Act 2 —' header line
  - act 2 segment 1: no 'PLACE:' line
  - act 2 segment 1: NARRATOR narrates speech: 'NARRATOR: The boatman asks what they are supposed to do now;'
  - act 2 segment 1: speaker prefix "The Boatman's Wife" maps to no character
- prose-a2-segment1 (after spot-edit): FAIL (1 problem(s))
  - act 2 segment 1: speaker prefix "Boatman's Wife" maps to no character
- prose-a2-segment1 (retry): FAIL (1 problem(s))
  - act 2 segment 1: speaker prefix "Boatman's Wife" maps to no character
- prose-a2-segment3 (before spot-edit): FAIL (1 problem(s))
  - act 2 segment 3: speaker prefix "Boatman's Wife" maps to no character
- prose-a2-segment3 (after spot-edit): PASS
- prose-a2-segment5 (before spot-edit): PASS
- prose-a3-segment1 (before spot-edit): FAIL (2 problem(s))
  - act 3 segment 1: missing '## Act 3 —' header line
  - act 3 segment 1: no 'PLACE:' line
- prose-a3-segment1 (after spot-edit): PASS
- prose-a3-segment3 (before spot-edit): PASS
- prose-a3-segment5 (before spot-edit): FAIL (1 problem(s))
  - act 3 segment 5: NARRATOR narrates speech: 'NARRATOR: The light through the salt bins casts three distin'
- prose-a3-segment5 (after spot-edit): FAIL (1 problem(s))
  - act 3 segment 5: NARRATOR narrates speech: 'NARRATOR: The light through the salt bins casts three distin'
- prose-a4-segment1 (before spot-edit): FAIL (2 problem(s))
  - act 4 segment 1: missing '## Act 4 —' header line
  - act 4 segment 1: no 'PLACE:' line
- prose-a4-segment1 (after spot-edit): FAIL (1 problem(s))
  - act 4 segment 1: PLACE 'Temple veranda' is not one of the allowed places ['river post', 'salt store', 'school veranda']
- prose-a4-segment1 (retry): FAIL (1 problem(s))
  - act 4 segment 1: missing '## Act 4 —' header line
- prose-a4-segment3 (before spot-edit): PASS
- prose-a4-segment5 (before spot-edit): PASS
- prose (assembled, full-document checks): FAIL (10 problem(s))
  - speaker prefix "Boatman's Wife" maps to no character ('Boatman\'s Wife: [pleads] "Please, Kamnan Noi." [[tag_161]]') — rename it to a nickname from the Names list, or make the line NARRATOR:
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: The boatman stands on the temple veranda holding a sleeping ' — the words belong to the speaking character's own line
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: The light through the salt bins casts three distinct moving ' — the words belong to the speaking character's own line
  - act 2: PLACE 'River post' is not one of the allowed places ['the river post', 'the salt store', 'the school veranda'] — restage the act at an allowed place
  - prose: NARRATOR line uses second person: "NARRATOR: The boatman's wife does not unfold the coded paper; she hold"
  - prose: line under 'Boatman' has neither quoted speech nor a [stage direction] — narration must sit under NARRATOR: 'Boatman: What are we supposed to do now? NARRATOR: Lek suggests regist'
  - prose: near-duplicate lines share the run 'the name already cut into the': 'The Boatman: "The name is already cut into the woo' / 'The Boatman: [shakes his head] "The name is alread'
  - prose: near-duplicate lines share the run 'the boatmans wife does not unfold': "NARRATOR: The boatman's wife does not unfold the c" / "NARRATOR: The boatman's wife does not unfold the c"
  - act 1 choice 'I demand Kamnan Noi show us the red-inked column and explain': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 3 choice 'I challenge Kamnan Noi to show the two charts he drew and ex': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
- format: FAIL (6 problem(s))
  - FATAL: act 2: speaker "Boatman's Wife" does not map to any character id
  - FATAL: act 2: found 1 tag markers (need exactly 2)
  - act 2: act title is a PLACE line — header malformed; title sanitized
  - act 3: act title is a PLACE line — header malformed; title sanitized
  - act 4: act title is a PLACE line — header malformed; title sanitized
  - tags used ['tag_045', 'tag_081', 'tag_131', 'tag_269', 'tag_278', 'tag_288'] != assigned set ['tag_045', 'tag_081', 'tag_131', 'tag_161', 'tag_209', 'tag_269', 'tag_278', 'tag_288']

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4787 out=1170 reasoning=0
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2142 out=1340 reasoning=0
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2222 out=2658 reasoning=0
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=4449 out=2971 reasoning=0
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=5019 out=3326 reasoning=0
[plan] GATE FAILED (14 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (16 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=4075 out=18125 reasoning=14608
[plan] spot-edit DISCARDED (disqualified (machinery stripped / FATAL class grew)) — keeping the original, failures recorded
[prose-a1-segment1] single generation call
[api] prose-a1-segment1: model=deepseek/deepseek-v4-flash tokens in=2038 out=7738 reasoning=7568
[prose-a1-segment1] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 1: missing '## Act 1 —' header line
  - act 1 segment 1: no 'PLACE:' line
[prose-a1-segment1-spot-edit] one spot-edit pass (2 problem(s) to fix)
[api] prose-a1-segment1-spot-edit: model=deepseek/deepseek-v4-flash tokens in=255 out=788 reasoning=608
[prose-a1-segment1] FATAL-class failures remain — ONE segment-only retry (numbered-line template)
[prose-a1-segment1-retry] single generation call
[api] prose-a1-segment1-retry: model=deepseek/deepseek-v4-flash tokens in=2013 out=4249 reasoning=4083
[prose-a1-segment1-retry] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 1: NARRATOR narrates speech: 'NARRATOR: The boatman stands on the temple veranda holding a'
[prose-a1-segment1] done: 1 problem(s)
[prose-a1-segment3] single generation call
[api] prose-a1-segment3: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose-a1-segment3: model=deepseek/deepseek-v4-flash tokens in=1851 out=3231 reasoning=3110
[prose-a1-segment3] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 3: technique vocabulary 'symbol'
[prose-a1-segment3-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a1-segment3-spot-edit: model=deepseek/deepseek-v4-flash tokens in=187 out=395 reasoning=269
[prose-a1-segment3] done: 0 problem(s)
[prose-a1-segment5] single generation call
[api] prose-a1-segment5: model=deepseek/deepseek-v4-flash tokens in=1827 out=719 reasoning=589
[prose-a1-segment5] GATE FAILED (3 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 5: markdown asterisk in prose
  - act 1 segment 5: NARRATOR narrates speech: 'NARRATOR: Lek asks to see the ledger entry; Kamnan Noi slide'
  - act 1 segment 5: technique vocabulary 'symbol'
[prose-a1-segment5-spot-edit] one spot-edit pass (3 problem(s) to fix)
[api] prose-a1-segment5-spot-edit: model=deepseek/deepseek-v4-flash tokens in=245 out=1730 reasoning=1602
[prose-a1-segment5] done: 0 problem(s)
[prose-a2-segment1] single generation call
[api] prose-a2-segment1: model=deepseek/deepseek-v4-flash tokens in=1703 out=1534 reasoning=1397
[prose-a2-segment1] GATE FAILED (4 problem(s) — recorded, continuing without regeneration):
  - act 2 segment 1: missing '## Act 2 —' header line
  - act 2 segment 1: no 'PLACE:' line
  - act 2 segment 1: NARRATOR narrates speech: 'NARRATOR: The boatman asks what they are supposed to do now;'
  - act 2 segment 1: speaker prefix "The Boatman's Wife" maps to no character
[prose-a2-segment1-spot-edit] one spot-edit pass (4 problem(s) to fix)
[api] prose-a2-segment1-spot-edit: model=deepseek/deepseek-v4-flash tokens in=279 out=2335 reasoning=2311
[prose-a2-segment1] FATAL-class failures remain — ONE segment-only retry (numbered-line template)
[prose-a2-segment1-retry] single generation call
[api] prose-a2-segment1-retry: model=deepseek/deepseek-v4-flash tokens in=1757 out=3641 reasoning=3496
[prose-a2-segment1-retry] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 2 segment 1: NARRATOR narrates speech: 'NARRATOR: The boatman asks what they are supposed to do now,'
  - act 2 segment 1: speaker prefix "The Boatman's Wife" maps to no character
[prose-a2-segment1] done: 1 problem(s)
[prose-a2-segment3] single generation call
[api] prose-a2-segment3: model=deepseek/deepseek-v4-flash tokens in=1645 out=1299 reasoning=1234
[prose-a2-segment3] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 2 segment 3: speaker prefix "Boatman's Wife" maps to no character
[prose-a2-segment3-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a2-segment3-spot-edit: model=deepseek/deepseek-v4-flash tokens in=140 out=1977 reasoning=1914
[prose-a2-segment3] done: 0 problem(s)
[prose-a2-segment5] single generation call
[api] prose-a2-segment5: model=deepseek/deepseek-v4-flash tokens in=1603 out=1337 reasoning=1240
[prose-a2-segment5] passed gate
[prose-a2-segment5] done: 0 problem(s)
[prose-a3-segment1] single generation call
[api] prose-a3-segment1: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose-a3-segment1: empty content or length-truncated (finish=None, attempt 2/8)
[api] prose-a3-segment1: model=deepseek/deepseek-v4-flash tokens in=1693 out=1235 reasoning=1101
[prose-a3-segment1] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 3 segment 1: missing '## Act 3 —' header line
  - act 3 segment 1: no 'PLACE:' line
[prose-a3-segment1-spot-edit] one spot-edit pass (2 problem(s) to fix)
[api] prose-a3-segment1-spot-edit: model=deepseek/deepseek-v4-flash tokens in=221 out=672 reasoning=526
[prose-a3-segment1] done: 0 problem(s)
[prose-a3-segment3] single generation call
[api] prose-a3-segment3: model=deepseek/deepseek-v4-flash tokens in=1663 out=2182 reasoning=2080
[prose-a3-segment3] passed gate
[prose-a3-segment3] done: 0 problem(s)
[prose-a3-segment5] single generation call
[api] prose-a3-segment5: model=deepseek/deepseek-v4-flash tokens in=1631 out=914 reasoning=802
[prose-a3-segment5] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 3 segment 5: NARRATOR narrates speech: 'NARRATOR: The light through the salt bins casts three distin'
[prose-a3-segment5-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a3-segment5-spot-edit: model=deepseek/deepseek-v4-flash tokens in=196 out=1530 reasoning=1643
[prose-a3-segment5] done: 1 problem(s)
[prose-a4-segment1] single generation call
[api] prose-a4-segment1: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose-a4-segment1: model=deepseek/deepseek-v4-flash tokens in=1667 out=2681 reasoning=2563
[prose-a4-segment1] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 4 segment 1: missing '## Act 4 —' header line
  - act 4 segment 1: no 'PLACE:' line
[prose-a4-segment1-spot-edit] one spot-edit pass (2 problem(s) to fix)
[api] prose-a4-segment1-spot-edit: model=deepseek/deepseek-v4-flash tokens in=284 out=852 reasoning=722
[prose-a4-segment1] FATAL-class failures remain — ONE segment-only retry (numbered-line template)
[prose-a4-segment1-retry] single generation call
[api] prose-a4-segment1-retry: model=deepseek/deepseek-v4-flash tokens in=1721 out=4172 reasoning=4046
[prose-a4-segment1-retry] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 4 segment 1: missing '## Act 4 —' header line
[prose-a4-segment1] done: 1 problem(s)
[prose-a4-segment3] single generation call
[api] prose-a4-segment3: model=deepseek/deepseek-v4-flash tokens in=1700 out=2212 reasoning=2136
[prose-a4-segment3] passed gate
[prose-a4-segment3] done: 0 problem(s)
[prose-a4-segment5] single generation call
[api] prose-a4-segment5: model=deepseek/deepseek-v4-flash tokens in=1632 out=2592 reasoning=2477
[prose-a4-segment5] passed gate
[prose-a4-segment5] done: 0 problem(s)
[prose-a4] act header restored deterministically
[prose] coverage failure: act 1 choice 'I demand Kamnan Noi show us the red-inked column and explain': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
[prose] coverage failure: act 3 choice 'I challenge Kamnan Noi to show the two charts he drew and ex': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
[prose-coverage-repair] one spot-edit pass (2 problem(s) to fix)
[api] prose-coverage-repair: model=deepseek/deepseek-v4-flash tokens in=1641 out=6353 reasoning=4918
[prose] coverage repair accepted
[format] FATAL (2 unmappable item(s)) — no episode written:
  - act 2: speaker "Boatman's Wife" does not map to any character id
  - act 2: found 1 tag markers (need exactly 2)
```
