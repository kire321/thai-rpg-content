# Pipeline report — ep_009
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v3.2, spot-edit=deepseek/deepseek-v3.2, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=49240, completion=16329
- cost estimate: $0.0198 (MODEL_PRICES in driver.py; update per model)
- final status: FAILED (hard contract violation — see report)
- tags picked by planner: tag_000, tag_005, tag_001, tag_002, tag_008, tag_011, tag_003, tag_014
- shortlist tags NOT used (for PO balancing): tag_004, tag_009, tag_012, tag_013

## Gate results
- plan (before spot-edit): FAIL (20 problem(s))
  - technique vocabulary 'thesis' in the outline: ...'e the morning boat.” — carries: stakes, thesis\n5. She places the blank paper on '... (the outline lists concrete events only — the writer must never see technique words)
  - outline contains 1 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - wonder beats: need one WONDER beat per act (found acts [1, 2, 4])
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The Funeral Parlor', "The Letter-Writer's Landing", 'The School Veranda'])
  - act 1: char_sangwan is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 5: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1: no beat labeled 'STAKES:' (one early beat must be a character stating aloud what they want and what it costs)
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_bua', 'char_sangwan']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 1 [medium] PASS outcome 'I hear him call across the water that the wait is ' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 1 [hard] PASS outcome 'I see him nod and sit down on the gunwale to wait.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 2 beat 3: char_pawnshop_appraiser speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 12: char_funeral_timekeeper speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 2 [medium] FAIL outcome 'I see her turn away and say she does not remember ' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 3: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 4: expected exactly 2 TAG beat-pairs (found 0) — each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat
  - act 4 [medium] FAIL outcome 'I see him remain silent and cover the jar with his' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
- plan (after spot-edit): FAIL (11 problem(s))
  - technique vocabulary 'thesis' in the outline: ...'on the third for four years. — carries: thesis\n6. The Dance Teacher says a brace'... (the outline lists concrete events only — the writer must never see technique words)
  - thesis noun phrase: need a THESIS beat in act 1 (the opening line) plus at least 2 later THESIS occurrences
  - wonder beats: need one WONDER beat per act (found acts [1, 2, 4])
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The Funeral Parlor', "The Letter-Writer's Landing", 'The School Veranda'])
  - act 1 beat 3: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 5: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_bua', 'char_sangwan']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 4 beat 8: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 4 [medium] FAIL outcome 'I see him remain silent and cover the jar with his' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
- prose-a1-segment1 (before spot-edit): FAIL (4 problem(s))
  - act 1 segment 1: missing '## Act 1 —' header line
  - act 1 segment 1: no 'PLACE:' line
  - act 1 segment 1: line has no 'Speaker:' prefix: '[The School Veranda]'
  - act 1 segment 1: has 7 lines (hard budget 4-6) — this segment's budget is the whole contract; add or merge lines
- prose-a1-segment1 (after spot-edit): FAIL (1 problem(s))
  - act 1 segment 1: PLACE '[The School Veranda]' is not one of the allowed places ['funeral parlor', "letter-writer's landing", 'school veranda']
- prose-a1-segment3 (before spot-edit): FAIL (1 problem(s))
  - act 1 segment 3: has 1 lines (hard budget 2-3) — this segment's budget is the whole contract; add or merge lines
- prose-a1-segment3 (after spot-edit): FAIL (1 problem(s))
  - act 1 segment 3: has 1 lines (hard budget 2-3) — this segment's budget is the whole contract; add or merge lines
- prose-a1-segment3 (retry): PASS
- prose-a1-segment5 (before spot-edit): PASS
- prose-a2-segment1 (before spot-edit): FAIL (1 problem(s))
  - act 2 segment 1: missing '## Act 2 —' header line
- prose-a2-segment1 (after spot-edit): PASS
- prose-a2-segment3 (before spot-edit): FAIL (2 problem(s))
  - act 2 segment 3: line has no 'Speaker:' prefix: '[They push through the heavy wooden doors and enter the fune'
  - act 2 segment 3: [[tag_002]] must terminate the segment's LAST line — no content line may follow the marker
- prose-a2-segment3 (after spot-edit): PASS
- prose-a2-segment5 (before spot-edit): FAIL (1 problem(s))
  - act 2 segment 5: has 4 lines (hard budget 2-3) — this segment's budget is the whole contract; add or merge lines
- prose-a2-segment5 (after spot-edit): PASS
- prose-a3-segment1 (before spot-edit): FAIL (2 problem(s))
  - act 3 segment 1: missing '## Act 3 —' header line
  - act 3 segment 1: markers [] — expected exactly one [[tag_008]] at the END of this segment's last line
