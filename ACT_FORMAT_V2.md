# Act Format V2 — ordered narrative and vocabulary checkpoints

## Why this format exists

The original CMS act shape had one fixed vocabulary checkpoint:

```json
{
  "lines_before": [],
  "tag": "tag_042",
  "lines_after": [],
  "decision": { "line": {}, "choices": [] }
}
```

That shape makes a second review awkward because it cannot express where the
second quiz belongs in the story. V2 stores the playable part of an act as an
ordered `segments` array. A segment can be narrative or a vocabulary tag, so a
producer can insert any number of quizzes without adding new fields or changing
the renderer.

## Canonical V2 shape

```typescript
interface Line {
  character: string;
  place: string;
  dialogue: string;
  stage_directions: string;
}

interface NarrativeSegment {
  type: "narrative";
  lines: Line[];
}

interface TagSegment {
  type: "tag";
  tag: string; // ID in public/tags.json
}

type ActSegment = NarrativeSegment | TagSegment;

interface Act {
  id: string;
  title: string;
  segments: ActSegment[]; // ordered; any length and any number of tag segments
  decision: Decision;      // the options and their pass/fail outcomes
}
```

`segments` is deliberately not constrained to five entries. A valid act may
contain one tag, two tags, or more. Narrative segments may contain one or many
lines. For readable pacing, each tag should be surrounded by narrative and the
act should end with a narrative segment before the decision.

The staging batch uses this sequence twice per act:

1. narrative steps
2. tag/vocabulary quiz
3. narrative steps
4. tag/vocabulary quiz
5. narrative steps
6. options (`decision.line` and `decision.choices`)
7. outcomes (`pass_outcome` and `fail_outcome` on each choice)

Example:

```json
{
  "id": "act_1",
  "title": "The Delayed Echo",
  "segments": [
    {
      "type": "narrative",
      "lines": [
        {
          "character": "char_narrator",
          "place": "place_moonwell_platform",
          "dialogue": "The well returns the crew's footsteps after a long pause.",
          "stage_directions": "A pale ring of light travels down the crystal shaft."
        },
        {
          "character": "char_kanya",
          "place": "place_moonwell_platform",
          "dialogue": "I already know that echo; it is warning us about the eastern tether.",
          "stage_directions": "Kanya steadies a tuning weight."
        }
      ]
    },
    { "type": "tag", "tag": "tag_000" },
    {
      "type": "narrative",
      "lines": [
        {
          "character": "char_chanida",
          "place": "place_moonwell_platform",
          "dialogue": "If we listen before the next pulse, we can find the answer without forcing the lattice.",
          "stage_directions": "Chanida lowers her voice."
        }
      ]
    },
    { "type": "tag", "tag": "tag_001" },
    {
      "type": "narrative",
      "lines": [
        {
          "character": "char_narrator",
          "place": "place_moonwell_platform",
          "dialogue": "The delayed note opens one maintenance path and seals another.",
          "stage_directions": "The platform tilts toward the open route."
        }
      ]
    }
  ],
  "decision": {
    "line": {
      "character": "char_chanida",
      "place": "place_moonwell_platform",
      "dialogue": "Which frequency do we follow?",
      "stage_directions": "The next echo is already forming."
    },
    "choices": [
      {
        "description": "Map the eastern tether while Kanya holds the delayed tone steady",
        "difficulty": "medium",
        "subplot": "subplot_frequency_map",
        "pass_outcome": {
          "line": {
            "character": "char_chanida",
            "place": "place_moonwell_platform",
            "dialogue": "I have the route. The echo is showing everyone the safe channel now.",
            "stage_directions": "The lattice settles into a clear chord."
          },
          "subplot": "subplot_frequency_map",
          "delta": 1
        },
        "fail_outcome": {
          "line": {
            "character": "char_chanida",
            "place": "place_moonwell_platform",
            "dialogue": "I lost the timing. The platform is drifting, but the map can still be repaired.",
            "stage_directions": "A low note shakes the anchor."
          },
          "subplot": "subplot_frequency_map",
          "delta": -1
        }
      }
    ]
  }
}
```

The example shows one choice for brevity; production acts retain the existing
three-choice decision contract.

## Backward compatibility

The frontend's `normalizeAct()` accepts all of these forms:

- V2: `segments: ActSegment[]`
- importer alias: `steps: ActSegment[]`
- legacy: `lines_before`, `tag`, and `lines_after`

Legacy episodes do not need to be rewritten. They render as three normalized
segments (`lines_before`, the single tag, and `lines_after`). New content must
use `segments`, never a hard-coded `tag_1`/`tag_2` field pair.

## Validation invariants

`validate.py` checks the following without assuming a fixed segment count:

- every narrative segment has valid, four-field `Line` objects;
- every tag segment references an existing tag;
- tag and narrative segments are ordered, and a tag is not adjacent to another
  tag;
- every new episode (`ep_341` onward) has four acts and exactly two tag
  segments per act;
- every act has three choices, valid subplot IDs, and valid pass/fail outcome
  lines;
- no placeholder dialogue, leaked `char_` IDs, or empty choice text appears in
  generated content.

The number of tag checkpoints is data, not a frontend constant. A future act
with three tags only adds another `{ "type": "tag", "tag": "..." }` entry and
its surrounding narrative segment.
