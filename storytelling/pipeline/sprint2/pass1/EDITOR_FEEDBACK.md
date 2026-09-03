# EDITOR FEEDBACK — ep_004 "The Incomplete Record" (sprint 2, pass 1, rebuilt pipeline)

Headline: the two structural embarrassments of the ep_003 era are dead. Thai is present in all 8 tag slots and correctly placed per the PO's restated rule; the formatter is a faithful transcriber (decisions verbatim from plan, zero invented content). The episode that shipped is instead sunk by two things the gates saw and shipped anyway — empty final segments in all 4 acts and act lengths of 17–23 lines against an 8–12 target — plus a literary problem no gate can see: the PC is a bystander in his own episode.

---

## (a) Verdict per rubric area

### 1. Common-sense fiction guidelines

**Show don't tell — IMPROVED, with a new clunky-tell subclass.** Third-person narration throughout; clean concrete action (*"Phum tilts the plate in the sun." / "He traces his finger over a corner of the glass."*). But the English gloss lines required after each Thai phrase have become a tell-machine: *"Lek nods, his expression unreadable, showing no love for the comment."*; *"Phum does not reach for it, ignoring that it can still be of use."*; *"The question hangs in the humid air as Phum looks tired."* Each explains the Thai line's meaning instead of dramatizing a reaction.

**Does the story make sense — MOSTLY, but the stakes are hollow.** The causal chain is legible (blank plate arrives → bureau demands reply → number found → plate sent as its own reply). What is never established: why any of this matters to Phum or Lek. The plan gate flagged "no STAKES beat" and it was never fixed — the bureau's demand has no cost attached. A blank plate from Bangkok is a curiosity, not a sticky situation. Compare ep_003's inheritance/audit pressure: absent here.

**Length — FAIL (worst mechanical defect).** Narrative lines per act: **19 / 18 / 23 / 17** against the 8–12 target. Segment 1 runs 12–20 lines, and **segment 5 is EMPTY in all four acts** (`"lines": []`). The format gate recorded all 12 count violations and shipped regardless; the deterministic formatter should hard-fail on an empty segment the way it hard-fails on unmappable speakers.

### 2. Dialectical-fiction skill

**Desire as practice/inventory/attention — PASS (best area).** Phum's want is rendered exactly right: *"Phum cleans his lens on his sleeve and looks at the envelope but does not touch it."*; *"I want to know what they are asking for, and it will cost me a trip to the letter-writer."* — a want folded into a cost, stated as practice. His examination of the plate (tilting in the sun, tracing the edge, reciting the number from memory) is connoisseur attention. Lek's ledger-keeping is practice too.

**Thesis machinery / noun phrases — THIN.** No "like"/"as if" similes (ban holding across three iterations now). But there is no discernible thesis texture either — no noun phrases, no institutions, no soft magical realism. The registry number "visible only at an angle" is the closest thing to a thesis image (truth legible only obliquely) and it is good; one image is not machinery.

**Wonder beats — PARTIAL.** The etched number at an angle and the blank plate that is "not blank; it has been fixed" are genuine connoisseur-seeing beats. Acts 2 and 4 have nothing — no inventory, no numinous, no elegiac frame anywhere in the episode.

**Four-act arc / act 4 transforms — WEAK PASS.** Act 4's close is the episode's best writing: *"He writes the registry number Phum recited. He leaves the rest of the line blank."* — the incomplete record rhyming with the blank plate, the untouched teacup beside the stool. The problem is transformed (the reply is gone; what remains is the gap in the ledger). But the urgency curve is flat: Phum solves the actual problem single-handedly mid-act-3, and acts 3–4 are procedure and denouement. No deadline converges (the mail-boat date from act 1 is never used as pressure).

**Characters as contradictions — PARTIAL.** Phum: the man with failing eyesight who is the only one who can see the number (*"ผมสายตาไม่ดี"* — "my eyes are bad" — then he reads what no one else can). That is a real structural irony, well deployed. Nobody else has one; the District Officer is a flat obstacle.

**Refrain — absent (third episode running).** The blank plate / blank ledger line is an *image* rhyme, not a verbal refrain; the skill requires a repeated phrase whose meaning changes. Still no refrain machinery in any output to date.

**Fatalism — ABSENT.** Nothing cosmic; the episode is a tidy bureaucratic anecdote.