- prose-a3-segment1 (after spot-edit): FAIL (1 problem(s))
  - act 3 segment 1: the last line must carry the English anchor word 'believe' before the marker (last: 'The District Officer: [enters, followed by a clerk with a le')
- prose-a3-segment3 (before spot-edit): PASS
- prose-a3-segment5 (before spot-edit): PASS
- prose-a4-segment1 (before spot-edit): FAIL (9 problem(s))
  - act 4 segment 1: missing '## Act 4 —' header line
  - act 4 segment 1: line has no 'Speaker:' prefix: '[An old woman climbs the steps, holding a shophouse paper ba'
  - act 4 segment 1: speaker prefix 'OLD WOMAN' maps to no character
  - act 4 segment 1: line under 'OLD WOMAN' has neither quoted speech nor a [stage direction] — narration belongs to NARRATOR
  - act 4 segment 1: line has no 'Speaker:' prefix: '[The old woman holds out the paper bag.]'
  - act 4 segment 1: speaker prefix 'OLD WOMAN' maps to no character
  - act 4 segment 1: line under 'OLD WOMAN' has neither quoted speech nor a [stage direction] — narration belongs to NARRATOR
  - act 4 segment 1: has 7 lines (hard budget 4-6) — this segment's budget is the whole contract; add or merge lines
  - act 4 segment 1: markers [] — expected exactly one [[tag_003]] at the END of this segment's last line
- prose-a4-segment1 (after spot-edit): FAIL (4 problem(s))
  - act 4 segment 1: NARRATOR line contains quoted speech: 'NARRATOR: An old woman calls out, "Nim? Are you here?"'
  - act 4 segment 1: NARRATOR line contains quoted speech: 'NARRATOR: The old woman holds out the paper bag and says, "I'
  - act 4 segment 1: the last line must carry the English anchor word 'anymore' before the marker (last: 'NARRATOR: The old woman holds out the paper bag and says, "I')
  - act 4 segment 1: narrator-subject leak — NARRATOR performs 'The Monk''s beat ('places'): 'NARRATOR: The Monk places a small ceramic jar on the veranda rail.' — the character must act/speak in his own line
- prose-a4-segment3 (before spot-edit): FAIL (1 problem(s))
  - act 4 segment 3: markers [] — expected exactly one [[tag_014]] at the END of this segment's last line
- prose-a4-segment3 (after spot-edit): FAIL (1 problem(s))
  - act 4 segment 3: the last line must carry the English anchor word 'break' before the marker (last: 'LEK: [eyes move from the practice sheets, to the small jar o')
- prose-a4-segment5 (before spot-edit): PASS
- prose (assembled, full-document checks): FAIL (13 problem(s))
  - NARRATOR line contains quoted speech: 'NARRATOR: An old woman calls out, "Nim? Are you here?"' — give the speech to the speaking character as '<Nickname>: [action] "words"'
  - NARRATOR line contains quoted speech: 'NARRATOR: The old woman holds out the paper bag and says, "I brought m' — give the speech to the speaking character as '<Nickname>: [action] "words"'
  - act 1 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4: no 'PLACE:' line (the formatter needs one per act, copied exactly from the allowed place names)
  - marker [[tag_008]]: the line immediately before it does not use the English anchor word 'believe' (prev line: 'The District Officer: [enters, followed by a clerk with a ledger.] "A ')
  - marker [[tag_003]]: the line immediately before it does not use the English anchor word 'anymore' (prev line: 'NARRATOR: The old woman holds out the paper bag and says, "I brought m')
  - marker [[tag_014]]: the line immediately before it does not use the English anchor word 'break' (prev line: 'LEK: [eyes move from the practice sheets, to the small jar on the rail')
  - prose: narrator-subject leak — NARRATOR performs 'The Monk''s beat ('places'): 'NARRATOR: The Monk places a small ceramic jar on the veranda rail.' — the character must act/speak in his own line
  - prose: NARRATOR line uses second person: 'NARRATOR: An old woman calls out, "Nim? Are you here?"'
  - act 1 choice 'I will give the Boatman a silver coin from the tin box to wa': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 2 choice 'I will give the bracelet to Lek to hold, telling him it is t': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 4 choice 'I will ask the Monk to chant a brief blessing over the jar w': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 4 choice 'I will open the jar and show the ash to The Dance Teacher to': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
- coverage (plan beats must reach the prose): FAIL (4 problem(s))
  - act 1 choice 'I will give the Boatman a silver coin from the tin box to wa': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 2 choice 'I will give the bracelet to Lek to hold, telling him it is t': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 4 choice 'I will ask the Monk to chant a brief blessing over the jar w': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
  - act 4 choice 'I will open the jar and show the ash to The Dance Teacher to': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
