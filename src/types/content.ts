export interface Line {
  character: string
  place: string
  dialogue: string
  stage_directions: string
}

export interface ChoiceOutcome {
  line: Line
  subplot: string
  delta: number
}

export interface Choice {
  description: string
  difficulty: 'easy' | 'medium' | 'hard' | string
  subplot: string
  pass_outcome: ChoiceOutcome
  fail_outcome: ChoiceOutcome
}

export interface Decision {
  line: Line
  choices: Choice[]
}

/** A run of dialogue/stage direction in an act. */
export interface NarrativeSegment {
  type: 'narrative'
  lines: Line[]
}

/** A vocabulary checkpoint. The frontend resolves the tag to its quiz items. */
export interface TagSegment {
  type: 'tag'
  tag: string
}

/**
 * Act content is intentionally an open ordered list rather than a fixed set of
 * fields. A producer may insert any number of tag checkpoints between
 * narrative segments while the decision remains the act's final interaction.
 */
export type ActSegment = NarrativeSegment | TagSegment

export interface LegacyAct {
  id: string
  title: string
  lines_before: Line[]
  tag: string
  lines_after: Line[]
  decision: Decision
}

export interface SegmentedAct {
  id: string
  title: string
  segments: ActSegment[]
  decision: Decision
}

/** Optional alias accepted by importers that call the ordered list `steps`. */
export interface SteppedAct {
  id: string
  title: string
  steps: ActSegment[]
  decision: Decision
}

export type Act = LegacyAct | SegmentedAct | SteppedAct

export interface Episode {
  id: string
  title: string
  acts: Act[]
}

export interface CatalogCharacter {
  id: string
  name: string
  picture: string
  type: 'party' | 'npc' | 'narrator' | string
  description: string
}

export interface CatalogPlace {
  id: string
  name: string
  picture: string
  description: string
}

export interface CatalogTag {
  id: string
  name: string
  vocab_item_ids: string[]
}
