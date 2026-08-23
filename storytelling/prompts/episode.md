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

## Voice & narration rules
11. ALL narration goes to char_narrator. The PC (char_pricha) speaks only his own dialogue, never narration. Narrator lines are never first person.
12. FLOW: every line must visibly continue the previous one — response, consequence, or reaction. Each scene must work the contradiction, characters, and objects set up in the episode's first line; no orphan lines, no topic jumps. Read last-line→first-line across every boundary.
13. INTRODUCE every character before or with their first line of dialogue: a short narrator line or stage direction giving who they are, what they are doing right now, and what they want. A reader who knows nothing must be able to follow.
14. PLOT CLARITY: within the first narrative segment of act 1, the reader must learn what the characters are trying to do and why it matters to them (the stakes, in their terms). No mystery-mongering about the surface plot.
15. Never have a character announce the location to no one. Location is established by narrator lines and stage directions only.
16. OUTCOMES (pass_outcome/fail_outcome lines) are always a non-narrator character's first-person dialogue — a concrete thing they say. Never narrator, never third person, never abstraction.

## Wonder (from the dialectical-fiction skill — mandatory)
17. At least ONE wonder beat per act, using one of: (a) exact loving inventory — a specialist's taxonomy, scale+precision ("eighty-four thousand elephants hung with netting of gold thread"); (b) the numinous domesticated — a marvel at the kitchen table with everyone calm, composure IS the wonder; (c) connoisseur attention — render a character's disciplined seeing; (d) the elegiac frame — foreknowledge that this world is passing ("the last reign in which men drank it twice a year"). Similes only from the story's own material.

## Coherence rules learned from the latest editorial review (violations = automatic rejection)
18. PC IDENTITY: the player character's id is char_pricha and his name is Pricha; "Lek" is his nickname. The FIRST narrator line that mentions him must state both ("Pricha — Lek to the whole landing — ..."). After that, pick ONE name and use it in every stage direction. Never let stage directions use a name the dialogue has never established.
19. SPEAKER BUDGET: at most 3 speaking characters in act 1 segment 1 (narrator + PC + one other). Other characters enter and are introduced in later segments/acts, each introduced by a narrator line or stage direction BEFORE or WITH their first line (rule 13). A character who has never been introduced never speaks — no exceptions, including one-word lines.
20. NO ORPHAN LINES: a line may never respond to something that has not happened on the page. Ban terse non-sequiturs ("Refused.", "Laughter at noon.") unless the immediately preceding lines contain the exact thing being refused/laughed at. Every line needs a visible hook in a previous line.
21. LINE COUNTS ARE EXACT: segment 1 of each act = 4-6 lines; segments 2 and 3 = 2-3 lines each. Count before submitting. A 7-line segment 1 is an automatic schema failure.
22. BANNED ABSOLUTELY (zero instances): "not X but Y" / "not X — Y" constructions ("Not carelessness. Haste.", "not erasure — it's correction", "not a request"); similes imported from outside the story's world ("like a prayer" — prayers are not this scene's material; similes may draw only on objects/actions already present in the episode).
23. TAG PLACEMENT: the Thai phrase(s) tied to a tag must appear INSIDE the narrative segment that the tag segment immediately follows — same segment, not a neighboring one. Each of the episode's 8 tag segments must have its phrase(s) in its own preceding segment.
24. NAME BRIDGES FOR EVERYONE: any character known by two names (full name + nickname/short form) gets the bridge at first mention ("Sangwan — Wan — ..."), exactly like the PC. After bridging, use one name consistently.
25. EVERY LINE MUST BE TRUE IN THE SCENE: a greeting, answer, or reaction must match what has actually happened on the page (no "you are back so late" to people who haven't left; no answering a question nobody asked). Re-read each line against the physical scene before submitting.
26. THAI GLOSS DISCIPLINE: when a line contains a Thai phrase, the English of THAT SAME LINE must gloss or clearly contextualize that exact phrase. Never put a Thai phrase in one character's line whose meaning belongs to another line.
27. NO DUPLICATE LINES: no line of dialogue may appear twice in the episode (verbatim or near-verbatim), across segment boundaries or within them. Repetition is only permitted for the single designated refrain, and the refrain must change wording at each occurrence.
28. BANNED TICS (additional, zero instances): "Or X. Or both." / "Or X. Or Y." fragment strings; "truth is in the X, not the Y" and every other "not the X" antithesis; these are in addition to rules 8 and 22.
29. SECRET DISCIPLINE, ABSOLUTE: the words "dead", "death", "the dead", "died", "ghost" may NOT appear anywhere in the episode in connection with the concealed person — not in dialogue, choices, outcomes, or stage directions. Planting means: objects, schedules, signatures, silences, third-person references to "the lady". A line that lets the reader conclude the person is dead is a leak.
30. REFRAIN FINAL OCCURRENCE: must escalate to genuinely cosmic scale — sky, sea, stars, the turning of the world — not merely weather or endurance. ("Rain darkened the ink but it held" is weather; "the current carrying the salutation into the mouth of the sea" is cosmic.)
31. TAG FIDELITY: you are given the definition of each assigned tag. The Thai phrase in the segment preceding a tag must exemplify THAT tag's meaning, and the 8 anchor phrases must all be different from each other.
32. CHOICE INTEGRITY: no two choice descriptions in the whole episode may be identical or near-identical. Within each choice, pass_outcome and fail_outcome must be DIFFERENT lines — success and failure may never produce the same sentence. No outcome line may be reused anywhere else in the episode.
33. CHARACTER-FACT CONSISTENCY: a character may only claim experiences the episode establishes as theirs. (The PC has never met the lady Nim — he cannot have memories of her; the PC is the teacher — no other character may claim his class.) Keep a fact ledger while writing: who has met whom, who does what job, what has physically happened. Every line must agree with it.
34. REFRAIN RECOGNIZABILITY: the final cosmic occurrence must still echo the refrain's core words (e.g. if the refrain is "one envelope, always on time", the cosmic version keeps "one" and "on time" while scaling to sea/stars — "One envelope. Always on time. The current carries it past the last landing, into the mouth of the sea."). Cosmic scale WITHOUT recognizable wording is a failure; recognizable wording WITHOUT cosmic scale is a failure.
35. SECRET IMPLICATIONS: language implying the concealed person exists only in memory ("she lives in my memory", "I remember her", "the late") is as much a leak as saying "dead". She must always be referred to as alive and elsewhere — present-tense, travel-distance away, never memory-distance.
36. BRIDGE POSITION: a character's name bridge must occur at or before the FIRST use of either name — if "Wan" is spoken in act 1, the Sangwan=Wan bridge must be in act 1 too.
