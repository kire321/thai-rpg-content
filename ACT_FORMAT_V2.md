# Act Format V2 Specification

## Overview

The new act format generalizes the episode structure to support a variable number of tag/vocab quizzes per act. This enables richer pacing (narrative → quiz → narrative → quiz → decision) while remaining backward-compatible with the old format.

## Old Format (lines_before / tag / lines_after)

```typescript
interface OldAct {
  id: string;           // e.g., "act_001"
  title: string;        // e.g., "The Market Confrontation"
  lines_before: Line[]; // narrative lines before the tag quiz
  tag: string;          // e.g., "tag_001" - single tag ID
  lines_after: Line[];  // narrative lines after the tag quiz
  decision: Decision;   // 3 choices with outcomes
}
```

## New Format V2 (segments array)

```typescript
interface NarrativeSegment {
  type: "narrative";
  lines: Line[];
}

interface TagSegment {
  type: "tag";
  tag: string;          // tag/vocab ID, e.g., "tag_042"
}

type Segment = NarrativeSegment | TagSegment;

interface NewAct {
  id: string;
  title: string;
  segments: Segment[];  // ordered array of narrative + tag segments
  decision: Decision;
}
```

## Example Act with 2 Tags

```json
{
  "id": "act_001",
  "title": "The Whispering Garden",
  "segments": [
    {
      "type": "narrative",
      "lines": [
        { "text": "Bussaba leads you through rows of crystal-blooming flowers.", "character": "char_narrator" },
        { "text": "Each blossom hums at a different frequency.", "character": "char_narrator" }
      ]
    },
    {
      "type": "tag",
      "tag": "tag_042"
    },
    {
      "type": "narrative",
      "lines": [
        { "text": "She touches a purple bloom and it sings a greeting.", "character": "char_narrator" },
        { "text": "Welcome to my garden, travelers.", "character": "char_bussaba" }
      ]
    },
    {
      "type": "tag",
      "tag": "tag_017"
    },
    {
      "type": "narrative",
      "lines": [
        { "text": "The flowers nearest you begin to dim.", "character": "char_narrator" },
        { "text": "Something is wrong with the lattice here.", "character": "char_chanida" }
      ]
    }
  ],
  "decision": {
    "prompt": "What do you do?",
    "choices": [
      { "text": "Investigate the dimming flowers", "outcome": "pass", "next": "act_002" },
      { "text": "Ask Bussaba about the resonance", "outcome": "pass", "next": "act_002" },
      { "text": "Ignore it and move on", "outcome": "fail", "next": "act_003" }
    ]
  }
}
```

## Frontend Rendering Strategy

The EpisodeDetail page uses a `normalizeAct()` helper to render both formats uniformly:

```typescript
// Helper: Detect old vs new format
function isOldAct(act: Act): act is OldAct {
  return 'lines_before' in act && 'tag' in act && 'lines_after' in act;
}

// Helper: Normalize act to render segments
type RenderSegment =
  | { kind: 'narrative'; lines: Line[] }
  | { kind: 'tag'; tag: string };

function normalizeAct(act: Act): RenderSegment[] {
  if (isOldAct(act)) {
    return [
      { kind: 'narrative', lines: act.lines_before },
      { kind: 'tag', tag: act.tag },
      { kind: 'narrative', lines: act.lines_after },
    ];
  }
  return act.segments.map((seg) => {
    if (seg.type === 'narrative') {
      return { kind: 'narrative' as const, lines: seg.lines };
    }
    return { kind: 'tag' as const, tag: seg.tag };
  });
}
```

## Episode Identification

- Episodes using the new format should be numbered starting from `ep_341` (after the existing 340 episodes)
- New episodes have `id`, `title`, `acts[]` structure identical to old episodes
- The act format is detected at render time by checking for the `segments` property

## Tag Distribution for New Episodes

Each new episode has 4 acts, each with 2 tags = 8 tags per episode.
170 episodes × 8 tags = 1,360 tag slots total.
The generation script uses a least-used-first algorithm to distribute tags evenly.
