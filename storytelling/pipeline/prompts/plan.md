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
- the personal tie: the concrete named person or relationship (their mother, their sister, their creditor) that makes this stake THEIRS, and the act-1-or-2 line that will make that tie visible. A reader must be able to say WHY this character cares, in one sentence, from the text alone.
If a character has NO motivation triggered by this situation, CUT them from the episode — do not list them.

## CENTRAL OBJECT
Name it. State explicitly WHO OWNS IT and who possesses it right now. State HOW the reader learns both facts by the end of act 1 (which line, which gesture). The object appears early and recurs.

## REFRAIN
One line: `REFRAIN: <the refrain's exact act-1 sentence, verbatim as it will appear in the prose>`. The prose gate will check that its content words recur in all four acts, so keep the sentence short (≤12 words) and built from concrete repeatable words.

## ACT MAP
Four subsections (### Act 1 ... ### Act 4). For each act give: location; who is present (with every entrance/exit); what changes; the wonder beat (name which of the 4 techniques: exact loving inventory / the numinous domesticated / connoisseur attention / elegiac frame); the refrain occurrence — quote the exact sentence you will write in this act — and its NEW meaning at this occurrence. THE REFRAIN MUST APPEAR IN ALL FOUR ACTS, one occurrence each, meaning shifting each time, act-4 occurrence cosmic. Act 1 = matter arrives on the veranda, contradiction introduced, stakes clear within the first stretch; Act 2 = more urgent, party travels to the foregrounded place; Act 3 = maximally urgent, deadlines converge; Act 4 = TRANSFORMATION (the problem stops being urgent — e.g. the concealed person announces they are coming), ending back on the veranda. Never end by restating the act-1 problem.

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
The anchor phrases are FIXED and assigned by the pipeline — use them VERBATIM, do not invent or modify them:
{{ANCHOR_LIST}}

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

## SECRET IS NEVER THE SUBJECT
The concealed person's situation is BACKGROUND LOGISTICS ONLY — she is alive, elsewhere, present-tense, and her monthly schedule is simply how the world works. BANNED STORY MOVES: urns, ashes, funerary/merit rites connected to her, "outlived", "let her rest", "taken from life", claims to "reveal the truth about her", any character demanding the truth about her, any act-4 revelation about her. Act 4 transforms the SURFACE problem (the letter, the money, the schedule, the debt) — never the secret. If your act 4 reveals anything about the concealed person, the plan has failed; rewrite it.

## VOCABULARY HYGIENE (applies to the plan AND all downstream stages)
The following words are banned from the plan and everything derived from it — they poison the prose: "forgery", "forge/forged", "ghost", "dead/died/death", "the late X", "as if", "not X but Y" antitheses, "Or X. Or both." fragments. Frame the secret positively: Wan writes IN HIS SISTER'S HAND for a lady who lives elsewhere (present-tense, travel-distance away). Never use the word "forgery" even as a label — call it "writing in another's hand", "the copied hand", "the practiced signature". When confirming compliance anywhere in the plan, NEVER quote the banned words themselves — write "complies with the banned list" instead.
