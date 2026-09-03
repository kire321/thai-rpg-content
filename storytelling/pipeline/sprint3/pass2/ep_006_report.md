# Pipeline report — ep_006
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=33316, completion=29582
- cost estimate: $0.0150 (MODEL_PRICES in driver.py; update per model)
- final status: COMPLETED WITH GATE FAILURES (see report)
- tags picked by planner: tag_182, tag_284, tag_006, tag_108, tag_010, tag_151, tag_065, tag_077
- shortlist tags NOT used (for PO balancing): tag_129, tag_053, tag_070, tag_221

## Gate results
- plan (before spot-edit): FAIL (21 problem(s))
  - technique vocabulary 'tension' in the outline: ...'3. The Water Blessing Drummer tests the tension of his drum skin.\n\n\n6. Pom gives'... (the outline lists concrete events only — the writer must never see technique words)
  - outline contains 5 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - thesis noun phrase "the notebook-keeper, clerk of other people's news" uses 'of'/'like'/'as' — it must be direct apposition ("the letter-writer, clerk of other people's news")
  - act 1: STAKES beat is beat 7 — it must land in the first 6 beats (segment 1)
  - act 1 beat 18: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 1: beat budget seg1 has 9 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: beat budget seg2 has 10 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 1: beat budget seg3 has 21 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 2: beat budget seg1 has 17 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: a deadline is planted in acts 1-2 but no act-3 beat shows it converging (act 3 is the maximally-urgent act)
  - act 3 beat 14: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 3 beat 22: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 3: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg2 has 8 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 9 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4 beat 16: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 4 beat 20: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 4: beat budget seg1 has 17 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: beat budget seg2 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
- plan (after spot-edit): FAIL (21 problem(s))
  - technique vocabulary 'tension' in the outline: ...'3. The Water Blessing Drummer tests the tension of his drum skin.\n\n\n6. Pom gives'... (the outline lists concrete events only — the writer must never see technique words)
  - outline contains 5 comparison(s) ('like'/'as if'); beats must be direct assertions (the writer expands whatever the outline contains — give it no comparisons)
  - thesis noun phrase "the notebook-keeper, clerk of other people's news" uses 'of'/'like'/'as' — it must be direct apposition ("the letter-writer, clerk of other people's news")
  - act 1: STAKES beat is beat 7 — it must land in the first 6 beats (segment 1)
  - act 1 beat 18: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 1: beat budget seg1 has 9 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 1: beat budget seg2 has 10 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 1: beat budget seg3 has 21 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 2: beat budget seg1 has 17 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 2: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: a deadline is planted in acts 1-2 but no act-3 beat shows it converging (act 3 is the maximally-urgent act)
  - act 3 beat 14: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 3 beat 22: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 3: beat budget seg1 has 15 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 3: beat budget seg2 has 8 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 3: beat budget seg3 has 9 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4 beat 16: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 4 beat 20: TAG beat names no character — the theme scene needs someone in it, doing or feeling the tag's theme
  - act 4: beat budget seg1 has 17 beats (need 4-6) — place each TAG pair so segment line counts land
  - act 4: beat budget seg2 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
  - act 4: beat budget seg3 has 4 beats (need 2-3) — place each TAG pair so segment line counts land
- prose (before spot-edit): FAIL (14 problem(s))
  - prose contains 5 comparisons ('like'/'as if'); max 2 — state images directly instead of comparing them
  - act 1 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 3: has 10 prose lines (expected 2-3) — rebalance lines around the markers
  - act 1 segment 5: has 20 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 16 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 1: has 14 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 8 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 5: has 8 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 15 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - marker [[tag_108]]: the line immediately before it does not use the English anchor word 'interesting' (prev line: 'NARRATOR: “Which one should I prepare for final submission?” Pom asks ')
  - technique vocabulary 'tension' appears in the prose: ...'R: The Water Blessing Drummer tests the tension of his drum skin.\nNARRATOR: The '...
- prose (after spot-edit): FAIL (14 problem(s))
  - prose contains 5 comparisons ('like'/'as if'); max 2 — state images directly instead of comparing them
  - act 1 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 3: has 10 prose lines (expected 2-3) — rebalance lines around the markers
  - act 1 segment 5: has 20 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 16 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 1: has 14 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 8 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 5: has 8 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 15 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - marker [[tag_108]]: the line immediately before it does not use the English anchor word 'interesting' (prev line: 'NARRATOR: “Which one should I prepare for final submission?” Pom asks ')
  - technique vocabulary 'tension' appears in the prose: ...'R: The Water Blessing Drummer tests the tension of his drum skin.\nNARRATOR: The '...
- format: FAIL (3 problem(s))
  - act 1 segment 5: has 6 lines (expected 2-3) after mechanical merging
  - act 1 segment 5: has 6 lines (expected 2-3)
  - act 2 segment 4: the line immediately before tag 'tag_108' does not use its English anchor word 'interesting' (last line: '“Which one should I prepare for final submission?” Pom asks Lek, his e')

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4948 out=1616
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=2486 out=1836
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2641 out=3269
[plan-4-machinery] single generation call
[api] plan-4-machinery: model=deepseek/deepseek-v3.2 tokens in=4225 out=3596
[plan-5-tags] single generation call
[api] plan-5-tags: model=deepseek/deepseek-v3.2 tokens in=5573 out=4040
[plan] GATE FAILED (21 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (23 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=4895 out=11181
[plan] spot-edit DISCARDED (disqualified (machinery stripped / FATAL class grew)) — keeping the original, failures recorded
[prose] single generation call
[api] prose: model=deepseek/deepseek-v4-flash tokens in=6051 out=2028
[prose] GATE FAILED (14 problem(s) — recorded, continuing without regeneration):
  - prose contains 5 comparisons ('like'/'as if'); max 2 — state images directly instead of comparing them
  - act 1 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 1 segment 3: has 10 prose lines (expected 2-3) — rebalance lines around the markers
  - act 1 segment 5: has 20 prose lines (expected 2-3) — rebalance lines around the markers
  - act 2 segment 1: has 16 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 1: has 14 prose lines (expected 4-6) — rebalance lines around the markers
  - act 3 segment 3: has 8 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 5: has 8 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 15 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - marker [[tag_108]]: the line immediately before it does not use the English anchor word 'interesting' (prev line: 'NARRATOR: “Which one should I prepare for final submission?” Pom asks ')
  - technique vocabulary 'tension' appears in the prose: ...'R: The Water Blessing Drummer tests the tension of his drum skin.\nNARRATOR: The '...
[prose-spot-edit] one spot-edit pass (14 problem(s) to fix)
[api] prose-spot-edit: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose-spot-edit: empty content or length-truncated (finish=length, attempt 2/8)
[api] prose-spot-edit: model=deepseek/deepseek-v4-flash tokens in=2497 out=2016
[prose] spot-edit DISCARDED (would leave 17 problems vs 14 before) — keeping the original, failures recorded
[format] GATE FAILED (3 problem(s) — recorded, episode kept as-is):
  - act 1 segment 5: has 6 lines (expected 2-3) after mechanical merging
  - act 1 segment 5: has 6 lines (expected 2-3)
  - act 2 segment 4: the line immediately before tag 'tag_108' does not use its English anchor word 'interesting' (last line: '“Which one should I prepare for final submission?” Pom asks Lek, his e')
[out] wrote /mnt/agents/output/sprint3/pass2/ep_006.json
[out] wrote /mnt/agents/output/sprint3/pass2/ep_006.plan.md
[out] wrote /mnt/agents/output/sprint3/pass2/ep_006.prose.md
```
