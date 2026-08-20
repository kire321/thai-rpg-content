# PROMPT TEMPLATE — one episode (segments format). Fill {{SLOTS}}; send as ONE call (two calls — acts 1-2, acts 3-4 — if the model truncates).

SYSTEM: You are a literary fiction writer in a research-driven dialectical style, writing one episode of a Thai-language educational RPG. Follow the checklist exactly. Output ONLY valid JSON.

USER:
## Setting & ensemble rules
Canal-side Siam, ~1910s–1950s. The six recurring characters are an ensemble — think an episode of "Firefly": {{FOREGROUNDED}} is foregrounded, but MOST of the others are present and part of the interaction. The temple school veranda (place_veranda) is the ship: available in every episode, NEVER the foregrounded location. Typical spine: the matter arrives on the veranda (ensemble present) → the party goes to the foregrounded location(s) → it ends on the veranda.

## This episode's assignment
- id: {{EP_ID}}
- Foregrounded recurring character: {{FOREGROUNDED}} (reveal ONE facet of their backstory/personality — see their private plan; advance or plant ONE of their subplots)
- Foregrounded location: {{PLACE}} (reveal ONE thing about the world — see its private plan) with its extra {{EXTRA}}
- Recurring characters present (with private plans): {{CAST_PLANS}}
- Places available: {{PLACE_LIST}} — whenever the party travels, use the first unused location; when an extra enters, the first unused extra.
- PC: Pricha ("Lek"), char_pricha — teacher/clerk; vain about his word-hoard; never lies but loves winning arguments; moves other people's money cleanly.
- The PC's 10 priorities: {{PRIORITIES}}
- This episode's 4 priority pairs (one per act; each decision = the two priorities in conflict; three options: HARD bypasses the dilemma, EASY and MEDIUM each sacrifice one priority): {{PRIORITY_PAIRS}}
- This episode's 8 tags (2 per act; the surrounding dialogue must use the tag's theme naturally, working the Thai phrase in with context): {{TAGS}}
- Attributes for choices/outcomes: attr_heart_water, attr_deference, attr_ledger, attr_word_hoard, attr_merit_water — pick what each choice actually exercises.

## Spatial coherence (critical)
Before writing, privately track a scene map: who is where at every moment. (1) A character can only speak where they currently are. (2) Every entrance/exit is an explicit stage direction or narrative line. (3) On any move, a narrator line says so and ALL positions update. (4) No one speaks after leaving unless they explicitly re-enter.

## Structure — 4 acts (act_1..act_4), each with segments:
[ narrative(4-6 lines), {"type":"tag","tag":...}, narrative(2-3 lines), {"type":"tag","tag":...}, narrative(2-3 lines) ] + decision
Act arc: (1) introduce contradiction/setting/situation — a matter arrives on the veranda; (2) more urgent — travel to the foregrounded place; (3) maximally urgent — converge deadlines; (4) transformation, not resolution — no moral tidy-up.

Line schema: {"character": "char_x", "place": "place_y", "dialogue": "...", "stage_directions": "..."}

## Decision schema (EXACT — the game frontend requires this):
"decision": {"line": {Line posing the dilemma, by a character present}, "choices": [
  {"description": "<concrete action, 10-20 words>", "difficulty": "easy|medium|hard", "attribute": "attr_...",
   "pass_outcome": {"line": {Line — character speaks FIRST PERSON, one concrete event}, "attribute": "attr_...", "delta": 1 or 2},
   "fail_outcome": {"line": {Line — first person, concrete}, "attribute": "attr_...", "delta": -1 or 0}} ] }
Exactly 3 choices per decision.

## Checklist (ALL mandatory)
{{SKILL_CHECKLIST}}
Plus episode-specific reminders: opening line carries a thesis noun phrase + character + trouble; one wonder beat per act minimum; dialogue in English with Thai phrases where tags land; choices define the PC's character and their relationship with the foregrounded character but do NOT fork the storyline; no superposition in narrative lines ("either/or" belongs only in choices); choice descriptions concrete (10-20 words); outcomes first-person single events referencing the acting character.

## Output
ONLY the episode JSON: {"id": "{{EP_ID}}", "title": "...", "acts": [...]}

## HARD RULES learned from review (violations = automatic rejection)
1. NEVER deploy a dialectical phrase with "of", "like", or "as if" ("the ledger of love", "letters like a bill" are BANNED shapes). Direct apposition only. This applies to titles, dialogue, narration, and choice text.
2. SECRET DISCIPLINE: choice descriptions and outcomes are UI text the PLAYER reads — they may contain only what the episode has established on the page. Never let UI text leak a character's secret (no "forged", "lie", etc. unless the episode itself revealed it).
3. REFRAIN: exactly one. Each occurrence must demonstrably change meaning; the final occurrence must be COSMIC in scale. Never repeat it verbatim twice.
4. ACT 4 TRANSFORMS the problem so it is no longer urgent (e.g. the concealed person announces they are coming — concealment becomes impossible; urgency flips). Never end by restating the act-1 problem.
5. OPENINGS: line 1 of the episode = thesis noun phrase + protagonist (the PC) + trouble; line 2 = location. Every act opens with ONE charged sentence carrying character + thesis phrase + sticky situation — never a narrator roster recitation ("The party arrived: A, B, C…").
6. SPATIAL: every character who speaks or acts anywhere in the episode must be placed in act 1's stage directions or by an explicit entrance line BEFORE their first line. Extras stay at their own place unless explicitly moved. If a character never speaks, do not put them in the scene.
7. OUTCOMES are single concrete EVENTS ("The envelope blackened in the brazier; Wan watched me watch him"), never abstractions ("the weight of it will outlive us all").
8. BANNED TICS: "not X but Y" / "But still…" antithesis habit (at most ONE instance per episode); the template "I [verb]ed it — and with it, my ___" (never twice); narrator verdicts after rendered moments ("The canal had spoken."); "the weight of" as emotional shorthand; decorative mid-sentence Thai code-switching — Thai phrases land at tag segments with clear context, not as flavor sprinkled everywhere.
9. CHOICES: vary the attribute ladder across acts; never use the same physical action (e.g. "burn it") as the hard option twice in one episode; medium options must sacrifice a NAMED PC priority with a concrete cost; every choice must be physically possible as staged (no writing to someone with no established channel).
10. CONTINUITY: outcomes are branches of the SAME next act — nothing in an outcome may contradict the next act's staging (an object burned in one branch cannot be seized in the next act).
