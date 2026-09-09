# Pipeline report — ep_003
- models: plan=qwen/qwen3-235b-a22b-2507, prose=qwen/qwen3-235b-a22b-2507, format=qwen/qwen3-235b-a22b-2507
- mode: single pass, no retries, no restarts
- tokens: prompt=14179, completion=8249
- cost estimate: $0.0058 (MODEL_PRICES in driver.py; update per model)
- final status: COMPLETED WITH GATE FAILURES (see report)

## Gate results
- plan: FAIL (12 problem(s))
  - TAG PLAN does not contain the assigned Thai phrase for tag_198 verbatim: '…ยืนอยู่ตรงหน้า'
  - outline uses place 'The Pawnshop', which is not in this episode's allowed places (['The Funeral Parlor', 'The Salt Store', 'The School Veranda'])
  - act 1 beat 11: char_boatman speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 [easy] choice 'Accept the red ink without proof' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 1 [easy] FAIL outcome 'I hesitate and he snatches the paper back.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 1 [medium] choice 'Demand the boatman’s testimony' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 1 [medium] choice references char_boatman, who is not on stage and never entered
  - act 1 [hard] choice 'Ask Kamnan Noi to verify the sky' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 2 [easy] choice 'File the widow’s version' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 2 [medium] choice 'Record both times' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 3 [medium] choice 'Lock it in the tin box' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 4: no DECISION beat (every act needs exactly one, ending the act)
- prose: FAIL (9 problem(s))
  - tag markers ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_250', 'tag_288', 'tag_330'] != assigned set ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330'] (each tag needs exactly one marker line '[[tag_xxx]]')
  - marker [[tag_288]]: assigned Thai phrase 'ไม่ใช่ปัญหาหรอก' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_330]]: assigned Thai phrase 'ผมมีสอน' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_089]]: assigned Thai phrase 'ผมดีใจที่ได้ยิน' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_083]]: assigned Thai phrase 'เดาง่ายมาก' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_250]]: assigned Thai phrase 'รู้สึกไม่เหมือนเดิม' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_059]]: the line immediately before it does not use the English anchor word 'finish' (prev line: 'Present: Lek, Kamnan Noi. The rain starts — soft on the veranda roof. ')
  - marker [[tag_059]]: assigned Thai phrase 'ยังเล่าไม่จบ' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_198]]: assigned Thai phrase '…ยืนอยู่ตรงหน้า' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
