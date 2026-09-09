# Pipeline report — ep_008
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=25003, completion=35620
- cost estimate: $0.0144 (MODEL_PRICES in driver.py; update per model)
- final status: FAILED (hard contract violation — see report)
- tags picked by planner: tag_045, tag_131, tag_209, tag_269, tag_087, tag_244, tag_081, tag_279
- shortlist tags NOT used (for PO balancing): tag_132, tag_278, tag_161, tag_288

## Gate results
- plan (before spot-edit): FAIL (37 problem(s))
  - technique vocabulary 'thesis' in the outline: ...'arate matter.— carries: intro:The Monk, thesis\n6. Kamnan Noi closes his ledger w'... (the outline lists concrete events only — the writer must never see technique words)
  - outline contains 6 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The River Post', 'The Salt Store', 'The School Veranda'])
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_mor_duang is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_pawnshop_appraiser is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_monk is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_type_monitor is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 4: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 7: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 8: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 9: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 10: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 11: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 12: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 13: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 14: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 15: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 beat 11: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_monk', 'char_mor_duang']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: dilemma line 'The rope in my hands is dry. A dry rope snaps.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 2 beat 6: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 13: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 15: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 18: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2: dilemma line 'This salt is for the boat, not the name.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 3: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 1 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: dilemma line 'My pen writes what the ledger accepts.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 4: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: dilemma line 'The rain will wash away pencil, but not ink.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 4 beat 16: the compass changes hands and is never referenced again — an object moved must be accounted for by episode end
  - act 4 beat 17: the folded changes hands and is never referenced again — an object moved must be accounted for by episode end
- plan (after spot-edit): FAIL (37 problem(s))
  - technique vocabulary 'thesis' in the outline: ...'arate matter.— carries: intro:The Monk, thesis\n6. Kamnan Noi closes his ledger w'... (the outline lists concrete events only — the writer must never see technique words)
  - outline contains 6 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - a PRESENT line stages the scene at 'The Pawnshop', which is not in this episode's allowed places (['The River Post', 'The Salt Store', 'The School Veranda'])
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_mor_duang is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_pawnshop_appraiser is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_monk is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1: char_type_monitor is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — non-obvious characters must be introduced before they speak (place-obvious ones need no introduction)
  - act 1 beat 4: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 6: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 7: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 8: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 9: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 10: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 11: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 12: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 13: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 14: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1 beat 15: opening-segment beat carries <2 plan elements — each opening beat must interlock (character intro AND stakes/setting/thesis in the same beat), not roster-sequencing
  - act 1: a run of 3+ single-element beats — merge them so each beat carries multiple plan elements
  - act 1 beat 11: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 1 opening stretch has 3 non-PC speakers ['char_boatman', 'char_monk', 'char_mor_duang']; budget is narrator + PC + one other — move later speakers' beats after the STAKES beat or into later acts
  - act 1: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: dilemma line 'The rope in my hands is dry. A dry rope snaps.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 2 beat 6: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 13: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 15: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2 beat 18: char_salt_clerk speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
  - act 2: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2: dilemma line 'This salt is for the boat, not the name.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 3: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 1 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: dilemma line 'My pen writes what the ledger accepts.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 4: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: dilemma line 'The rain will wash away pencil, but not ink.' reads as bare 'X or Y' menu-text — write dialogue the character would actually say that poses the choice (a question, or a fuller spoken line)
  - act 4 beat 16: the compass changes hands and is never referenced again — an object moved must be accounted for by episode end
  - act 4 beat 17: the folded changes hands and is never referenced again — an object moved must be accounted for by episode end
