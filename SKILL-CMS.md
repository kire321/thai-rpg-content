# Thai RPG CMS — Content Agent Skill

> **SELF-UPDATE RULE:** Update this file before finishing every content task. Record
> new invariants, workflow changes, and bugs; remove stale instructions.
>
> **SECRETS RULE:** Never commit, print, or publish API keys, tokens, or other
> credentials. Read them from the environment or a local secret store at
> runtime. If a credential is found in a file, remove it from the working tree
> before publishing and treat it as compromised.

## Project

Chantara is a Thai language-learning RPG set in a world of floating skycities
and a crystalline lattice that reacts to sound. This repository is the static
CMS: JSON catalogs are under `public/`, and the React editor is under `src/`.

- CMS repository: `https://github.com/kire321/thai-rpg-content`
- Game repository (reference only): `https://github.com/kire321/thai-rpg`
- Publisher repository: `https://github.com/kire321/kire321.github.io`

## Current catalog (staging)

| Type | File | Count | Notes |
|---|---|---:|---|
| Episodes | `public/episodes.json` | 510 | 340 legacy + 170 V2 staging episodes |
| Tags | `public/tags.json` | 340 | Each links to 5–10 vocabulary items |
| Vocabulary | `public/vocab_items.json` | 340 | Thai, phonetics, English, and reverse tag links |
| Characters | `public/characters.json` | 30 | 4 party, 15 legacy NPC/narrator records, 10 new NPCs |
| Places | `public/places.json` | 30 | 20 legacy + 10 new acoustically distinct locations |
| Subplots | `public/subplots.json` | 5 | Recurring story threads |

The ten staging NPCs are `char_kanya`, `char_wichai`, `char_maliwan`,
`char_jintana`, `char_sakchai`, `char_pailin`, `char_rung`, `char_nop`,
`char_chaiyo`, and `char_lalida`. The ten staging places use the
`place_moonwell_platform`, `place_iron_kite_docks`, `place_singing_rice_terraces`,
`place_undertone_bazaar`, `place_lattice_fisheries`, `place_bellflower_observatory`,
`place_broken_tether_field`, `place_echo_cistern`, `place_cloudstep_village`, and
`place_resonant_greenhouse` IDs. Each has a picture in `public/characters/` or
`public/places/`.

## Episode and act format

Every episode has exactly four acts. Legacy acts remain supported:

```json
{
  "lines_before": [],
  "tag": "tag_042",
  "lines_after": [],
  "decision": { "line": {}, "choices": [] }
}
```

New acts use an ordered, extensible list:

```json
{
  "id": "act_1",
  "title": "The Delayed Echo",
  "segments": [
    { "type": "narrative", "lines": [] },
    { "type": "tag", "tag": "tag_042" },
    { "type": "narrative", "lines": [] },
    { "type": "tag", "tag": "tag_043" },
    { "type": "narrative", "lines": [] }
  ],
  "decision": { "line": {}, "choices": [] }
}
```

`segments` is an ordered array, not a five-field template. It may contain any
number of `narrative` and `tag` segments; a tag should be surrounded by
narrative. The frontend also accepts `steps` as an importer alias. `decision`
is the options step, and each choice's `pass_outcome`/`fail_outcome` is its
outcome step. See `ACT_FORMAT_V2.md` and `src/types/content.ts` for the full
contract.

The 170 new episodes (`ep_341`–`ep_510`) intentionally have exactly two tag
segments per act and 48 narrative lines per episode. Each tag's vocabulary
phrase is spoken immediately before its checkpoint, so the quiz is story-linked
rather than an unrelated review interruption.

## Generation

`generate_episodes_v3.py` is the canonical generator. It is OpenRouter-first:

- URL: `https://openrouter.ai/api/v1/chat/completions`
- Default model: `deepseek/deepseek-chat-v3-0324`
- Fallback model: `deepseek/deepseek-chat`
- Runtime key: `OPENROUTER_API_KEY` (never put it in source)
- `HTTP-Referer`: `https://github.com/kire321/thai-rpg-content`
- Temperature: `1.0`; episode `max_tokens`: `16000`