**No moral tidy-up — PASS.** The ledger stays blank; the tea goes undrunk; nothing is absolved or explained.

**Anti-AI discipline — ONE VIOLATION.** *"The plate is not blank; it has been fixed."* is a "not X but Y" construction (rule 22: zero allowed). Em-dashes are controlled. The gloss-tells noted above are the residual tic.

### 3. Game requirements

**Thai / tags — PASS mechanically, FAIL dramatically (the big one).** All 8 Thai phrases present, each in the segment preceding its tag, each followed by an English-anchor line immediately before the marker — the PO's restated rule is satisfied structurally, and the prose gate passed. BUT the Thai lines are dramaturgical orphans: the Pond Diver's *"โทรกลับหาพี่ด้วยนะ"* ("call me back") is said to no one about nothing; the District Officer's *"ชอบสุดๆ"* ("love it!") about walking to the canal is bizarrely chipper for his menace function; *"ผมได้กลิ่นน้ำหอม"* ("I smell perfume") is a pure non-sequitur; Lek's *"มีเรื่องจะบอก"* ("I have something to tell you") is a cliffhanger the episode never pays off. Rules 20/25 (no orphan lines; every line true in the scene) are violated in spirit at exactly the tag slots — the pedagogical moments are the least believable lines in the episode. The vocab phrases are conversational filler, and the pipeline has no mechanism to give them a dramatic pretext.

**Narrator POV — FIXED.** Third person throughout; the two residual attribution slips (narration voiced to char_phum; the officer referring to himself in third person) were gate-recorded.

