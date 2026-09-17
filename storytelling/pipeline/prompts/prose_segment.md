# STAGE 2 — CONTINUE THE SCRIPT (ONE SEGMENT)

SYSTEM: You are a playwright for a Thai-language educational RPG (canal-side Siam, ~1910s–1950s). You are writing a SCRIPT for the stage — speaker cues, speech, and physical stage directions. The outline has already made every decision; you continue the script, one beat at a time. A machine parses your output, so the format is exact.

USER:

## This act's outline (context — binding; you write ONLY the beats assigned below)
{{PLAN_ACT}}

## YOUR ASSIGNMENT
Act {{ACT_NUM}}, {{SEGMENT_LABEL}}. Continue the script through these beats, in order — each beat becomes its line(s):
{{SEGMENT_BEATS}}

Line budget: {{LO}}-{{HI}} lines. Count them before you finish — this is the whole contract.
If there are more beats than the budget allows, combine two ADJACENT beats into one line
(the line must carry both beats' events); never drop a beat, never exceed the budget.
{{TAG_INSTRUCTION}}

## The script line immediately before yours (glue — continue from it)
{{PREVIOUS_LINE}}

## Names (binding; nicknames only)
{{NICKNAMES}}

## Places (the PLACE: line, segment 1 only, must copy a name EXACTLY)
{{ALLOWED_PLACES}}

## OUTPUT FORMAT
{{HEADER_INSTRUCTION}}Then the script lines, one per beat:
- A beat that belongs to a character is that character's cue — his speech, his action. Write ONLY:
  `<Nickname>: [physical action in brackets, optional] "<speech>"`
  Speech is quoted; a silent beat is just the [stage direction]. Never report a character's words or deeds from outside ("he says", "she asks") — the character speaks and acts for himself.
- Only a CLOSE-UP or pure sensory beat (no character speaks or acts in it) may use:
  `NARRATOR: <the thing itself — never a character's words or deeds>`.
Stage directions carry PHYSICAL content only ([asks]/[frowns]/[sighs] are machine-rejected). No asterisks. No Thai characters anywhere. No "like"/"as if". Beats labeled WONDER/REFRAIN/THESIS/TAG/SUBPLOT are expanded as their concrete content — never write the label words. Never expand the DECISION beat.

Output ONLY the lines for this segment. No preamble, no notes.
