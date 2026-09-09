# EDITOR FEEDBACK — ep_005 "The Declaration" (sprint 2, pass 2)

Headline: the mechanical floor is now real. Segments in contract in all 4 acts, costed stakes in act 1, PC acts in every act, zero decision.line duplications, Thai in all 8 slots, one residual format error. The remaining defects are literary and concentrated in exactly the places no detector exists: Thai pretext quality (still ~half orphan), a new compression artifact (run-on narrator lines crammed to fit the line budget), and wooden either/or dilemma lines.

---

## (a) Verdict per rubric area

### 1. Common-sense fiction guidelines

**Show don't tell — IMPROVED.** Act 1 opens with three grounded tableaux (*"kneeling on the worn floorboards with the school's tin document box open before him"*; *"Phra Kam sits perfectly still in faded robes by the pond's edge… a small black notebook beside him"*). Residual tells: *"his determined expression unchanged"*; *"acknowledging the regulation"* — both at tag slots.

**Does the story make sense — YES, first episode to fully pass.** Officer's ultimatum with cost and deadline in line 4 (*"Produce the monk's temple papers within three days, or the fine will be levied on this school."*); the search logic (chests → pawnshop → registry office) is pipe-flow; act 4's dodge (declare the monk a ward of the veranda) is a believable canal-bureaucracy move. One confusion: act 2 segment 2 line 1 repeats segment 1's staging near-verbatim (*"At the pawnshop landing, The Pawnshop Appraiser is weighing a bundle of red-stringed gold."* vs seg 1's *"weighing a bundle of gold tied with red string"*) — a rule-27 near-duplicate no gate caught.

**New compression artifact — run-on beat-cramming.** Act 3 segment 2 line 1: *"The Grain Clerk says monks are registered by the Sangha, not the tax office, and the Tax Clerk adds that for a fine, a name can be entered into the residence book, as he slides the heavy ledger toward Lek, open to a column of thumbprints, and The District Officer enters and stands behind him."* — four beats welded into one sentence to satisfy the line budget. Same at act 4 segment 2 line 1 (three beats: Lek's argument, the officer's laugh, the spoon). The line-count contract is being met by cramming, not by writing to budget. Also note: this run-on contains a "not X but Y" (*"registered by the Sangha, not the tax office"* — rule 22).

**Length — PASS.** 10 / 12 / 11 / 10 narrative lines — inside 8–12 for the first time.

### 2. Dialectical-fiction skill

**Desire as practice/inventory/attention — PASS.** Phra Kam's practice is the episode's spine: the small black notebook (*"writes a single word with a charcoal pencil, then closes it"*), the rusted spoon produced from his robe at exactly the moment his right to eat is questioned. The spoon is the tin-box standard — want shown as inventory, never explained. Best desire-work of any episode so far.

**Thesis machinery — THIN but present.** *"If there is no paper, there is no person for the ledger"* is a genuine thesis-adjacent line (personhood as registry entry), and the thumbprint column extends it. No sustained noun-phrase work; no soft magical realism.

**Wonder beats — PARTIAL.** The red stamp *"bleeding into the old wood"* of the cracked pillar; the ledger *"open to a column of thumbprints"*; the spoon held flat on the palm. Act 2 is bare. No elegiac frame.

**Four-act arc / act 4 transforms — PASS (best arc so far).** The problem (no papers → no person) is transformed, not solved: Lek's declaration reframes membership as hospitality rather than documentation, the officer laughs at it, and then the spoon answers the laugh — *"The District Officer shakes his head at the spoon, turns, and walks down the steps without another word."* The declaration's validity is left untested; nobody wins. This is the first act 4 that both transforms and withholds tidy-up.

**Characters as contradictions — PASS (first).** Phra Kam: the man with no papers who carries the only two objects that prove him — a notebook he won't open and a spoon. The officer: enforcing personhood-by-ledger while recognizing the regulation's absurdity (he nods along with the clerk, then laughs, then leaves). Wan watches from doorways and says things that don't fit — not a contradiction, just underwritten.