- format: FAIL (58 problem(s))
  - act 1 segment 1 line 6: third-person narration attributed to 'char_funeral_timekeeper' (narration must be char_narrator)
  - act 1 segment 2: Thai phrase 'ไม่ใช่ปัญหาหรอก' for tag 'tag_288' does not appear in the segment preceding its tag
  - act 1 segment 4: the line immediately before tag 'tag_330' does not use its English anchor word 'class' (last line: 'I’ll need proof — a tide stamp, a boat log.')
  - act 1 segment 4: Thai phrase 'ผมมีสอน' for tag 'tag_330' does not appear in the segment preceding its tag
  - act 1 segment 5 line 1: third-person narration attributed to 'char_funeral_timekeeper' (narration must be char_narrator)
  - act 1 choice 1 (easy): description is 6 words (must be 10-20)
  - act 1 choice 2 (medium): description is 4 words (must be 10-20)
  - act 1 choice 3 (hard): description is 7 words (must be 10-20)
  - act 2 segment 2: the line immediately before tag 'tag_083' does not use its English anchor word 'guess' (last line: 'Kamnan Noi writes the fire’s time in his small ledger.')
  - act 2 segment 2: Thai phrase 'เดาง่ายมาก' for tag 'tag_083' does not appear in the segment preceding its tag
  - act 2 segment 3 line 1: third-person narration attributed to 'char_salt_clerk' (narration must be char_narrator)
  - act 2 segment 4: the line immediately before tag 'tag_230' does not use its English anchor word 'tell' (last line: 'I don’t read time — only salt — but the lantern was lit when I left.')
  - act 2 segment 4: Thai phrase 'มีเรื่องจะบอก' for tag 'tag_230' does not appear in the segment preceding its tag
  - act 2 segment 5: has 4 lines (expected 2-3)
  - act 2 segment 5 line 1: third-person narration attributed to 'char_pawnshop_appraiser' (narration must be char_narrator)
  - act 2 segment 5 line 3: third-person narration attributed to 'char_pawnshop_appraiser' (narration must be char_narrator)
  - act 2 choice 1 (easy): description is 4 words (must be 10-20)
  - act 2 choice 2 (medium): description is 3 words (must be 10-20)
  - act 2 choice 3 (hard): description is 6 words (must be 10-20)
  - act 3 segment 1 line 5: third-person narration attributed to 'char_boatman' (narration must be char_narrator)
  - act 3 segment 2: the line immediately before tag 'tag_250' does not use its English anchor word 'feel' (last line: 'The naming means nothing if the land is gone.')
  - act 3 segment 2: Thai phrase 'รู้สึกไม่เหมือนเดิม' for tag 'tag_250' does not appear in the segment preceding its tag
  - act 3 segment 4: the line immediately before tag 'tag_198' does not use its English anchor word 'stand' (last line: 'I don’t feel the same as before — something in the air has shifted.')
  - act 3 segment 4: Thai phrase '…ยืนอยู่ตรงหน้า' for tag 'tag_198' does not appear in the segment preceding its tag
  - act 3 segment 5 line 1: third-person narration attributed to 'char_fire_stoker' (narration must be char_narrator)
  - act 3 choice 1 (easy): description is 7 words (must be 10-20)
  - act 3 choice 2 (medium): description is 6 words (must be 10-20)
  - act 3 choice 2 (medium) pass_outcome: place 'place_rice_ledger' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 3 choice 2 (medium) fail_outcome: place 'place_rice_ledger' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 3 choice 3 (hard): description is 7 words (must be 10-20)
  - act 4 segment 1 line 4: unknown character 'char_kam'
  - act 4 segment 2: the line immediately before tag 'tag_059' does not use its English anchor word 'finish' (last line: 'I have something to tell you.')
  - act 4 segment 2: Thai phrase 'ยังเล่าไม่จบ' for tag 'tag_059' does not appear in the segment preceding its tag
  - act 4 segment 3 line 2: unknown character 'char_kam'
  - act 4 segment 4: the line immediately before tag 'tag_198' does not use its English anchor word 'stand' (last line: 'Time is.')
  - act 4 segment 4: Thai phrase '…ยืนอยู่ตรงหน้า' for tag 'tag_198' does not appear in the segment preceding its tag
  - act 4 segment 5 line 1: place 'place_river_post' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 4 segment 5 line 2: place 'place_river_post' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 4 decision.line: unknown character 'char_kam'
  - act 4 choice 1 (easy): description is 5 words (must be 10-20)
  - act 4 choice 2 (medium): description is 3 words (must be 10-20)
  - act 4 choice 3 (hard): description is 4 words (must be 10-20)
  - tags used ['tag_059', 'tag_083', 'tag_198', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330'] != assigned set ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330']
  - act 1: dialogue not found in the prose (formatter-invented or rewritten): 'Why the record changed now, six days after the coffin left?'
  - act 1: dialogue not found in the prose (formatter-invented or rewritten): 'The tide log shows the boat arrived at 4:08, so the body must have die'
  - act 1: dialogue not found in the prose (formatter-invented or rewritten): 'The boatman burned his log. He said the water lied.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'I burned the log because the widow paid me double to lie.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'Why are you telling me now?'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'The fire scared me — the house fell at 3:58, same as the tide.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'Did you see the clock?'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'I don’t read time — only salt — but the lantern was lit when I left.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'Why did she burn the house?'
  - act 3: dialogue not found in the prose (formatter-invented or rewritten): 'Why do you care?'
  - act 3: dialogue not found in the prose (formatter-invented or rewritten): 'The boy is my nephew — born under Rahu.'
  - act 3: dialogue not found in the prose (formatter-invented or rewritten): 'Does that prove the fire started then?'
  - act 4: dialogue not found in the prose (formatter-invented or rewritten): 'I’m not finished yet — the words sharp between us.'
  - act 4 decision: description not found in the prose (formatter-invented or rewritten): 'Press for the full story'
  - act 4 decision: dialogue not found in the prose (formatter-invented or rewritten): 'I demand the rest and he tells me everything.'

