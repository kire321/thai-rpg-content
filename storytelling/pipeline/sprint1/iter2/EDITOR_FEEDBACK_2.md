# EDITOR FEEDBACK 2 — ep_003 "The Red Ink" (iteration 2)

Method note: I evaluate what actually shipped in `ep_003.json`, not the gates' self-report. The 58 format-gate hits are real but the more important story this iteration is (a) a major POV regression the gates do not check at all, and (b) gates that now *detect* nearly everything but *ship* it anyway.

---

## (a) Verdict per rubric area

### 1. Common-sense fiction guidelines

**Show don't tell — MIXED, new failure mode.** Iter1's simile-captions are gone, but the prose stage has converted the whole episode to first-person interiority, and the formatter then attributed that interiority to `char_narrator`. Shipped narrator lines:
- *"The Funeral Timekeeper stands on the school veranda with a red-ink correction in hand, and I know right away it's about the widow's husband."*
- *"I feel the weight of his words, but the doubt stays."* (also the banned "the weight of" tic, rule 8)
- *"That's really easy to guess, I think — but I say nothing."*

Narrator lines are first-person PC interiority throughout — a direct violation of rule 11/57 ("Narrator lines are never first person") that **no gate checks**. This is the single biggest shipped defect.

**Does the story make sense — IMPROVED but timeline now muddled.** Stakes are spoken early (timekeeper: *"The death was at 4:07 AM, not 4:13, and the land audit begins tomorrow."*; the explicit STAKES line *"Correct the time or the land goes to the district"* exists in the prose but was **dropped by the formatter** and never shipped). New problem: the widow's house fire — iter1's act-4 climax — is now act-2 backstory (*"the house fell at 3:58, same as the tide"*), so the urgency curve is inverted: the catastrophe has already happened before the dispute is even joined, and acts 3–4 have nothing left to escalate toward.

**My three criteria** — scored in (d).

### 2. Dialectical-fiction skill