**Decisions — MAJOR IMPROVEMENT, two residual defects.** Choice descriptions are 10–20 words, concrete, object-bound, physically staged — first time ever. Pass/fail outcomes now diverge in action (*"I see a faint registry number surface on the wet glass"* vs *"I see only my own reflection, the plate unchanged"*; *"I pour the water over the stone… and shut the book"* vs *"I spill the jar, soaking the ledger page and blurring the registry number"*). Residual: (1) **every decision.line verbatim-duplicates a narrative line** (all 4 acts — e.g. the monk's *"The plate is blank, but the bureau demands a reply. How do we proceed?"* appears in segment 2 and again as the decision line); (2) acts 2 and 3 use the identical attribute ladder (deference/ledger/word_hoard), violating the vary-the-ladder rule; (3) act 1's hard choice has the PC "claiming" a blank plate is the complete reply — the PC never lies.

**Segments format — FAIL.** Empty segment 5 ×4; count blowouts ×8. JSON parses; shape is formally correct; content distribution is broken.

**Spine / travel — PASS.** Veranda → letter-writer's landing → veranda, with explicit travel and return lines. The foregrounded place is visited.

**Introductions — PARTIAL.** The Monk gets an entrance (*"arrives from the temple hall, holding a palm-leaf manuscript"*). Phum and the Pond Diver — the foregrounded character and the second-most-present extra — are never introduced; line 1 presumes the reader knows "Phum's stool." Act 1 segment 1 has 5 speakers (budget: 3).

---

## (b) Numbered defect list (severity order)

1. **Empty final segments in all 4 acts + massive count blowout.** Where: every act's segment 5 (`"lines": []`); segment 1s of 12/15/20/14 lines. Why: the writer places both tag markers late; the deterministic formatter splits faithfully and ships an empty segment instead of hard-failing. This is a ship-blocker class: the game renders an empty beat before every decision, and act lengths are ~2× target. The formatter must treat 0-line segments as FATAL, and the writer needs marker-position budgeting (the CHANGES3 headwind note already suspects this).

2. **Thai tag lines are orphan non-sequiturs.** Where: at minimum 4 of 8 (โทรกลับหาพี่ด้วยนะ, ชอบสุดๆ, ผมได้กลิ่นน้ำหอม, มีเรื่องจะบอก). Why: placement is now mechanically perfect and dramatically empty — the phrase is inserted, then the following English line reverse-engineers a gloss. The plan's TAG beat-pair mechanism needs a pretext: the scene beat must create a situation in which a person would actually say this phrase.

3. **PC is a bystander; the foregrounded NPC solves everything.** Where: Lek's shipped dialogue is four lines total ("Do you expect correspondence?", plus three Thai/gloss beats); Phum finds the number, dictates the reply, seals the envelope, hands it over. The PC's only agency is inside decision outcomes. Why: episodes are supposed to define the PC through the dilemma; here the dilemma is spectating on Phum's competence. A plan-level constraint is needed (the PC must hold the central thread — touch it in every act).

4. **Stakes absent (plan gate flagged, never fixed).** Where: act 1; the bureau's demand carries no cost. The STAKES beat was missing from the plan, the spot-edit didn't add it, and the pipeline proceeded. Why: without a cost, the episode is an errand; act 4's melancholy lands on nothing.

5. **decision.line duplicates a narrative line in all 4 acts.** Where: e.g. act 3's *"The registry number is found, but how do we ensure the reply reaches the bureau correctly?"* — spoken by Phum in segment 2, then repeated as the decision line. Why: the formatter builds the decision verbatim from the plan's dilemma beat, and the writer also writes that beat into the prose. One of the two must be suppressed (or the dilemma line must be written as a fresh line).

6. **Gloss-tells: English anchor lines explain instead of react.** Where: *"showing no love for the comment"*, *"ignoring that it can still be of use"*, *"The question hangs in the humid air as Phum looks tired."* Why: the PO rule forces an English-anchor line after the Thai; the writer satisfies it by narrating the Thai line's meaning. These are the episode's worst sentences and they sit at the highest-visibility slots.

7. **Foregrounded character never introduced; act-1 speaker budget blown.** Where: Phum and the Pond Diver speak from line 2 with no introduction; segment 1 has 5 speakers. Why: the plan's PRESENT-line grammar was fixed for rosters leaking onto the page, but nothing replaced it as an introduction mechanism for characters present from the start.

8. **Flat urgency curve; deadline planted and never used.** Where: act 1 plants the mail boat "two days hence"; no subsequent line references it; the reply is sent with time to spare. Why: no planner constraint that act 3 converge deadlines; the arc rule (maximally urgent) is unenforced.

9. **Minor rule violations:** one "not X but Y" (*"The plate is not blank; it has been fixed."*); acts 2–3 identical attribute ladders; act-1 hard choice makes the never-lies PC claim a blank plate is a complete reply; two gate-recorded narration-attribution slips.

---

## (c) Comparison vs ep_003 pass-2 defect list

| # | ep_003 pass-2 defect | Status | Evidence |
|---|---|---|---|
| 1 | Outcomes generic stock phrases | **FIXED** | Outcomes concrete, object-bound, first-person events (*"I drop the plate, and it cracks on the veranda floorboards."*) |
| 2 | Zero Thai | **FIXED mechanically / dramatically broken** | 8/8 phrases present and correctly placed per PO rule; but ≥4 are orphan non-sequiturs (defect 2 above) |
| 3 | like/as-if flood | **FIXED (holding)** | 0 similes, third consecutive clean output |
| 4 | Stakes never stated | **UNCHANGED** | Plan gate flagged missing STAKES beat; shipped without one; no cost attached to the bureau's demand |
| 5 | No introductions / budget | **IMPROVED** | Monk gets an entrance; but Phum and Pond Diver unintroduced, seg-1 has 5 speakers |
| 6 | Temporal inversion | **FIXED (holding)** | None found |
| 7 | Refrain failure | **UNCHANGED** | Still no verbal refrain; a good image rhyme (blank plate / blank ledger line) instead |
| 8 | Choices reference unestablished facts | **IMPROVED** | Choices built from established objects; mild exception: "The Mirror Mender" named in act-1 choice before the trade is shown |
| 9 | Telling captions | **IMPROVED** | Simile-captions gone; replaced by gloss-tells at tag slots (defect 6) |
| 10 | Spatial bookkeeping | **FIXED** | Explicit travel and return; outcomes staged where the scene is |
| 11 | Key-handoff charge | **N/A** | Different episode/character; but note the subplot-plant function is absent here — nothing of Phum's backstory is revealed or planted, which was the assignment |
| 12 | PC uncharacterized | **WORSE** | Lek now has ~4 lines and zero narrative agency; Phum gets all the practice/attention beats |
| 13 | Formatter regenerating | **FIXED** | Deterministic formatter; decisions verbatim from plan; zero invented strings. New gap: ships empty segments (defect 1) |
| N1 | First-person narrator (pass-2 new) | **FIXED** | Third-person narration throughout |
| N2 | Pass=fail outcome equivalence (pass-2 new) | **FIXED** | Pass/fail diverge in action in all 12 pairs |
| N3 | Urgency arc regression (fire-as-backstory) | **IMPROVED** | No inversion; but curve is flat — problem solved by NPC mid-act-3, planted deadline unused (defect 8) |
| N4 | decision.line duplication (pass-2 new) | **UNCHANGED** | All 4 acts: decision.line verbatim-repeats a narrative line |

**Tally: 8 fixed, 5 improved, 3 unchanged, 1 worse, 1 N/A.**

## Systemic vs one-off

**Systemic:** empty segments / marker budgeting (deterministic — writer behavior + missing FATAL check); Thai orphan lines (the beat-pair mechanism has no dramatic-pretext requirement); PC passivity (no plan constraint keeping the central thread in the PC's hands); missing STAKES enforcement (gate flagged, pipeline proceeded — detection without enforcement again); decision.line duplication (structural: plan beat serves two masters); gloss-tells (rule-driven, will recur); flat urgency (no deadline-convergence constraint).

**One-off:** the "not X but Y" instance; the two attribution slips; the act-1 hard choice bending the PC's never-lies trait.

---

## (d) My three criteria (ep_003 pass-2 scores in parentheses)

1. **Stakes legibility: 2/5 (3/5).** What the bureau wants is clear; what it costs anyone is never said. Regression from ep_003 iter2.
2. **Choice–outcome consequentiality: 4/5 (3/5).** Choices concrete and staged; pass/fail genuinely divergent; fail outcomes cost something (cracked plate, blurred number, drawn attention). Docked one point for the identical act 2/3 ladders and the lie in act-1 hard.
3. **Ensemble choreography: 3/5 (3/5).** Travel and return clean, no teleports, no hallucinated IDs; but two speaking characters never introduced and the 5-speaker opening segment is a crowd.

---

## Bottom line: trajectory check

**Converging, yes — bulk-ready, not yet.** The rebuild fixed the right things structurally: deterministic formatting killed an entire defect class, Thai placement works, decisions are real. The failure center of gravity has moved from "the pipeline corrupts content" to "the pipeline faithfully ships under-dramatized content": empty segments, double-length acts, a spectator PC, orphan Thai. All four remaining problems are plan/writer-stage and all four are mechanically checkable — which means they are all fixable by the same gate-with-authority pattern that worked for similes and transcription.

**Top 3 remaining fixes, in order:**
1. **Make segment structure a hard contract:** FATAL on any empty segment and on segment-1 >6 lines at the formatter; give the writer explicit marker-position budgets (lines 1–6 / 7–9 / 10–12 per act) so acts land at 8–12 lines. This is deterministic and cheap; until it bites, every episode ships malformed.
2. **Give the PC the thread and the stakes a cost:** plan-gate must *block* (not flag) a missing STAKES beat, and require the PC to act in every act's beats — not just inside decision outcomes. The current planner lets the foregrounded NPC carry the whole episode.
3. **Dramatic pretext for tag phrases + fresh dilemma lines:** the TAG beat-pair must include the situation that makes the Thai phrase something a person would say (a gate could at least check the phrase isn't the speaker's only context-free utterance); and the decision.line must be written as a new line, not reused from the prose — or the prose occurrence suppressed.

## Headwinds / tailwinds

**Tailwinds:** First-ever prose gate PASS. First episode with Thai in all 8 slots, placed per the PO's rule. First episode with 10–20-word choices and divergent pass/fail outcomes. The deterministic formatter means every remaining format error is measurable, not mysterious. Phum's contradiction (failing eyes / only one who can see) and the act-4 closing image (the blank ledger line, the untouched tea) show the models *can* hit the register when the plan gives them the material. Spot-edit demonstrably works (prose 2 → PASS).

**Headwinds:** The gate-authority problem persists in a new form: the plan gate flagged the missing STAKES beat and the pipeline shipped anyway — detection without enforcement, third iteration running. The writer's marker placement is reliably wrong (both markers late, every act), so until budgeting or a FATAL check lands, the empty-segment defect will recur in every episode. The tag-vocab list itself (conversational filler like "call me back", "love it!") fights the fiction — expect orphan Thai at some rate no matter how good the pretext mechanism gets, and budget for it. And the subplot-plant assignment (reveal one facet of the foregrounded character's private plan) was silently dropped this run — nobody checked, because nothing gates it.
