# Pipeline report — ep_005
- models: plan=deepseek/deepseek-v3.2, prose=deepseek/deepseek-v4-flash, spot-edit=deepseek/deepseek-v4-flash, format=deterministic (no LLM)
- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops
- tokens: prompt=23185, completion=41754
- cost estimate: $0.0138 (MODEL_PRICES in driver.py; update per model)
- final status: COMPLETED WITH GATE FAILURES (see report)

## Gate results
- plan (before spot-edit): FAIL (7 problem(s))
  - outline uses place 'The Mirror Mender', which is not in this episode's allowed places (['The Pawnshop', 'The Rice Ledger', 'The School Veranda'])
  - act 1: char_boatman is in the PRESENT line but gets no ENTRANCE beat in the first 6 beats — characters present from the start must be introduced before they speak
  - act 1: STAKES beat is beat 10 — it must land in the first 6 beats (segment 1)
  - act 1 [easy] FAIL outcome 'I find only dust and mothballs in the empty chest.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 2 [easy] FAIL outcome 'I am told the box is worthless tin and sent away.' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 2 [medium] choice 'Ask to see the ledger of pledges to check for any temple ite' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
  - act 2 [hard] choice 'Suggest Phra Kam temporarily surrender his rusted spoon to e' shares fewer than 2 content words with the page so far — choices may only use objects/facts/people the beats or sticky situation already established
- plan (after spot-edit): FAIL (4 problem(s))
  - outline uses place 'The Mirror Mender', which is not in this episode's allowed places (['The Pawnshop', 'The Rice Ledger', 'The School Veranda'])
  - act 2 [easy] FAIL outcome does not begin with 'I ' — outcomes are the PC speaking in first person
  - act 2 [medium] FAIL outcome 'I see only lists of knives and spoons, no religiou' shares no content word with its choice or the scene's beats — outcomes must be a concrete event resulting from THAT choice's action, naming its objects
  - act 3 beat 15: char_district_officer speaks/acts in dialogue before any ENTRANCE beat or act-1 PRESENT line introduces them
- prose (before spot-edit): FAIL (7 problem(s))
  - act 1 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
- prose (after spot-edit): PASS
- format: FAIL (1 problem(s))
  - act 2 choice 1 (easy) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'The appraiser pushes the box back and tells me it is worthle'

## Log
```
[plan-1-base] single generation call
[api] plan-1-base: model=deepseek/deepseek-v3.2 tokens in=4861 out=1024
[plan-1-base] passed gate
[plan-2-stakes-entrances] single generation call
[api] plan-2-stakes-entrances: model=deepseek/deepseek-v3.2 tokens in=1894 out=1804
[plan-3-decisions] single generation call
[api] plan-3-decisions: model=deepseek/deepseek-v3.2 tokens in=2609 out=2660
[plan-4-tags] single generation call
[api] plan-4-tags: model=deepseek/deepseek-v3.2 tokens in=3875 out=3106
[plan] GATE FAILED (7 problem(s)) — one spot-edit pass follows
[plan-spot-edit] one spot-edit pass (7 problem(s) to fix)
[api] plan-spot-edit: model=deepseek/deepseek-v4-flash tokens in=3477 out=9242
[plan] after spot-edit: 4 problem(s) remain — recorded, continuing
[prose] single generation call
[api] prose: empty content or length-truncated (finish=length, attempt 1/8)
[api] prose: empty content or length-truncated (finish=length, attempt 2/8)
[api] prose: model=deepseek/deepseek-v4-flash tokens in=5080 out=9174
[prose] GATE FAILED (7 problem(s) — recorded, continuing without regeneration):
  - act 1 segment 1: has 8 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 2 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
  - act 3 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 1: has 7 prose lines (expected 4-6) — rebalance lines around the markers
  - act 4 segment 3: has 4 prose lines (expected 2-3) — rebalance lines around the markers
  - act 4 segment 5: has 1 prose lines (expected 2-3) — rebalance lines around the markers
[prose-spot-edit] one spot-edit pass (7 problem(s) to fix)
[api] prose-spot-edit: model=deepseek/deepseek-v4-flash tokens in=1389 out=14744
[prose] after spot-edit: 0 problem(s) remain — recorded, continuing
[format] GATE FAILED (1 problem(s) — recorded, episode kept as-is):
  - act 2 choice 1 (easy) fail_outcome: outcome dialogue must begin with 'I ' (first person PC speech): 'The appraiser pushes the box back and tells me it is worthle'
[out] wrote /mnt/agents/output/sprint2/pass2/ep_005.json
[out] wrote /mnt/agents/output/sprint2/pass2/ep_005.plan.md
[out] wrote /mnt/agents/output/sprint2/pass2/ep_005.prose.md
```