- format: FAIL (1 problem(s))
  - FATAL: coverage FATAL

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=5066 out=1244 reasoning=0
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2215 out=1283 reasoning=0
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2166 out=2164 reasoning=0
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=4639 out=2382 reasoning=0
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=4510 out=2827 reasoning=0
[plan] GATE FAILED (20 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (22 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v3.2 tokens in=3825 out=2815 reasoning=0
[plan] after spot-edit: 11 problem(s) remain — recorded, continuing
[prose-a1-segment1] single generation call
[api] prose-a1-segment1: model=deepseek/deepseek-v3.2 tokens in=2028 out=209 reasoning=0
[prose-a1-segment1] GATE FAILED (4 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 1: missing '## Act 1 —' header line
  - act 1 segment 1: no 'PLACE:' line
  - act 1 segment 1: line has no 'Speaker:' prefix: '[The School Veranda]'
  - act 1 segment 1: has 7 lines (hard budget 4-6) — this segment's budget is the whole contract; add or merge lines
[api] prose-a1-segment1-lines-line: model=deepseek/deepseek-v3.2 tokens in=117 out=11 reasoning=0
[prose-a1-segment1-spot-edit] one spot-edit pass (4 problem(s) to fix)
[api] prose-a1-segment1-spot-edit: model=deepseek/deepseek-v3.2 tokens in=355 out=215 reasoning=0
[prose-a1-segment1] done: 1 problem(s)
[prose-a1-segment3] single generation call
[api] prose-a1-segment3: model=deepseek/deepseek-v3.2 tokens in=1838 out=55 reasoning=0
[prose-a1-segment3] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 3: has 1 lines (hard budget 2-3) — this segment's budget is the whole contract; add or merge lines
[prose-a1-segment3-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a1-segment3-spot-edit: model=deepseek/deepseek-v3.2 tokens in=144 out=63 reasoning=0
[prose-a1-segment3] FATAL-class failures remain — ONE segment-only retry (numbered-line template)
[prose-a1-segment3-retry] single generation call
[api] prose-a1-segment3-retry: model=deepseek/deepseek-v3.2 tokens in=1871 out=58 reasoning=0
[prose-a1-segment3-retry] passed gate
[prose-a1-segment3] done: 0 problem(s)
[prose-a1-segment5] single generation call
[api] prose-a1-segment5: model=deepseek/deepseek-v3.2 tokens in=1802 out=86 reasoning=0
[prose-a1-segment5] passed gate
[prose-a1-segment5] done: 0 problem(s)
[prose-a1] PLACE line normalized to 'The School Veranda' (was unmappable or missing)
[prose-a2-segment1] single generation call
[api] prose-a2-segment1: model=deepseek/deepseek-v3.2 tokens in=1805 out=126 reasoning=0
[prose-a2-segment1] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 2 segment 1: missing '## Act 2 —' header line
[prose-a2-segment1-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a2-segment1-spot-edit: model=deepseek/deepseek-v3.2 tokens in=199 out=132 reasoning=0
[prose-a2-segment1] done: 0 problem(s)
[prose-a2-segment3] single generation call
[api] prose-a2-segment3: model=deepseek/deepseek-v3.2 tokens in=1726 out=79 reasoning=0
[prose-a2-segment3] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 2 segment 3: line has no 'Speaker:' prefix: '[They push through the heavy wooden doors and enter the fune'
  - act 2 segment 3: [[tag_002]] must terminate the segment's LAST line — no content line may follow the marker
[api] prose-a2-segment3-lines-line: model=deepseek/deepseek-v3.2 tokens in=133 out=18 reasoning=0
[prose-a2-segment3] line-level repair applied
[prose-a2-segment3-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a2-segment3-spot-edit: model=deepseek/deepseek-v3.2 tokens in=165 out=64 reasoning=0
[prose-a2-segment3] done: 0 problem(s)
[prose-a2-segment5] single generation call
[api] prose-a2-segment5: model=deepseek/deepseek-v3.2 tokens in=1696 out=94 reasoning=0
[prose-a2-segment5] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 2 segment 5: has 4 lines (hard budget 2-3) — this segment's budget is the whole contract; add or merge lines
[prose-a2-segment5-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a2-segment5-spot-edit: model=deepseek/deepseek-v3.2 tokens in=183 out=91 reasoning=0
[prose-a2-segment5] done: 0 problem(s)
[prose-a3-segment1] single generation call
[api] prose-a3-segment1: model=deepseek/deepseek-v3.2 tokens in=1809 out=127 reasoning=0
[prose-a3-segment1] GATE FAILED (2 problem(s) — recorded, continuing without regeneration):
  - act 3 segment 1: missing '## Act 3 —' header line
  - act 3 segment 1: markers [] — expected exactly one [[tag_008]] at the END of this segment's last line
[prose-a3-segment1-spot-edit] one spot-edit pass (2 problem(s) to fix)
[api] prose-a3-segment1-spot-edit: model=deepseek/deepseek-v3.2 tokens in=228 out=137 reasoning=0
[prose-a3-segment1] done: 1 problem(s)
[prose-a3-segment3] single generation call
[api] prose-a3-segment3: model=deepseek/deepseek-v3.2 tokens in=1698 out=92 reasoning=0
[prose-a3-segment3] passed gate
[prose-a3-segment3] done: 0 problem(s)
[prose-a3-segment5] single generation call
[api] prose-a3-segment5: model=deepseek/deepseek-v3.2 tokens in=1638 out=87 reasoning=0
[prose-a3-segment5] passed gate
[prose-a3-segment5] done: 0 problem(s)
[prose-a4-segment1] single generation call
[api] prose-a4-segment1: model=deepseek/deepseek-v3.2 tokens in=1755 out=130 reasoning=0
[prose-a4-segment1] GATE FAILED (9 problem(s) — recorded, continuing without regeneration):
  - act 4 segment 1: missing '## Act 4 —' header line
  - act 4 segment 1: line has no 'Speaker:' prefix: '[An old woman climbs the steps, holding a shophouse paper ba'
  - act 4 segment 1: speaker prefix 'OLD WOMAN' maps to no character
  - act 4 segment 1: line under 'OLD WOMAN' has neither quoted speech nor a [stage direction] — narration belongs to NARRATOR
  - act 4 segment 1: line has no 'Speaker:' prefix: '[The old woman holds out the paper bag.]'
  - act 4 segment 1: speaker prefix 'OLD WOMAN' maps to no character
  - act 4 segment 1: line under 'OLD WOMAN' has neither quoted speech nor a [stage direction] — narration belongs to NARRATOR
  - act 4 segment 1: has 7 lines (hard budget 4-6) — this segment's budget is the whole contract; add or merge lines
  - act 4 segment 1: markers [] — expected exactly one [[tag_003]] at the END of this segment's last line
[api] prose-a4-segment1-lines-line: model=deepseek/deepseek-v3.2 tokens in=136 out=19 reasoning=0
[api] prose-a4-segment1-lines-line: model=deepseek/deepseek-v3.2 tokens in=125 out=11 reasoning=0
[prose-a4-segment1] line-level repair applied
[prose-a4-segment1-spot-edit] one spot-edit pass (8 problem(s) to fix)
[api] prose-a4-segment1-spot-edit: model=deepseek/deepseek-v3.2 tokens in=403 out=156 reasoning=0
[prose-a4-segment1] done: 4 problem(s)
[prose-a4-segment3] single generation call
[api] prose-a4-segment3: model=deepseek/deepseek-v3.2 tokens in=1707 out=56 reasoning=0
[prose-a4-segment3] GATE FAILED (1 problem(s) — recorded, continuing without regeneration):
  - act 4 segment 3: markers [] — expected exactly one [[tag_014]] at the END of this segment's last line
[prose-a4-segment3-spot-edit] one spot-edit pass (1 problem(s) to fix)
[api] prose-a4-segment3-spot-edit: model=deepseek/deepseek-v3.2 tokens in=138 out=62 reasoning=0
[prose-a4-segment3] done: 1 problem(s)
[prose-a4-segment5] single generation call
[api] prose-a4-segment5: model=deepseek/deepseek-v3.2 tokens in=1659 out=67 reasoning=0
[prose-a4-segment5] passed gate
[prose-a4-segment5] done: 0 problem(s)
[prose] coverage failure: act 1 choice 'I will give the Boatman a silver coin from the tin box to wa': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
[prose] coverage failure: act 2 choice 'I will give the bracelet to Lek to hold, telling him it is t': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
[prose] coverage failure: act 4 choice 'I will ask the Monk to chant a brief blessing over the jar w': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
[prose] coverage failure: act 4 choice 'I will open the jar and show the ash to The Dance Teacher to': its objects/acts appear nowhere in the prose — the choice is orphaned from the story it resolves
[prose-coverage-repair] one spot-edit pass (4 problem(s) to fix)
[api] prose-coverage-repair: model=deepseek/deepseek-v3.2 tokens in=1461 out=1369 reasoning=0
[prose] coverage repair insufficient (1 remain) — discarded
[format] skipped: coverage FATAL (planned beats never reached the prose)
[format] FATAL (1 unmappable item(s)) — no episode written:
  - coverage FATAL
```