**Refrain — ABSENT (fourth episode running).** Notebook and spoon recur as objects; no verbal refrain with changing meaning exists. This is now the longest-standing unaddressed skill requirement.

**Fatalism — ABSENT.** No cosmic register; the episode is a bureaucratic parable. Acceptable singly, but the skill asks for it.

**Moral ambiguity — PASS.** Both impulses live: the officer's regulation is real (he nods in agreement, acts within it) and Lek's declaration is a legal fiction — a good-hearted forgery. The story argues for neither.

**Anti-AI discipline — ONE CLASS VIOLATION.** The run-on lines contain "not X but Y"; otherwise clean. Em-dashes controlled.

### 3. Game requirements

**Segments / counts — PASS.** [6,2,2] [6,3,3] [6,3,2] [4,3,3]; no empty segments; the FATAL backstop works.

**Thai / tags — MIXED (my judgment, since no detector exists).** Placement mechanics perfect. Pretext quality: **4 of 8 land, 4 of 8 orphan.**
- GOOD: Grain Clerk's *"อยู่จังหวัดอะไร"* ("which province?") — exactly what a registration clerk asks; Lek's hesitation (*"unable to name a province"*) is a true dramatic reaction. Appraiser's *"ไม่เคย"* ("never") — a direct answer to Lek's "Have you ever…?" Wan's *"มีอะไรเข้าตา"* ("something in my eye") — motivated by the slanting light. Boatman's *"ไม่ไปไหนเหรอ"* — passable as a prod at the stalled search.
- ORPHAN: Wan's *"ชอบสุดๆ"* ("love it!") — she has been established as "watching silently" from a shadow; bursting out with this after an ultimatum is character-breaking. Appraiser's *"มีขายที่"* — a fragment with no dramatic meaning. Tax Clerk's *"ทุกคนรู้จักมัน"* ("everyone knows it") — refers to nothing. Boatman's *"ขอไม้จิ้มฟันหน่อย"* ("toothpick, please") — inserted into the episode's climax (the spoon beat), actively damaging the best moment in the episode.
Root cause is selection-side: `assign_thai_phrases()` picks phrases deterministically with no regard for whether the episode's situations can stage them. "Toothpick please" cannot be dramatized in a registration-crisis episode. No writing-side fix will solve this; the assignment step needs a semantic-fit filter (or the plan needs license to reorder/swap tags across acts to find the fittable slots).

**Gloss-tells — IMPROVED, not eliminated.** Most post-Thai lines are now genuine reactions (hesitation, blinking, head-shake). Residuals: *"his determined expression unchanged"*, *"acknowledging the regulation"*.

**Decisions — PASS with one voice defect.** Fresh dilemma lines (duplication: zero). Choices 10–20 words, concrete, staged. Outcomes divergent and costly (*"I am told the school's stamp holds no authority for residence."*). BUT all four dilemma lines are telegraphic either/or UI-prompts voiced by characters: *"Produce the papers or face the fine."*, *"Find proof of identity or find something of value."*, *"Enter a name in the ledger or leave it blank."*, and worst, Phra Kam — established across four acts as near-silent — *"Accept the declaration or refuse it."* The duplication fix was satisfied by making characters speak game-menu text. A dilemma line should be a line the character would say that poses the choice.

**Outcomes — PASS.** One residual voice error (act 2 easy fail: *"The appraiser pushes the box back…"* — third person, gate-recorded).

**Introductions / budget — IMPROVED.** Everyone is introduced by appositive or action in the opening tableaux (Lek the teacher, Phra Kam, Wan, the Boatman, the officer). Act 1 segment 1 has narrator + officer + boatman speaking — technically over the "PC + one other" budget (Lek is silent in segment 1).

**Spine / travel — PASS.** Veranda → pawnshop → rice-ledger office → veranda, all explicit.

**Deadline convergence — PASS.** Three-day deadline planted act 1; act 3 the officer re-enters at the registry office demanding *"Have you found the papers?"* — pressure converges where it should.

