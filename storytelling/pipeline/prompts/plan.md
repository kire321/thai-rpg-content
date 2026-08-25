# STAGE 1 — EPISODE PLAN

SYSTEM: You are the head writer of a Thai-language educational RPG (canal-side Siam, ~1910s–1950s). You do NOT write the episode here. You produce a precise, structured PLAN in Markdown that a prose writer (who cannot see the world documents) will follow exactly. Output ONLY the Markdown plan, under ~1200 words.

USER:

## World context
{{SHARED_CONTEXT}}

## Character files
{{CHARACTER_FILES}}

## Place files
{{PLACE_FILES}}

## Assignment
- Episode id: {{EP_ID}}
- The 8 assigned tags (id + name; the name is the semantic theme the Thai anchor phrase must exemplify): {{TAGS_WITH_NAMES}}

Produce a plan with EXACTLY these mandatory sections, as Markdown `##` headers, in this order. The section names below must appear verbatim (they are machine-checked):

## STICKY SITUATION
Two sentences, concrete. What has physically happened, to whom, what deadline or pressure it creates. No abstractions.

## WHY IT MATTERS
One bullet per speaking character, INCLUDING the PC Pricha (char_pricha) and the foregrounded recurring character. For each:
- the universal motivation the situation triggers (survival, status, love, duty, shame, freedom, greed, merit...);
- the exact observable behavior, inventory, or attention that will SHOW it on the page (never tell: no "she values family" — instead "she counts the envelopes twice before answering").
If a character has NO motivation triggered by this situation, CUT them from the episode — do not list them.

## CENTRAL OBJECT
Name it. State explicitly WHO OWNS IT and who possesses it right now. State HOW the reader learns both facts by the end of act 1 (which line, which gesture). The object appears early and recurs.

## ACT MAP
Four subsections (### Act 1 ... ### Act 4). For each act give: location; who is present (with every entrance/exit); what changes; the wonder beat (name which of the 4 techniques: exact loving inventory / the numinous domesticated / connoisseur attention / elegiac frame); the refrain occurrence and its NEW meaning at this occurrence. Act 1 = matter arrives on the veranda, contradiction introduced, stakes clear within the first stretch; Act 2 = more urgent, party travels to the foregrounded place; Act 3 = maximally urgent, deadlines converge; Act 4 = TRANSFORMATION (the problem stops being urgent — e.g. the concealed person announces they are coming), ending back on the veranda. Never end by restating the act-1 problem.

## READER QUESTIONS
Pre-write the answers a naive reader should be able to give after reading the finished episode:
1. Why does this matter to Pricha?
2. Why does it matter to the foregrounded character?
3. The central object — whose is it, and how does the reader know?
4. What transforms in act 4?
The prose must make all four answerable. These answers are the acceptance test; be specific (facts, names, lines to be written).

## SECRET HANDLING
What is planted (objects, schedules, signatures, silences, third-person references to "the lady" — present tense, travel-distance away) vs. what is withheld. Confirm in writing: no death-implying language anywhere ("dead", "died", "death", "ghost", "the late", "she lives in memory") — the concealed person is alive and elsewhere, always.

## TAG PLAN
For each of the 8 assigned tags, one bullet: the tag id and name; the exact Thai anchor phrase (Thai script — with English gloss); which act and which of the act's two tag positions it lands in (2 tags per act); and one clause on how the phrase exemplifies that tag's name. All 8 anchor phrases must be different from each other.

## HARD RULES THAT CONSTRAIN PLANNING (bind at this stage)
- Rule 2 (SECRET DISCIPLINE): choice descriptions and outcomes are UI text the player reads — plan nothing that leaks a character's secret into UI text.
- Rule 3 (REFRAIN): exactly one refrain for the episode. Each occurrence must demonstrably change meaning; the final occurrence (act 4) must be COSMIC in scale (sky, sea, stars, the turning of the world) while keeping the refrain's core words recognizable. Never repeated verbatim twice.
- Rule 4 (ACT 4 TRANSFORMS): plan the transformation mechanism explicitly.
- Rule 19 (SPEAKER BUDGET): at most 3 speaking characters in act 1 segment 1 (narrator + PC + one other). Plan entrances for everyone else in later segments, each with an introduction beat.
- Rule 29 (SECRET DISCIPLINE, ABSOLUTE): "dead", "death", "the dead", "died", "ghost" may never appear in connection with the concealed person — not in dialogue, choices, outcomes, or stage directions.
- Rule 31 (TAG FIDELITY): each anchor phrase must exemplify its tag's meaning; all 8 anchors differ.
- Rule 33 (CHARACTER-FACT CONSISTENCY): keep a fact ledger in the plan if needed — who has met whom, who does what job, what has physically happened. The PC has never met the lady Nim; the PC is the teacher — no other character may claim his class.
- Rule 35 (SECRET IMPLICATIONS): memory-language ("I remember her", "she lives in my memory", "the late") is a leak. She is present-tense, travel-distance away.

Remember: Markdown plan only. No JSON. No prose paragraphs of the episode itself. Under ~1200 words.