The prompt assigns exact tags, NPCs, places, and the V2 schema. API responses are
sanitized and rejected unless they have four acts, the assigned two tags per
act, three choices, valid IDs, and usable narrative. `generate_episodes_v2.py`
and `generate_episodes.py` are compatibility entry points.

For offline review/CI, run:

```bash
python generate_episodes_v3.py --offline --count 170
```

The deterministic fallback is deliberately complete, not a placeholder: it
keeps the same pacing, quotes each assigned vocabulary phrase, and balances
catalog references. A real OpenRouter key can be supplied later to regenerate
new batches without changing the schema.

## Validation and build

Run from the repository root:

```bash
python validate.py
npm ci
npm run build
```

`validate.py` checks legacy and V2 acts, arbitrary segment lengths, tag
references, narrative/tag ordering, two tags per new act, line/entity IDs,
choices/outcomes, pictures, catalog counts, episode IDs, and tag distribution.
The current complete catalog has 2,720 tag uses with a 7–9 usage range (legacy
history is not rewritten just to force an artificial exact four-use count).

Targeted frontend lint is:

```bash
npx eslint src/pages/EpisodeDetail.tsx src/pages/Episodes.tsx src/pages/Characters.tsx \
  src/pages/Places.tsx src/pages/Tags.tsx src/pages/VocabItems.tsx \
  src/pages/Subplots.tsx src/lib/cms.ts
```

The repository's generated UI primitives retain pre-existing full-lint warnings;
`npm run build` is the release gate.

## Branch and publishing workflow

- `master` is the canonical production source and remains at the 340-episode
  release until the user explicitly approves promotion.
- `510_episodes` is an archived earlier expansion; do not delete it.
- `staging` is the branch for this 30-character/30-place, 510-episode preview.
- Use GitHub's REST Git Trees API for a single multi-file commit when the shell
  Git transport has TLS/HTTP2 problems. Keep credentials in process memory only.

The publisher normally mirrors `thai-rpg-content@master` to:

- CMS data: `https://kire321.github.io/cms/`
- CMS UI: `https://kire321.github.io/cms-ui/`

For staging previews, build with `VITE_CMS_BASE=.` and publish the complete
`dist/` tree to the `staging-preview` branch. `staging-preview` is reset to the
current `staging` source commit before the built files are overlaid, so the
preview has traceable source ancestry. The live preview is served through
RawGitHack at:

`https://raw.githack.com/kire321/thai-rpg-content/staging-preview/index.html`

An immutable URL can use the `staging-preview` commit SHA on
`https://rawcdn.githack.com/`. Verify the HTML, JS bundle, `episodes.json`, and a
new image independently after every publish. The current fine-grained PAT is
content-only in practice: GitHub rejects workflow-file writes, Actions
workflow dispatches, Publisher-repository writes, and Pages configuration with
HTTP 403. Do not spend time retrying those endpoints without a replacement PAT
that explicitly grants Workflows, Actions, and Pages write permissions. The
RawGitHack preview leaves the publisher's production `/cms/` and `/cms-ui/`
paths untouched.

## Content quality rules

- Choices are concrete, action-oriented, and specific to the current scene.
- Pass/fail outcomes speak in first person and describe one concrete result.
- Narrative does not use superposition (“either X or Y”); alternatives belong
  in choices.
- Use only catalog IDs in JSON fields; never leak IDs into dialogue.
- New episodes must use both old and new NPCs/places over the batch. The
  generator's schedule keeps per-entity reference counts close while ensuring
  every new entity appears.
- Keep `stage_directions` a string and line objects limited to the four schema
  fields.

## Agent checklist

1. Read this file and inspect the current JSON/catalog state.
2. Make the smallest maintainable code/data change.
3. Run `python validate.py` and `npm run build`.
4. Review generated samples and distribution statistics.
5. Push a verified change to `staging`, never `master` without approval.
6. Build/publish `staging-preview` and verify the RawGitHack preview.
7. Update this file with anything learned before replying.