**Subplot plant — PASS (apparently).** The notebook (one word written, closed; a line "about gratitude and place" read only in the hard outcome) and the spoon are concrete planted facets of Phra Kam's private material — visible, unexplained, promising.

---

## (b) Numbered defect list (severity order)

1. **Thai pretext failure at selection level: 4 of 8 orphan phrases, one damaging the climax.** Where: ชอบสุดๆ (act 1), มีขายที่ (act 2), ทุกคนรู้จักมัน (act 3), ขอไม้จิ้มฟันหน่อย (act 4, inside the spoon beat). Why: the phrases are assigned deterministically without semantic fit to the episode; the writer then has to stage the unstageable. This is the last pedagogical-quality defect and it is structural, not prompt-level.
2. **Run-on beat-cramming to satisfy the line budget.** Where: act 3 seg 2 line 1 (four beats), act 4 seg 2 line 1 (three beats). Why: the count contract is met by welding beats; produces the episode's worst sentences and smuggles in a banned "not X but Y". The budget needs to be enforced on the plan's beat count, not on post-hoc sentence merging.
3. **Dilemma lines are telegraphic game-menu text voiced by characters.** Where: all 4 decision.lines; worst: the near-silent Phra Kam "speaking" *"Accept the declaration or refuse it."* Why: the duplication fix removed the symptom and created a voice violation; the dilemma line needs to be dialogue that poses the choice in character.
4. **Refrain absent (4th episode).** No verbal refrain machinery has ever shipped. The skill mandates it; nothing in the plan steps creates one.
5. **Near-duplicate staging line.** Where: act 2 seg 1 line 1 vs seg 2 line 1 (red-stringed gold weighed twice). Why: rule 27; the duplicate scan evidently misses near-verbatim narration (it caught dialogue only).
6. **Minor:** act-1 segment-1 speaker budget technically exceeded (officer + boatman speak, Lek silent); act-3 easy choice has the never-lies PC fabricating a residence certificate; residual gloss-tells (2); one third-person outcome (gate-recorded).

---

## (c) Comparison vs ep_004 defect list

| # | ep_004 defect | Status | Evidence |
|---|---|---|---|
| 1 | Empty seg-5 ×4, seg-1 12–20 lines | **FIXED** | All segments in contract; FATAL backstop verified; lengths 10/12/11/10 |
| 2 | Thai orphan non-sequiturs (≥4/8) | **UNCHANGED (root cause relocated)** | Still 4/8 orphans; but now demonstrably a *selection* problem (unstageable phrases), not a placement problem |
| 3 | PC bystander | **FIXED** | Lek searches, questions, approaches counters, and authors the act-4 declaration himself |
| 4 | Stakes absent | **FIXED** | Costed ultimatum in act-1 line 4; FATAL backstop |
| 5 | decision.line duplicates ×4 | **FIXED → new voice defect** | 0 duplications; replaced by telegraphic menu-text (defect 3) |
| 6 | Gloss-tells | **IMPROVED** | Reactions mostly dramatic; 2 residuals |
| 7 | Foreground char unintroduced / budget | **IMPROVED** | All introduced in opening tableaux; budget technically still exceeded in seg 1 |
| 8 | Deadline planted, never used | **FIXED** | Officer converges in act 3 |
| 9 | Minor (not-X-but-Y, ladders, PC lies) | **IMPROVED** | Ladders varied; one "not X but Y" (inside a run-on); one PC-trait bend (fabricated certificate) |
| — | Subplot plant (noted absent in ep_004) | **FIXED** | Notebook + spoon planted, unexplained |

**Tally: 6 fixed, 3 improved, 1 unchanged. No regressions. Two new defect classes (run-on cramming; menu-voice dilemma lines), both side-effects of otherwise-correct fixes.**

## Systemic vs one-off

