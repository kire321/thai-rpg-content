# Pipeline run report — ep_006 (sprint 3 pass 1, rescue run)

- models: plan=deepseek/deepseek-v3.2, prose/edit=deepseek/deepseek-v4-flash (deterministic formatter)
- tags picked by planner: tag_065, tag_182, tag_151, tag_284, tag_108, tag_010, tag_077, tag_006
- shortlist tags NOT used (for PO balancing): tag_129, tag_053, tag_070, tag_221
- cost estimate: $0.0091 (rescue-run prose+edit; full-pipeline attempts ~$0.10 total — see CHANGES5.md)
- final status: COMPLETED — all gates PASS on shipped artifact

## Gate results (shipped artifact)
- plan: 21 -> 12 after spot-edit (residuals RECORDED; among them: ALL THREE machinery gates —
  the plan spot-edit stripped every THESIS/REFRAIN/WONDER beat while fixing other classes)
- prose: 13 -> 0 after the single spot-edit (count/place/marker classes all repaired)
- format: PASS (0 errors, 0 fatal; deterministic marker repositioning + verbatim same-speaker
  merging applied where needed, logged in _format_log)
- validate: PASS (0 errors; zero Thai anywhere)

## Segment structure (narrative line counts per act)
[[6, 3, 3], [6, 2, 2], [6, 3, 3], [6, 3, 3]]

## Literary machinery survival (change set B)
NONE in the shipped episode — the plan spot-edit removed all machinery beats.
Gates fire correctly; the keep-better guard accepted the edit because total
problem count fell. Fix candidates in CHANGES5.md.
