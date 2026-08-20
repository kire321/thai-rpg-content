# PROMPT TEMPLATE — one recurring character (fill {{SLOTS}}, send to chosen model as one call)

SYSTEM: You are a literary fiction writer working in a research-driven dialectical style. You follow the provided checklist exactly. You output ONLY the requested artifacts, no commentary.

USER:
You are creating ONE recurring party member for a Thai-language educational RPG, cast in the mold of the crew in "Firefly": one of six recurring characters who are all regularly present, with one foregrounded per episode.

## Setting
A canal-side village/temple world in Siam, ~1910s–1950s. The temple school veranda by the pond is the village's scribe-hub: villagers bring letters to be read and written, money to be held, ceremonies to be arranged, disputes to be witnessed. The player character (PC) is Pricha ("Lek"), the temple-school teacher and clerk. The party recurs because every matter in the canal world lands on the veranda; episodes are things brought to the veranda, and the party is who happens to be sitting on it.

## The six dialectics (this character owns {{DIALECTIC_ID}})
{{DIALECTIC_TABLE}}

## Your assignment
- Dialectic: {{DIALECTIC_ID}} — {{DIALECTIC_NAME}}. Thesis: {{DIALECTIC_THESIS}}
- Its implications: {{DIALECTIC_IMPLICATIONS}}
- Real-life anchor (research): {{ANCHOR}}
- Existing characters you must NOT duplicate and SHOULD interconnect with: {{EXISTING_CAST}}

## Requirements
1. A misfit whose failure in this setting exposes the dialectic's thesis. Inspired by (never copied from) the real anchor; lightly fictionalized; psychologically realistic. Plausibly present on the veranda episode after episode.
2. Ironic double nature — ONE body containing BOTH poles of the dialectical contradiction (Case: a hacker who can't access the matrix; the Garuda: a flyer who can't fly).
3. Three subplots: each reveals backstory tying into relations with OTHER recurring characters, reveals personality, affects the ongoing mission, and ends on a character-defining decision for the PC.
4. Three dialectical noun phrases (object from the character's domain + descriptor from the thesis domain, applied directly — no "like"/"as if").
5. A universal DRIVE under the concrete goal, plus how the desire shows as practice / inventory / attention.
6. Voice notes.

## Checklist (ALL items mandatory)
{{SKILL_CHECKLIST}}

## Output format — exactly these two artifacts, separated by a line containing only `===FILE 2===`

FILE 1 — JSON (public, shown to player; no spoilers, no thesis vocabulary; 2-4 sentence description of what is superficially obvious):
{"id": "char_<snake>", "name": "...", "picture": "/characters/<snake>.png", "type": "party", "description": "..."}

FILE 2 — Markdown (private narrative plans, episode-writers only): research anchor & what was kept/changed; drive under the goal + the one-line irony; practice/inventory/attention channels; three noun phrases; three subplots (each structured: situation / backstory revealed / personality revealed / effect on mission / the PC's decision, 120-180 words each); voice notes; how this character typically behaves when NOT foregrounded (2-3 lines — what they do at the edge of someone else's episode).
