# Pipeline report — ep_003
- models: plan=qwen/qwen3-235b-a22b-2507, prose=qwen/qwen3-235b-a22b-2507, format=qwen/qwen3-235b-a22b-2507
- mode: single pass, no retries, no restarts
- tokens: prompt=11645, completion=7320
- cost estimate: $0.0051 (MODEL_PRICES in driver.py; update per model)
- final status: COMPLETED WITH GATE FAILURES (see report)

## Gate results
- plan: PASS
- prose: FAIL (4 problem(s))
  - marker [[tag_089]]: the line immediately before it does not use the English anchor word 'hear' (prev line: 'The widow slams a paper on the veranda rail; Lek sees the ink is smudg')
  - marker [[tag_250]]: the line immediately before it does not use the English anchor word 'uncomfortable' (prev line: 'The veranda clock strikes uneven; Kamnan Noi flinches, then notes the ')
  - marker [[tag_288]]: the line immediately before it does not use the English anchor word 'starting' (prev line: 'Lek follows the boatman to the funeral parlor, where the coffin lid re')
  - marker [[tag_198]]: the line immediately before it does not use the English anchor word 'standing' (prev line: 'The Rain Gauge Keeper calls from the landing: rain started at 3:55 AM,')
- format: FAIL (33 problem(s))
  - act 1 segment 1 line 4: third-person narration attributed to 'char_salt_clerk' (narration must be char_narrator)
  - act 1 segment 2: the line immediately before tag 'tag_089' does not use its English anchor word 'hear' (last line: 'My ears. The crossed-out red numbers behind the counter, their stain l')
  - act 1 segment 3 line 1: third-person narration attributed to 'char_pawnshop_appraiser' (narration must be char_narrator)
  - act 1 segment 4: the line immediately before tag 'tag_330' does not use its English anchor word 'waiting' (last line: 'The widow says her husband drew breath at 4:07, and the clock in the p')
  - act 1 segment 5: has 1 lines (expected 2-3)
  - act 1 choice 1 (easy): description is 6 words (must be 10-20)
  - act 1 choice 2 (medium): description is 8 words (must be 10-20)
  - act 1 choice 2 (medium) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'It’s over. I’m signing it.'
  - act 1 choice 3 (hard): description is 7 words (must be 10-20)
  - act 1 choice 3 (hard) pass_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'You must go tell him!'
  - act 2 segment 2: the line immediately before tag 'tag_083' does not use its English anchor word 'guess' (last line: 'Lek follows the boatman to the funeral parlor, where the coffin lid re')
  - act 2 segment 4: the line immediately before tag 'tag_288' does not use its English anchor word 'starting' (last line: 'I can’t hear it.')
  - act 2 choice 1 (easy): description is 8 words (must be 10-20)
  - act 2 choice 2 (medium): description is 5 words (must be 10-20)
  - act 2 choice 2 (medium) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'That’s no problem.'
  - act 2 choice 3 (hard): description is 8 words (must be 10-20)
  - act 2 choice 3 (hard) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'It’s right here.'
  - act 3 segment 1 line 1: empty dialogue
  - act 3 segment 2: the line immediately before tag 'tag_230' does not use its English anchor word 'tell' (last line: 'Lek sees the same time—4:07—scratched inside the coffin rim, a secret ')
  - act 3 segment 3 line 2: empty dialogue
  - act 3 segment 4: the line immediately before tag 'tag_198' does not use its English anchor word 'standing' (last line: '')
  - act 3 choice 1 (easy): description is 4 words (must be 10-20)
  - act 3 choice 1 (easy) pass_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'It’s the best way.'
  - act 3 choice 2 (medium): description is 6 words (must be 10-20)
  - act 3 choice 2 (medium) pass_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'Now I know.'
  - act 3 choice 2 (medium) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'Don’t throw it away!'
  - act 3 choice 3 (hard): description is 8 words (must be 10-20)
  - act 3 choice 3 (hard) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'Are you finished yet?'
  - act 4 segment 2: the line immediately before tag 'tag_059' does not use its English anchor word 'finished' (last line: 'The sky turns paper-white as the sun clears the trees, the light flat ')
  - act 4 segment 4: the line immediately before tag 'tag_288' does not use its English anchor word 'starting' (last line: 'I nod.')
  - act 4: missing decision object
  - duplicate dialogue at act 3 segment 1 line 5 (first at act 2 segment 5 line 2): 'I have the deed.'
  - tags used ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_288', 'tag_288', 'tag_330'] != assigned set ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330']

