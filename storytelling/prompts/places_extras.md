# PROMPT TEMPLATE — 3 places + 3 extras for one recurring character (one API call)

SYSTEM: You are a literary worldbuilder in a research-driven dialectical style. Follow the checklist exactly. Output ONLY the requested artifacts.

USER:
You are creating THREE places and THREE extras (generic background NPCs) for a Thai-language educational RPG, all belonging to ONE recurring character's orbit.

## Setting
A canal-side village/temple world in Siam, ~1910s–1950s. The temple school veranda is the party's hub (it already exists — do not recreate it). Places are GENERIC ("The Pawnshop", never "Krungthep"). The world is never explained to the player; each place reveals ONE aspect of the world through what is superficially there.

## The recurring character these places belong to
{{CHARACTER_JSON_AND_PRIVATE}}

## Their dialectic
{{DIALECTIC_ID}} — {{DIALECTIC_NAME}}. Thesis: {{DIALECTIC_THESIS}}. Implications: {{DIALECTIC_IMPLICATIONS}}

## Requirements — 3 places
Each place: reveals one institution or action that is a tight if/then implication of the thesis, unique to that place; loosely inspired by real research, no fantasy-RPG clichés; 3-5 named spatial spots within it (for scene tracking — the party must be able to move between named spots); 2-3 episode hooks; one dialectical noun phrase for the place or something in it. The three places must be distinct in function (e.g. work / exchange / ceremony) and must be places this character plausibly returns to. Do NOT duplicate existing places: {{EXISTING_PLACES}}.

## Requirements — 3 extras (one per place)
Generic types, not named individuals (good: "The Appraiser"; bad: "Nanda"). Each extra's dialectical phrases must be LOGICAL IMPLICATIONS OF THE RECURRING CHARACTER'S CONTRADICTION — a smaller, generic instance of the same shape, never a duplicate. Each: a function the party repeatedly needs; 2-3 episode hooks (at least one that can intersect the recurring character's secret WITHOUT the extra knowing it); three dialectical noun phrases; voice notes.

## Checklist (ALL items mandatory — especially: institutions as if/then implications; desire as practice/inventory/attention; every character a contradiction; no info dumps)
{{SKILL_CHECKLIST}}

## Output format — exactly six artifacts, separated by lines containing only `===FILE n===`
For each place p (n=1..3): FILE (2n-1) = JSON: {"id": "place_<snake>", "name": "The ...", "picture": "/places/<snake>.png", "description": "<public, 2-4 sentences, surface detail only>"}
FILE (2n) = Markdown private plans: dialectic; the revealed thing and why it is an if/then of the thesis; episode hooks; noun phrase; spatial spots.
Then three more pairs (FILES 7-12) for the extras: JSON {"id": "char_<snake>", "name": "The ...", "picture": "/characters/<snake>.png", "type": "npc", "description": "<public, 2-4 sentences>"} and Markdown: the if/then implication of the recurring character's contradiction they embody; recurring function; hooks; three noun phrases; voice notes.