## Log
```
[plan] single generation call
[api] plan: model=qwen/qwen3-235b-a22b-2507 tokens in=5779 out=2061
[plan] GATE FAILED (12 problem(s) — recorded, continuing without regeneration):
  - TAG PLAN does not contain the assigned Thai phrase for tag_198 verbatim: '…ยืนอยู่ตรงหน้า'
  - outline uses place 'The Pawnshop', which is not in this episode's allowed places (['The Funeral Parlor', 'The Salt Store', 'The School Veranda'])
  - act 1 beat 11: char_boatman speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 [easy] choice 'Accept the red ink without proof' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 1 [easy] FAIL outcome 'I hesitate and he snatches the paper back.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 1 [medium] choice 'Demand the boatman’s testimony' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 1 [medium] choice references char_boatman, who is not on stage and never entered
  - act 1 [hard] choice 'Ask Kamnan Noi to verify the sky' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 2 [easy] choice 'File the widow’s version' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 2 [medium] choice 'Record both times' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 3 [medium] choice 'Lock it in the tin box' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 4: no DECISION beat (every act needs exactly one, ending the act)
[prose] single generation call
[api] prose: model=qwen/qwen3-235b-a22b-2507 tokens in=3878 out=1478
[prose] GATE FAILED (9 problem(s) — recorded, continuing without regeneration):
  - tag markers ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_250', 'tag_288', 'tag_330'] != assigned set ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330'] (each tag needs exactly one marker line '[[tag_xxx]]')
  - marker [[tag_288]]: assigned Thai phrase 'ไม่ใช่ปัญหาหรอก' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_330]]: assigned Thai phrase 'ผมมีสอน' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_089]]: assigned Thai phrase 'ผมดีใจที่ได้ยิน' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_083]]: assigned Thai phrase 'เดาง่ายมาก' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_250]]: assigned Thai phrase 'รู้สึกไม่เหมือนเดิม' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_059]]: the line immediately before it does not use the English anchor word 'finish' (prev line: 'Present: Lek, Kamnan Noi. The rain starts — soft on the veranda roof. ')
  - marker [[tag_059]]: assigned Thai phrase 'ยังเล่าไม่จบ' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
  - marker [[tag_198]]: assigned Thai phrase '…ยืนอยู่ตรงหน้า' does not appear in the stretch of prose preceding the marker (it must sit in the segment that precedes its tag, glossed by context in the same line)
[format] single generation call
[api] format: model=qwen/qwen3-235b-a22b-2507 tokens in=4522 out=4710
[format] passed gate
[format] GATE FAILED (58 problem(s) — recorded, episode kept as-is):
  - act 1 segment 1 line 6: third-person narration attributed to 'char_funeral_timekeeper' (narration must be char_narrator)
  - act 1 segment 2: Thai phrase 'ไม่ใช่ปัญหาหรอก' for tag 'tag_288' does not appear in the segment preceding its tag
  - act 1 segment 4: the line immediately before tag 'tag_330' does not use its English anchor word 'class' (last line: 'I’ll need proof — a tide stamp, a boat log.')
  - act 1 segment 4: Thai phrase 'ผมมีสอน' for tag 'tag_330' does not appear in the segment preceding its tag
  - act 1 segment 5 line 1: third-person narration attributed to 'char_funeral_timekeeper' (narration must be char_narrator)
  - act 1 choice 1 (easy): description is 6 words (must be 10-20)
  - act 1 choice 2 (medium): description is 4 words (must be 10-20)
  - act 1 choice 3 (hard): description is 7 words (must be 10-20)
  - act 2 segment 2: the line immediately before tag 'tag_083' does not use its English anchor word 'guess' (last line: 'Kamnan Noi writes the fire’s time in his small ledger.')
  - act 2 segment 2: Thai phrase 'เดาง่ายมาก' for tag 'tag_083' does not appear in the segment preceding its tag
  - act 2 segment 3 line 1: third-person narration attributed to 'char_salt_clerk' (narration must be char_narrator)
  - act 2 segment 4: the line immediately before tag 'tag_230' does not use its English anchor word 'tell' (last line: 'I don’t read time — only salt — but the lantern was lit when I left.')
  - act 2 segment 4: Thai phrase 'มีเรื่องจะบอก' for tag 'tag_230' does not appear in the segment preceding its tag
  - act 2 segment 5: has 4 lines (expected 2-3)
  - act 2 segment 5 line 1: third-person narration attributed to 'char_pawnshop_appraiser' (narration must be char_narrator)
  - act 2 segment 5 line 3: third-person narration attributed to 'char_pawnshop_appraiser' (narration must be char_narrator)
  - act 2 choice 1 (easy): description is 4 words (must be 10-20)
  - act 2 choice 2 (medium): description is 3 words (must be 10-20)
  - act 2 choice 3 (hard): description is 6 words (must be 10-20)
  - act 3 segment 1 line 5: third-person narration attributed to 'char_boatman' (narration must be char_narrator)
  - act 3 segment 2: the line immediately before tag 'tag_250' does not use its English anchor word 'feel' (last line: 'The naming means nothing if the land is gone.')
  - act 3 segment 2: Thai phrase 'รู้สึกไม่เหมือนเดิม' for tag 'tag_250' does not appear in the segment preceding its tag
  - act 3 segment 4: the line immediately before tag 'tag_198' does not use its English anchor word 'stand' (last line: 'I don’t feel the same as before — something in the air has shifted.')
  - act 3 segment 4: Thai phrase '…ยืนอยู่ตรงหน้า' for tag 'tag_198' does not appear in the segment preceding its tag
  - act 3 segment 5 line 1: third-person narration attributed to 'char_fire_stoker' (narration must be char_narrator)
  - act 3 choice 1 (easy): description is 7 words (must be 10-20)
  - act 3 choice 2 (medium): description is 6 words (must be 10-20)
  - act 3 choice 2 (medium) pass_outcome: place 'place_rice_ledger' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 3 choice 2 (medium) fail_outcome: place 'place_rice_ledger' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 3 choice 3 (hard): description is 7 words (must be 10-20)
  - act 4 segment 1 line 4: unknown character 'char_kam'
  - act 4 segment 2: the line immediately before tag 'tag_059' does not use its English anchor word 'finish' (last line: 'I have something to tell you.')
  - act 4 segment 2: Thai phrase 'ยังเล่าไม่จบ' for tag 'tag_059' does not appear in the segment preceding its tag
  - act 4 segment 3 line 2: unknown character 'char_kam'
  - act 4 segment 4: the line immediately before tag 'tag_198' does not use its English anchor word 'stand' (last line: 'Time is.')
  - act 4 segment 4: Thai phrase '…ยืนอยู่ตรงหน้า' for tag 'tag_198' does not appear in the segment preceding its tag
  - act 4 segment 5 line 1: place 'place_river_post' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 4 segment 5 line 2: place 'place_river_post' is not one of this episode's places (['place_funeral_parlor', 'place_salt_store', 'place_veranda'])
  - act 4 decision.line: unknown character 'char_kam'
  - act 4 choice 1 (easy): description is 5 words (must be 10-20)
  - act 4 choice 2 (medium): description is 3 words (must be 10-20)
  - act 4 choice 3 (hard): description is 4 words (must be 10-20)
  - tags used ['tag_059', 'tag_083', 'tag_198', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330'] != assigned set ['tag_059', 'tag_083', 'tag_089', 'tag_198', 'tag_230', 'tag_250', 'tag_288', 'tag_330']
  - act 1: dialogue not found in the prose (formatter-invented or rewritten): 'Why the record changed now, six days after the coffin left?'
  - act 1: dialogue not found in the prose (formatter-invented or rewritten): 'The tide log shows the boat arrived at 4:08, so the body must have die'
  - act 1: dialogue not found in the prose (formatter-invented or rewritten): 'The boatman burned his log. He said the water lied.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'I burned the log because the widow paid me double to lie.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'Why are you telling me now?'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'The fire scared me — the house fell at 3:58, same as the tide.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'Did you see the clock?'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'I don’t read time — only salt — but the lantern was lit when I left.'
  - act 2: dialogue not found in the prose (formatter-invented or rewritten): 'Why did she burn the house?'
  - act 3: dialogue not found in the prose (formatter-invented or rewritten): 'Why do you care?'
  - act 3: dialogue not found in the prose (formatter-invented or rewritten): 'The boy is my nephew — born under Rahu.'
  - act 3: dialogue not found in the prose (formatter-invented or rewritten): 'Does that prove the fire started then?'
  - act 4: dialogue not found in the prose (formatter-invented or rewritten): 'I’m not finished yet — the words sharp between us.'
  - act 4 decision: description not found in the prose (formatter-invented or rewritten): 'Press for the full story'
  - act 4 decision: dialogue not found in the prose (formatter-invented or rewritten): 'I demand the rest and he tells me everything.'
[out] wrote /mnt/agents/output/sprint1/iter2/ep_003.json
[out] wrote /mnt/agents/output/sprint1/iter2/ep_003.plan.md
[out] wrote /mnt/agents/output/sprint1/iter2/ep_003.prose.md
```