- prose (before spot-edit): FAIL (9 problem(s))
  - prose does not contain exactly four '## Act N' sections
  - speaker prefix "The Boatman's wife" maps to no character ("The Boatman's wife: [presses her forehead to the veranda flo") — rename it to a nickname from the Names list, or make the line NARRATOR:
  - junk stage direction [nods] — it merely restates the speech act; give it physical content or drop the brackets
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: Kamnan Noi says nothing, only watches the water.' — the words belong to the speaking character's own line
  - tag markers ['tag_045', 'tag_131', 'tag_209', 'tag_269'] != assigned set ['tag_045', 'tag_081', 'tag_087', 'tag_131', 'tag_209', 'tag_244', 'tag_269', 'tag_279'] (each tag needs exactly one marker '[[tag_xxx]]' at the end of the line carrying its English anchor word). MISSING: tag_087 belongs in act 3; tag_244 belongs in act 3; tag_081 belongs in act 4; tag_279 belongs in act 4
  - act 1 segment 1: has 15 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 16 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3: no 'PLACE:' line (the formatter needs one per act, copied exactly from the allowed place names)
- prose (after spot-edit): FAIL (9 problem(s))
  - prose does not contain exactly four '## Act N' sections
  - speaker prefix "The Boatman's wife" maps to no character ("The Boatman's wife: [presses her forehead to the veranda flo") — rename it to a nickname from the Names list, or make the line NARRATOR:
  - junk stage direction [nods] — it merely restates the speech act; give it physical content or drop the brackets
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: Kamnan Noi says nothing, only watches the water.' — the words belong to the speaking character's own line
  - tag markers ['tag_045', 'tag_131', 'tag_209', 'tag_269'] != assigned set ['tag_045', 'tag_081', 'tag_087', 'tag_131', 'tag_209', 'tag_244', 'tag_269', 'tag_279'] (each tag needs exactly one marker '[[tag_xxx]]' at the end of the line carrying its English anchor word). MISSING: tag_087 belongs in act 3; tag_244 belongs in act 3; tag_081 belongs in act 4; tag_279 belongs in act 4
  - act 1 segment 1: has 15 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 16 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3: no 'PLACE:' line (the formatter needs one per act, copied exactly from the allowed place names)
- format: FAIL (1 problem(s))
  - FATAL: prose does not have exactly acts 1-4 (found [1, 2, 3])

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4787 out=1107
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2079 out=1243
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2126 out=2552
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=4343 out=2901
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=4949 out=3636
[plan] GATE FAILED (37 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (39 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=5326 out=14580
[plan] spot-edit DISCARDED (disqualified (machinery stripped / FATAL class grew)) — keeping the original, failures recorded
[prose] single generation call
[api] prose: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose: model=deepseek/deepseek-v4-flash tokens in=0 out=0
[prose] GATE FAILED (9 problem(s) — recorded, continuing without regeneration):
  - prose does not contain exactly four '## Act N' sections
  - speaker prefix "The Boatman's wife" maps to no character ("The Boatman's wife: [presses her forehead to the veranda flo") — rename it to a nickname from the Names list, or make the line NARRATOR:
  - junk stage direction [nods] — it merely restates the speech act; give it physical content or drop the brackets
  - NARRATOR line narrates speech ('X asks/says'): 'NARRATOR: Kamnan Noi says nothing, only watches the water.' — the words belong to the speaking character's own line
  - tag markers ['tag_045', 'tag_131', 'tag_209', 'tag_269'] != assigned set ['tag_045', 'tag_081', 'tag_087', 'tag_131', 'tag_209', 'tag_244', 'tag_269', 'tag_279'] (each tag needs exactly one marker '[[tag_xxx]]' at the end of the line carrying its English anchor word). MISSING: tag_087 belongs in act 3; tag_244 belongs in act 3; tag_081 belongs in act 4; tag_279 belongs in act 4
  - act 1 segment 1: has 15 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 3: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 16 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3: no 'PLACE:' line (the formatter needs one per act, copied exactly from the allowed place names)
[prose-spot-edit] one spot-edit pass (9 problem(s) to fix)
[api] prose-spot-edit: model=deepseek/deepseek-v4-flash tokens in=1393 out=9601
[prose] spot-edit DISCARDED (would leave 14 problems vs 9 before) — keeping the original, failures recorded
[format] FATAL (1 unmappable item(s)) — no episode written:
  - prose does not have exactly acts 1-4 (found [1, 2, 3])
```