**Desire as practice/inventory/attention — PARTIAL, diluted.** Kamnan still gets practice beats (adjusting compass, recording the arrival minute, writing the fire's time in his small ledger). But iter1's rich attention-rendering is thinned; the tin-box beat (*"the box calls louder"*) — the one good PC desire beat — exists only in the prose and was dropped from the JSON.

**Thesis machinery / noun phrases — WEAKENED.** Similes: **zero** (the procedural fix worked perfectly). But the noun-phrase assets are also mostly gone: no "sky turned paper", no "chart gone blind"; only the Fire Stoker's *"Time burns. But paper lies."* carries the register. Removing the simile flood also removed most of the thesis texture — the baby went with the bathwater.

**Wonder beats — WORSE.** Iter1 had the bent pendulum, the flame dipping at 4:07, the time scratched inside the coffin rim. Iter2's candidates are a pink salt chit, cracked heels, a bent clock hand — concrete but inventory-lite, no numinous, no elegiac frame. The episode never travels to the funeral parlor, so the world's texture is four acts of veranda talk.

**Four-act arc / act 4 transforms — PARTIAL, arguably regressed.** Act 4 does deliver the private plan's subplot-3 beats (key slid across the wood, Kamnan walking to the riverbank in rising water — "does not return" is faithfully staged). But because the fire already happened in act 2's backstory, act 4 has no transformation of the *episode's* problem; the record dispute is simply abandoned. The final shipped line — *"…standing right in front of the flood."* — is a broken ellipsis fragment jammed into narration to satisfy a tag anchor.

**Characters as contradictions — PARTIAL.** The boatman gains a real contradiction (burned the log for the widow's double pay, then confesses from fear). The monk gains a motive (nephew born under Rahu). The appraiser remains a flat predator.

**Refrain — still absent.** No recurring phrase with changing meaning. UNCHANGED from iter1.

**Fatalism — PARTIAL.** *"Time burns. But paper lies."* and the convergent 3:58s gesture at the counting universe; Kamnan walking into the flood is the right cosmic register. But the pattern never accumulates on the page the way iter1's 3:55/3:58/4:07/4:08/4:13 sequence did.

**No moral tidy-up — FAIL (new).** Act 4's easy-outcome: *"I demand the rest and he tells me everything."* — Kamnan's sealed backstory dumped off-page on demand is exactly the revelation-on-cue the Gene Wolfe rule forbids, and it resolves the episode's one remaining mystery with a bow on it.

**Anti-AI discipline — MIXED.** Similes: fixed. Em-dash chains: much reduced. New tics: the banned "the weight of"; roster recitations (below); the ellipsis fragment.

### 3. Game requirements

**POV/narration — FAIL (ungated).** First-person narrator lines throughout, plus 6 gated misattributions.

**Roster recitations shipped — FAIL (new, ungated).** *"Present: Lek, Kamnan Noi, The Funeral Timekeeper."* appears as literal narrator dialogue at the top of acts 2, 3, 4. The plan grammar (`PRESENT:`) leaked onto the page — precisely the "narrator roster recitation" rule 5 bans.

**Thai — FAIL again in the shipped JSON.** Zero Thai phrases in the final episode; all 8 tag quizzes hang on nothing, second iteration running. The machinery (deterministic phrase assignment, three-stage gating) now exists and *recorded* every miss — but the episode shipped anyway. The pedagogical payload is still absent.

**Tags — FAIL.** tag_089 missing entirely, tag_198 duplicated; 7 of 8 English anchor-word placements wrong (gated).

**Decisions — MIXED.** Act 4 now has a decision (fixed). But: all 12 choice descriptions are 3–7 words (gated; the 10–20-word rule has never once been satisfied in either iteration); act 4's `decision.line` verbatim-duplicates a narrative line (*"I have something to tell you."*); act 3 outcomes teleport to `place_funeral_parlor` and an invalid `place_rice_ledger` while the scene is on the veranda; `char_kam` is a hallucinated character ID in act 4 (3 occurrences, gated as unknown).

**Pass/fail outcome equivalence — FAIL (new defect class).** Outcomes are now concrete and bound to the choice (real improvement), but pass and fail perform the *same action* with only a bystander's mood changed: *"I write 4:07 and the Appraiser pockets the deed."* vs *"I write 4:07 and the Boatman spits on the floor."*; *"I hand him the ledger and he writes nothing."* vs *"I hand him the ledger and he walks away."* Mechanically distinct lines, functionally identical events — failure never fails.

**Spine — REGRESSED.** The foregrounded place is never visited; the typical spine (veranda → foregrounded place → veranda) is broken. Iter1 at least traveled.

**Length — PASS.** Narrative lines per act: 11 / 12 / 11 / 8 — inside 8–12.

---

## (b) Pass-1 defect list: status

| # | Defect (pass 1) | Status | Evidence |
|---|---|---|---|
| 1 | Outcomes generic stock phrases | **FIXED (with new caveat)** | Outcomes now concrete and object-bound (*"I file the correction and the Timekeeper bows, hand over heart."*). New caveat: pass/fail perform the same action (see above). |
| 2 | Zero Thai | **UNCHANGED in shipped output** | Assignment machinery exists; model paraphrased/dropped 6–8 phrases; all misses recorded; episode shipped with 0 Thai. |
| 3 | like/as-if flood | **FIXED** | 0 similes in prose and JSON (was 7+). |
| 4 | Stakes never stated | **IMPROVED** | Stakes spoken in act 1 prose and partially shipped (land audit); but the explicit STAKES line was dropped by the formatter, and the inheritance motive (monk's nephew) only lands in act 3. |
| 5 | No introductions / budget blown | **IMPROVED** | Entrances now carry concrete descriptions (salt-crusted shirt, pink chit, soot). But the `PRESENT:` grammar leaked into the JSON as roster recitations, and act 1 segment 1 still has 4 speakers. |
| 6 | Temporal inversion | **FIXED** | No reaction-before-cause instances found. New minor non-sequiturs from jammed tag anchors (*"I'm not finished yet"* answering *"I have something to tell you"*). |
| 7 | Refrain failure | **UNCHANGED** | Still no refrain; *"Time burns. But paper lies."* occurs once only. |
| 8 | Choices reference unestablished facts | **IMPROVED** | Gate now catches these (boatman testimony w/ absent boatman recorded). Shipped act-3 outcomes still reference invalid places; the plan gate's own catches were not enforced. |
| 9 | Telling captions | **IMPROVED** | Image-captions gone with the similes; replaced by first-person interiority captions (*"I feel the weight of his words, but the doubt stays."*). |
| 10 | Spatial bookkeeping | **IMPROVED** | Entrances explicit; no act-boundary teleports in narrative. But outcomes teleport (parlor, invalid rice_ledger, river_post). |
| 11 | Key handoff denatured | **IMPROVED** | Key slide + *"Time is."* + riverbank walk restore the private plan's staging; still missing the "open it when the king dies" charge. |
| 12 | PC uncharacterized | **IMPROVED** | PC now has interiority and a want (the tin box, the class to teach) — but generic, and the best beat was dropped from the JSON. |
| 13 | Format stage regenerating | **UNCHANGED/WORSE** | 15 transcription-diff hits; hallucinated `char_kam`; roster lines shipped; STAKES line dropped; act-4 decision.line duplicated from narrative. The transcription gate *sees* all of this and ships it. |

**Score: 2 fixed, 7 improved, 3 unchanged, 1 unchanged/worse — plus two new defect classes (first-person narrator; pass=fail outcomes) and one arc regression (fire as backstory).**

---

## (c) Systemic vs one-off

**Systemic:** first-person narrator (prose prompt evidently instructs or permits first-person — every line, both stages); PRESENT-line leakage (plan grammar not fenced from page text); pass=fail outcome equivalence (the plan gate checks word-overlap, not action divergence); Thai non-compliance (two runs, same failure — the model will not place these phrases under current prompting); choice word-count (never satisfied in two iterations — the constraint is not landing at all); formatter invention/dropping (recurs across iterations); fire-as-backstory (planner ordering: the climactic event placed before the dispute).

**One-off:** `char_kam` hallucination (stochastic ID drift, though an allow-list check would kill it class-wide); the ellipsis fragment (stochastic, but a fragment/ellipsis lint would catch the class).

## Gate adequacy for bulk generation

The gate *detection* is now genuinely good (transcription diff, place allow-list, Thai placement, unknown characters). Two structural gaps remain:
1. **Gates record but never block or retry.** A 58-failure episode "COMPLETED". At 168 episodes this guarantees shipping broken pedagogical content (0 Thai) and schema-adjacent errors (unknown character IDs, invalid places) that the frontend may not survive.
2. **Detection blind spots:** no check for first-person narrator lines; no check for `PRESENT:`/roster lines as dialogue; no check that pass and fail outcomes diverge in action; no fragment/ellipsis lint; no check that `decision.line` isn't a duplicate of a narrative line; no refrain-presence check.

---

## (d) My three criteria — iter2 scores (iter1 in parentheses)

1. **Stakes legibility: 3/5 (was 2/5).** Time dispute + audit deadline clear in act 1; the "why" (inheritance) deferred to act 3; the explicit stakes line dropped in formatting.
2. **Choice–outcome consequentiality: 3/5 (was 1/5).** Outcomes now dramatize the chosen action with named objects — but pass and fail are the same event with different weather, so consequence is still not *differential*.
3. **Ensemble choreography: 3/5 (was 2/5).** Entrances are now introduced and concrete; but roster recitations ship as dialogue, outcomes teleport to off-scene/invalid places, and a hallucinated character ID appears in act 4.

---

## Bottom line

**Not ready for bulk generation.** Two iterations in, the pipeline has never once shipped Thai text (the product's core function), never satisfied the 10–20-word choice rule, and now ships a POV violation that breaks the narration contract in every act — all under gates that see most of it and wave it through. At $0.006/episode the cost is not the issue; the issue is that bulk mode would manufacture 168 recorded failures.

**Top 3 remaining fixes, in order:**
1. **Make gates blocking with bounded retry (at minimum for: Thai phrase placement, unknown character IDs, invalid places, choice word counts).** Detection without enforcement is a log, not a gate. These four checks are deterministic and cheap; retry only on their failure.
2. **Fix the POV regression at the prose prompt:** narration is third-person `char_narrator`; the PC's interiority belongs in `char_pricha` dialogue or is cut. Add a first-person-pronoun lint on narrator lines (the current gate set cannot see this at all). Fence plan grammar (`PRESENT:`, `ENTRANCE:`) so it can never reach the page.
3. **Decision quality:** require pass and fail outcomes to diverge in the *action* (fail = the action fails or costs), require `decision.line` to be a fresh line, and stop choices/outcomes from referencing off-stage places and characters. This is the difference between a game and a slideshow.

## Headwinds / tailwinds

**Tailwinds:** The procedural approach demonstrably works when the constraint is machine-enforced upstream: similes went from 7+ to 0 in one iteration by rejecting them in the *plan*. Outcomes are unrecognizably better (concrete, object-bound). Entrances now have bodies and wants. The transcription-diff and place/character allow-list gates are exactly the right instruments — they caught everything; they just don't have authority. The key/riverbank ending proves private-plan fidelity is achievable.

**Headwinds:** The pattern of fixes is whack-a-mole: each procedural patch (simile ban, PRESENT grammar, STAKES beat) creates a new leak (noun-phrase texture lost, roster lines shipped, stakes line dropped by the formatter). The model's non-compliance on Thai phrases and choice word counts has survived two prompt revisions — these may need structural solutions (post-insertion of Thai by code; programmatic choice-description expansion) rather than better prompting. The formatter remains the least trustworthy stage: it dropped the two best lines in the episode and invented a character. And the fire-as-backstory reordering shows the planner has no urgency-ordering constraint — expect flat or inverted arcs at bulk until one exists.