**Systemic:** Thai phrase/episode semantic mismatch (selection algorithm); run-on cramming (budget enforced at the wrong layer); menu-voice dilemma lines (the plan's DECISION beat shape invites it); missing refrain machinery (never been implemented in plan steps); near-duplicate narration scan gap.

**One-off:** the act-3 certificate forgery bending the PC's trait; the act-1 budget slip.

---

## (d) My three criteria (ep_004 scores in parentheses)

1. **Stakes legibility: 4/5 (2/5).** Cost, deadline, and owner all explicit by line 4; docked one because the fine's consequence for the school is asserted, never felt.
2. **Choice–outcome consequentiality: 4/5 (4/5).** Divergent, costly, staged; docked for the fabricated-certificate option sitting in the PC's never-lies trait.
3. **Ensemble choreography: 4/5 (3/5).** Everyone introduced, travel explicit, positions trackable; docked for the seg-1 budget slip and Wan's motivation-less interjections.

---

## Bottom line: bulk readiness

**Yes — conditionally ready.** The argument for proceeding: every remaining defect class is now quality-level, not validity-level. The JSON parses, segments are in contract with a FATAL backstop, Thai is present and placed, stakes/decisions/outcomes are structurally sound, and the episode is genuinely readable — ep_005 is the first output I would ship to a player without embarrassment. The two new defects (run-ons, menu-voice dilemmas) are instruction-level and can be fixed *during* bulk without invalidating already-generated episodes; the Thai-orphan problem is real but bounded (~half the tags land well, and the vocab list itself is the constraint).

**Do these three cheap things before/during bulk (none blocking):**
1. **Thai selection-side fit:** score candidate phrases against the episode's sticky situation/places before assignment (even a crude keyword/setting compatibility pass), or let the planner choose 8 from a larger shortlist. This converts the worst residual defect from ~50% orphan to whatever the shortlist allows.
2. **Dilemma-line voice:** require the DECISION dilemma beat to be written as in-character dialogue (the plan gate can check it isn't a bare "X or Y" imperative).
3. **Beat-count budgeting in the plan** (not sentence merging downstream): the plan gate should count beats per segment-range, so the writer never has to cram.

**Recommended spot-check regimen during bulk (168 episodes):**
- **First 5 episodes: full editorial review** (this rubric), to confirm no new systemic class appears at scale.
- **Thereafter 1-in-10 sampling** with a shortened checklist: (a) read only the 8 Thai lines + their following reaction lines — count orphans; (b) read the 4 decision.lines — flag menu-voice; (c) scan for run-on narrator lines (>2 clauses joined by "and"); (d) verify act-4 transformation vs the private plan's subplot. ~10 minutes per sampled episode.
- **Automated telemetry on all 168:** abort/FATAL rate, spot-edit invocation rate, keep-better-guard discards, format-gate residual counts. Tripwire: if any metric exceeds ~15% of episodes, pause and inspect — the guard and FATALs mean failures now abort cleanly rather than shipping, so the telemetry is trustworthy.
- **Track refrain absence** as a known debt: if the PO wants the skill fully honored, refrain machinery needs one dedicated plan step before episode ~50, not a retro-fix over 168.

## Headwinds / tailwinds

**Tailwinds:** The gate-with-authority pattern has now won every battle it was sent to: segments, stakes, PC-per-act, duplication, deadlines, subplot plant — six of nine ep_004 defects fixed in one pass, zero regressions. The keep-better guard makes spot-editing strictly safe, and FATALs convert bad output into clean aborts (the failure mode bulk generation needs). ep_005 contains the best material the pipeline has produced: the rusted spoon, the thumbprint column, "If there is no paper, there is no person for the ledger," and an act 4 that transforms without absolving. Cost ($0.014) is inside budget.

**Headwinds:** Every fix now generates its own side-effect at the quality layer (budget → cramming; duplication fix → menu-voice), which means the pipeline has entered the diminishing-returns zone where detectors don't exist and my review is the measurement — the spot-check regimen above is not optional. The Thai vocab list is the binding constraint on the pedagogical product: phrases like "toothpick please" and "love it!" will keep producing orphans until selection is semantic. The refrain — a core skill requirement — has never appeared in four episodes and has no plan machinery; it will not spontaneously appear. And v4-flash's reasoning-heavy spot-edits are 65% of episode cost; a cheaper editor model is the obvious optimization if $0.014 needs to come down.