## Log
```
[plan] single generation call
[api] plan: model=qwen/qwen3-235b-a22b-2507 tokens in=4996 out=1517
[plan] passed gate
[prose] single generation call
[api] prose: model=qwen/qwen3-235b-a22b-2507 tokens in=2658 out=1286
[prose] GATE FAILED (4 problem(s) — recorded, continuing without regeneration):
  - marker [[tag_089]]: the line immediately before it does not use the English anchor word 'hear' (prev line: 'The widow slams a paper on the veranda rail; Lek sees the ink is smudg')
  - marker [[tag_250]]: the line immediately before it does not use the English anchor word 'uncomfortable' (prev line: 'The veranda clock strikes uneven; Kamnan Noi flinches, then notes the ')
  - marker [[tag_288]]: the line immediately before it does not use the English anchor word 'starting' (prev line: 'Lek follows the boatman to the funeral parlor, where the coffin lid re')
  - marker [[tag_198]]: the line immediately before it does not use the English anchor word 'standing' (prev line: 'The Rain Gauge Keeper calls from the landing: rain started at 3:55 AM,')
[format] single generation call
[api] format: model=qwen/qwen3-235b-a22b-2507 tokens in=3991 out=4517
[format] passed gate
[format] GATE FAILED (33 problem(s) — recorded, episode kept as-is):
  - act 1 segment 1 line 4: third-person narration attributed to 'char_salt_clerk' (narration must be char_narrator)
  - act 1 segment 2: the line immediately before tag 'tag_089' does not use its English anchor word 'hear' (last line: 'My ears. The crossed-out red numbers behind the counter, their stain l')
  - act 1 segment 3 line 1: third-person narration attributed to 'char_pawnshop_appraiser' (narration must be char_narrator)
  - act 1 segment 4: the line immediately before tag 'tag_330' does not use its English anchor word 'waiting' (last line: 'The widow says her husband drew breath at 4:07, and the clock in the p')
  - act 1 segment 5: has 1 lines (expected 2-3)
  - act 1 choice 1 (easy): description is 6 words (must be 10-20)
  - act 1 choice 2 (medium): description is 8 words (must be 10-20)
  - act 1 choice 2 (medium) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'It’s over. I’m signing it.'
  - act 1 choice 3 (hard): description is 7 words (must be 10-20)
  - act 1 choice 3 (hard) pass_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'You must go tell him!'
  - act 2 segment 2: the line immediately before tag 'tag_083' does not use its English anchor word 'guess' (last line: 'Lek follows the boatman to the funeral parlor, where the coffin lid re')
  - act 2 segment 4: the line immediately before tag 'tag_288' does not use its English anchor word 'starting' (last line: 'I can’t hear it.')
  - act 2 choice 1 (easy): description is 8 words (must be 10-20)
  - act 2 choice 2 (medium): description is 5 words (must be 10-20)
  - act 2 choice 2 (medium) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'That’s no problem.'
  - act 2 choice 3 (hard): description is 8 words (must be 10-20)
  - act 2 choice 3 (hard) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'It’s right here.'
  - act 3 segment 1 line 1: empty dialogue
  - act 3 segment 2: the line immediately before tag 'tag_230' does not use its English anchor word 'tell' (last line: 'Lek sees the same time—4:07—scratched inside the coffin rim, a secret ')
  - act 3 segment 3 line 2: empty dialogue
  - act 3 segment 4: the line immediately before tag 'tag_198' does not use its English anchor word 'standing' (last line: '')
  - act 3 choice 1 (easy): description is 4 words (must be 10-20)
  - act 3 choice 1 (easy) pass_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'It’s the best way.'
  - act 3 choice 2 (medium): description is 6 words (must be 10-20)
  - act 3 choice 2 (medium) pass_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'Now I know.'
  - act 3 choice 2 (medium) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'Don’t throw it away!'
  - act 3 choice 3 (hard): description is 8 words (must be 10-20)
  - act 3 choice 3 (hard) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'Are you finished yet?'
  - act 4 segment 2: the line immediately before tag 'tag_059' does not use its English anchor word 'finished' (last line: 'The sky turns paper-white as the sun clears the trees, the light flat ')
  - act 4 segment 4: the line immediately before tag 'tag_288' does not use its English anchor word 'starting' (last line: 'I nod.')
  - act 4: missing decision object
  - duplicate dialogue at act 3 segment 1 line 5 (first at act 2 segment 5 line 2): 'I have the deed.'
  - tags used ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_288', 'tag_288', 'tag_330'] != assigned set ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330']
[out] wrote /mnt/agents/output/sprint1/iter1/ep_003.json
[out] wrote /mnt/agents/output/sprint1/iter1/ep_003.plan.md
[out] wrote /mnt/agents/output/sprint1/iter1/ep_003.prose.md
```
