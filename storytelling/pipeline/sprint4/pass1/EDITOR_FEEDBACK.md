# EDITOR FEEDBACK — ep_007 "The Stamped Settlement" (sprint 4, pass 1)

Headline: the literary machinery is back and visible for the first time since the ep_006 strip — a real refrain arc, a textbook wonder beat, soft magical realism characters actually use. But the segment hard contract — previously ticked done — is broken again ([7,3,1], [7,3,2], [6,5,4], [6,3,3]; only act 4 in contract), and the formatter's fix was verbatim concatenation, which creates five-beat monster lines. Feature verdicts below.

---

## FEATURE 1 — Actions in stage directions, speech in dialogue, attributed to the speaker: **TICK (with notes)**

The core pattern holds throughout: no narrator-quoted speech anywhere; every spoken line sits with its speaker; entrances and physical action ride in stage directions:
- char_district_officer: [stands behind the Clerk, tapping his boot against a veranda post] *"The temple school's records of salt chits must be checked…"*
- char_boatman: [waits by his boat, one foot on the gunwale, holding a bamboo pole] *"I can take you now, but the water is falling."*
- char_rangsri: [hands Lek a charcoal pencil] *"How do you write 'account settled'?"*

Notes, not blockers: (a) junk filler stage directions — char_pricha [asks], char_delivery_boy [responds], char_grain_clerk [frowns]/[sighs] — these are speech-verbs restating the dialogue function; either give them physical content or leave empty. (b) The formatter's verbatim concatenation puts multi-character action sequences into single narrator dialogue lines (act 2 seg 1 line 1 carries: office description, Grain Clerk slides the box, points at the ledger, Grain Clerk's fingers, the 3-vs-5 discrepancy, Tax Clerk entering with the ink pot — five beats, and internally jumbled: the Clerk "stands behind the counter" *after* sliding the box). Action is narrated rather than staged there, but it's narrator-narration, which is the narrator's job; the problem is density, not attribution.

## FEATURE 2 — Beats carry multiple plan points: **NO-TICK (partially achieved, wrong mechanism)**

The good: act 1's opening line is genuinely dense — *"The Salt Clerk arrives on the veranda with his hands stained red from the broken chalk block, and he places a single grain of pink salt on the ledger Lek is writing in."* — character, mystery object, and relationship-to-Lek in one sentence. Act 1 line 2 packs discovery + demand + deadline + cost into one speech (*"…before the sun touches the canal's far bank, or the district will seal the salt store and fine the temple."*).

The bad: (a) act 1 lines 1–5 are still one-character-per-line roster sequencing (Clerk arrives / Officer states / Rangsri sits / Boatman waits) — each line introduces exactly one plan element, which is the BAD pattern in the standard, just with better sentences. (b) Where density *does* occur mid-episode, it is the formatter's concatenation, not composition — act 2 seg 1 line 1 is a comma-spliced fact-queue with jumbled internal order. Composed density (the "Bua stole his stakes" standard) interlocks elements causally; concatenated density lists them. The writer should be writing dense lines, not the formatter assembling them.

---

## (a) Regression check across the accumulated checklist

