# Sprint 2 — Model shopping (benchmark of individual pipeline steps)

Date: sprint 2, task 1. Total benchmark spend: **$0.0199** (budget was ~$0.30).
Raw data: `/mnt/agents/output/sprint2/bench/` (results.json + per-model outputs).
Baseline for comparison: qwen/qwen3-235b-a22b-2507 (iter2 pipeline model).

## 1. ID mapping (PO's colloquial names → live OpenRouter IDs, prices $/token)

| PO name | Resolved ID | prompt | completion | notes |
|---|---|---|---|---|
| Latest Deepseek-v4-flash (not preview) | `deepseek/deepseek-v4-flash` | $0.0886/M | $0.1772/M | dated variants exist (`-0731`); used the undated stable ID |
| DeepSeek 3.2 | `deepseek/deepseek-v3.2` | $0.269/M | $0.40/M | |
| GLM5.3-Flash | `z-ai/glm-5.3-flash` | $0.075/M | $0.25/M | cheapest on paper; see transport failures below |
| (my pick) strong cheap instruction-follower | `minimax/minimax-m2.5` | $0.27/M | $1.08/M | **Gemini/OpenAI were unavailable**: every `google/*` and `openai/*` model returns HTTP 403 "not available in your region" for this key. MiniMax M2.5 probed OK. |
| (baseline) | `qwen/qwen3-235b-a22b-2507` | $0.0875/M | $0.35/M | iter1/iter2 pipeline model |

## 2. Benchmark design

- **PLAN**: current `plan.md` prompt, same ep_003 assignment (char_mor_duang,
  funeral parlor + salt store, same 8 tags), one call per model, temp 0.7.
  Scored with the iter2 plan gate (failure count; lower = better).
- **PROSE**: fixed input = iter2's `ep_003.plan.md`, one call per model,
  temp 0.8. Scored with the prose gate + Thai-verbatim count (the #1 qwen
  failure) + simile count.
- **SPOT-EDIT**: fixed input = iter2's `ep_003.prose.md` + its 9 known gate
  problems, "fix exactly these, change nothing else", temp 0.3. Scored:
  problems before→after + similarity to input (damage control; 1.0 = only
  the implicated sentences changed).

## 3. Results matrix (gate failures, lower = better)

| Model | PLAN fails | PROSE fails | Thai missing (of 8) | Similes | SPOT-EDIT (before→after) | Spot similarity |
|---|---|---|---|---|---|---|
| deepseek-v4-flash | 11 | **2** | **1** | 0 | **9 → 1** | 0.983 |
| deepseek-v3.2 | **6** | 10 | 7 | 0 | 9 → 2 | 0.982 |
| glm-5.3-flash | **FAILED** | **FAILED** | — | — | **FAILED** | — |
| minimax-m2.5 | 8 | 9 | 8 | 0 | 9 → 2 | 0.980 |
| qwen-235b (baseline, iter2) | 12 | 9 | 6 | 0 | n/a | n/a |

Per-step tokens/cost:
- v4-flash: plan 5.9k/2.1k $0.0011 · prose 4.0k/2.6k $0.0014 · spot 5.4k/2.9k $0.0014
- v3.2: plan 5.9k/2.1k $0.0024 · prose 4.0k/2.2k $0.0016 · spot 5.4k/1.4k $0.0011
- minimax-m2.5: plan 5.9k/2.3k $0.0041 · prose $0.0013 · spot $0.0013 (approx)
- glm-5.3-flash: all three cells FAILED (transport; below)

## 4. Qualitative notes

- **deepseek-v4-flash** — best prose by a wide margin: only 2 gate failures
  (one English anchor word miss, one Thai phrase paraphrased), 7/8 Thai
  phrases verbatim, zero similes, outcomes concrete. Best spot-editor:
  fixed 8 of 9 listed problems with 98% of the text untouched. Its PLAN
  output is weaker than v3.2's (11 vs 6 failures: sloppy TAG PLAN bullet
  shape, a budget overflow, missing act-4 DECISION beat) — but all its plan
  failures are mechanical-format issues, not comprehension issues; the
  outline itself is usable.
- **deepseek-v3.2** — best planner: 6 failures, cleanest outline structure,
  good decisions. But a poor prose writer for this task: ignored 7 of 8
  assigned Thai phrases (same disease as qwen).
- **minimax-m2.5** — middling planner (8 fails), ignored ALL 8 Thai phrases
  in prose (thai_miss 8), decent spot-editor (9→2, 98% similarity). Also the
  priciest of the three working models per token. Not competitive here.
- **glm-5.3-flash** — operationally unusable for this pipeline despite the
  lowest sticker price. It is a reasoning model served via Together that
  (a) burns most of max_tokens on reasoning, (b) non-streaming responses
  hang >15 min on keep-alive padding, (c) standard SSE streaming returns
  empty content to the driver's read-till-EOF parser. Only incremental
  readline streaming works, and even then a plan-sized call exceeded 12
  minutes without finishing. Recorded as FAILED on all cells rather than
  retried further.

## 5. Recommended mix

| Step | Model | Why | Est. cost/episode |
|---|---|---|---|
| PLAN | **deepseek/deepseek-v3.2** | best gate score (6 vs 11/12), cleanest outline structure; planning quality gates everything downstream | ~$0.0024 |
| PROSE | **deepseek/deepseek-v4-flash** | only model that copies Thai verbatim (7/8) and follows the marker/anchor machinery; 2 gate fails vs 9–10 for others | ~$0.0014 |
| SPOT-EDIT (if a repair step is added) | **deepseek/deepseek-v4-flash** | 9→1 problems at 0.983 similarity; v3.2 also fine (9→2) | ~$0.0014 |
| FORMAT | deepseek-v4-flash (or keep qwen) | not benchmarked as a cell (formatting is being restructured next task); v4-flash's instruction-following on prose suggests it; qwen baseline already adequate | ~$0.001 |

**Projected episode cost: ≈ $0.005–0.007** — same as today's all-qwen mix,
with better plan quality (v3.2: 6 fails vs qwen 12) and dramatically better
Thai fidelity (v4-flash: 1 miss vs qwen 6).

On the PO's openness to a costlier planner: **not needed** — v3.2 at
$0.27/M already beats qwen on the plan gate, and its remaining failures are
minor (one disallowed place, one missing act-4 DECISION beat, two outcome-
binding misses). No Sonnet-class expense justified.

If glm-5.3-flash's price is ever attractive again, it would need driver-side
work (incremental SSE reading + reasoning budget caps) — flagged for the
structural task, not recommended now.

## Headwinds / tailwinds
- Headwind: google/* and openai/* are region-blocked for this key (403) —
  the "Gemini Flash / GPT-mini" slot had to go to MiniMax, which
  underperformed. GLM transport quirks cost several benchmark hours.
- Tailwind: deepseek's two tiers split cleanly by strength (v3.2 plans,
  v4-flash writes/edits) at a combined price ≈ the current qwen mix; the
  benchmark was cheap ($0.02) and fully reproducible from
  `/mnt/agents/output/sprint2/bench/`.