| Item | Verdict | Evidence |
|---|---|---|
| Segment counts (was TICKED, sprint 2) | **REGRESSED — un-tick** | act 1 [7,3,1] (segment 3 has ONE line — the empty-segment FATAL evidently doesn't catch 1-liners); act 2 [7,3,2]; act 3 [6,5,4]. 14 format failures recorded, episode shipped. The deterministic merger treats the contract as a merging target, not a gate. |
| Act length 8–12 | **PARTIAL REGRESSION** | 11 / 12 / 15 / 12 — act 3 over target. |
| Introductions (relaxed rule) | **PASS, one ordering muddle** | Rangsri's tableau intro (*"sits at the edge of the veranda with her lacquered box open on her lap, humming a low, unfinished tune, and does not look up"*) is the best introduction the pipeline has written. But the Delivery Boy speaks and acts in act 3 seg 1 ([runs up, holding out the grimy cloth bag]) and is then introduced *again* in seg 2 (*"The Delivery Boy runs up from the landing, out of breath"*) — a double entrance. No late reveals of obviously-noticed characters. |
| Refrain | **PRESENT — first time ever** | "The water is falling": act 1 pragmatic (*"I can take you now, but the water is falling."* — tide talk); act 2 emotional (*"her stillness a mirror to the water falling"*); act 4 cosmic (*"the whole turning world is water falling through the dark"*). Three occurrences, meaning demonstrably shifts, final reaches sky/turning-world scale and keeps the core wording. This is the skill's refrain arc, delivered. |
| Thesis phrase / machinery | **PRESENT** | Rangsri's sound-catching vial is soft magical realism characters *use* (act 2: held to the doorway; act 3 hard choice: *"ask what sound it caught"*; act 4: *"it will keep the records from attracting false laughter"*). The laugh → accounted-for → "account settled" chain is a second mini-refrain with a meaning shift. |
| Wonder beats | **PASS** | Act 3's *"The spilled pink salt glints in the last sun, each grain holding a tiny, perfect sunset, and everyone treats it as just spilled salt."* is a textbook numinous-domesticated beat — the composure IS the wonder. Also the act-1 inventory (*"three bundles of ten, two loose chits, one torn half"*). Act 4 closes elegiac. |
| Spatial truthfulness | **PASS (1 muddle)** | Travel veranda → Rice Ledger → salt store → veranda, all explicit; boatman calling from the canal is properly off-scene-voice. Only the Delivery Boy double entrance. |
| Dilemma-line voice diversity | **UNCHANGED DEFECT** | New template, same monoculture: *"How to prepare for the ledger check?"* / *"How to address the ledger discrepancy?"* / *"How to secure the evidence before the deadline?"* / *"How to respond after the stamp is pressed?"* — four identical "How to X?" PC-voiced menu lines. Third episode running (ep_006 was "Do I X, or Y?"). Each gate fix spawns a new uniform template. |
| Outcome-voice diversity | **IMPROVED** | Act 1 mixes *"I have… / I drop… / I note… / I see… / I get… / I hear…"* — the "I see" monoculture is broken in acts 1–2, though acts 3–4 drift back (~60% "I see"). Net: much better than ep_006's 23/24. |
| Tag field-priming | **IMPROVED — best so far** | tag_146: *"I overheard the assistant laughing about it yesterday."* (hearing field); tag_113: *"Everyone knows your assistant was at the salt store after dark."* (common-knowledge field); tag_065: *"He's an old friend of the assistant. They talk by the canal."* (friend field — theme, not token); tag_303: *"How do you write 'account settled'?"* (writing field, in-scene and dramatic). Weaker: tag_215 (*"I'll get the rest of the salt from where I saw it hidden."* — "get" is a weak carrier) and tag_029 (*"I didn't catch the full amount myself. The boy was too loud."* — splits between catch and loud). 6/8 solid, 2/8 weak, no cognate collisions. |

## (b) My three criteria (ep_006 in parentheses)

1. **Stakes legibility: 4/5 (3/5).** Deadline, cost, and mechanism all explicit by line 2; the 3-vs-5 discrepancy gives the mystery a concrete shape. Docked: the narrator pre-emptively calls them *"the forged chits"* (act 2 seg 2) — verdict delivered before the evidence, deflating the mystery the episode is still investigating.
2. **Choice–outcome consequentiality: 4/5 (3/5).** Divergent outcomes with real verbs and real costs (*"I drop a bundle of chits into the canal water."*); the act-3 hard choice operationalizes Rangsri's magic as a tool — exactly the skill's "does a character use it" test. Docked: acts 3–4 relapse into "I see".
3. **Ensemble choreography: 3/5 (2/5).** Travel clean, entrances mostly clean, one double entrance, but act 1 seg 1 runs four speaking voices (Clerk, Officer, Boatman + narrator) with the PC silent — over budget again — and the merged lines scramble who-did-what-when inside a single line.

## (c) Freeform — things not on the checklist

1. **The orphaned PC transgression.** Act 1 seg 3 (its only line): *"Lek slips a single chit from the school's box into his own sleeve, a chit marked with a date two days from now."* The never-lies, clean-money PC steals a future-dated chit — and nothing in the episode ever references it again. This is simultaneously the most interesting thing Lek does and a dangling thread: either it's the PC's contradiction (needs a payoff beat) or it's a plan artifact that should never have shipped. A fact-ledger gate ("every object moved must be accounted for by episode end") would catch the class.
2. **Markdown leak:** *"the vial labeled *A gift given without reason*"* — asterisks in shipped dialogue. Trivial lint.
3. **The act-4 closing line over-explains its own elegy:** *"…knowing this world of chalk ledgers and canal deadlines is already passing into a different kind of silence."* The skill's elegiac frame works because it's shadowed, not announced. The first half of that line (*"the whole turning world is water falling through the dark"*) is perfect; the second half captions it. Same disease as the old simile-captions, now in elegiac form.

## (d) Bottom line

- **Feature 1 (stage-direction actions / speaker-attributed dialogue): TICK.** Pattern holds; notes (junk SD fillers, merge-produced narrator action-queues) are polish items.
- **Feature 2 (dense beats): NO-TICK.** Act 1's opening line proves the writer can do it; the roster-sequential lines 1–5 and the concatenation-as-density mechanism prove the pipeline doesn't require it. Needed: a plan/writer constraint on composed density in act-1 openings, and a formatter rule that merging must not be the primary density source (better: merge nothing; fail and let the spot-edit re-balance).
- **Regression that un-ticks a done feature: the segment hard contract.** [7,3,1] / [7,3,2] / [6,5,4] shipped with 14 recorded failures. The FATAL floor must cover under-length segments (1-line segment 3), over-length segment 1s and 2s, and should treat its own merge log as a failure signal — right now the formatter "repairs" its way out of a contract it was built to enforce.

## Headwinds / tailwinds

**Tailwinds:** The machinery survived an entire episode for the first time: a working refrain arc with a cosmic final occurrence, a genuinely wonderful wonder beat (the sunset in the spilled salt, everyone calm), and soft magical realism that passes the use-it test (the vial). Rangsri is the pipeline's first character who feels inhabited — lacquered box, unfinished tune, sound-catching, and the closing gift. Stakes, discrepancy, misdirection (the boy's laugh vs the assistant's), and the stamped-but-unjust settlement all hang together; act 4 transforms through the stamp being pressed *without* exoneration. Tag priming is the best yet (6/8, theme-level).

**Headwinds:** The formatter is now the pipeline's biggest liar: it concatenates until the counts look right, which means the written prose is chronically over-budget and the shipped text bears the seams (jumbled beat order, five-fact sentences). Fix the budget at the writer, or make merging itself a FATAL signal — do not let the repair define the artifact. Dilemma lines have now failed the same way through three templates ("Do I…?", "How to…?") — the gate needs syntax-entropy across the four lines, not per-line checks. The PC's most interesting act (the stolen chit) is an orphan, and the episode's mystery is spoiled by the narrator's own word "forged" — small gates (object ledger, spoiler-word lint) would catch both. Act 3 runs long (15 lines); the act-level 8–12 target needs the same hard floor the segments were supposed to have.
