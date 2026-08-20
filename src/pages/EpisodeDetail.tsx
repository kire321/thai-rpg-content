import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router'

interface Line {
  character: string
  place: string
  dialogue: string
  stage_directions: string
}

interface Choice {
  description: string
  difficulty: string
  attribute: string
  pass_outcome: Outcome
  fail_outcome: Outcome
}

interface Outcome {
  line: Line
  attribute: string
  delta: number
}

interface Decision {
  line: Line
  choices: Choice[]
}

// Old format: single tag with lines_before / lines_after
interface OldAct {
  id: string
  title: string
  lines_before: Line[]
  tag: string
  lines_after: Line[]
  decision: Decision
}

// New format V2: segments array with variable tags
interface NarrativeSegment {
  type: 'narrative'
  lines: Line[]
}

interface TagSegment {
  type: 'tag'
  tag: string
}

type Segment = NarrativeSegment | TagSegment

interface NewAct {
  id: string
  title: string
  segments: Segment[]
  decision: Decision
}

type Act = OldAct | NewAct

interface Episode {
  id: string
  title: string
  acts: Act[]
}

// Helper: Detect old vs new format
function isOldAct(act: Act): act is OldAct {
  return 'lines_before' in act && 'tag' in act && 'lines_after' in act
}

// Helper: Normalize act to render segments
type RenderSegment =
  | { kind: 'narrative'; lines: Line[] }
  | { kind: 'tag'; tag: string }

function normalizeAct(act: Act): RenderSegment[] {
  if (isOldAct(act)) {
    return [
      { kind: 'narrative', lines: act.lines_before },
      { kind: 'tag', tag: act.tag },
      { kind: 'narrative', lines: act.lines_after },
    ]
  }
  return act.segments.map((seg) => {
    if (seg.type === 'narrative') {
      return { kind: 'narrative' as const, lines: seg.lines }
    }
    return { kind: 'tag' as const, tag: seg.tag }
  })
}

export default function EpisodeDetail() {
  const { episodeId } = useParams<{ episodeId: string }>()
  const [episode, setEpisode] = useState<Episode | null>(null)
  const [tags, setTags] = useState<Record<string, { id: string; name: string }>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/cms/episodes.json').then((res) => res.json()),
      fetch('/cms/tags.json').then((res) => res.json()),
    ])
      .then(([epData, tagsData]) => {
        const ep = epData.find((e: Episode) => e.id === episodeId)
        setEpisode(ep || null)
        const tagMap: Record<string, { id: string; name: string }> = {}
        tagsData.forEach((t: { id: string; name: string }) => {
          tagMap[t.id] = t
        })
        setTags(tagMap)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load episode:', err)
        setLoading(false)
      })
  }, [episodeId])

  if (loading) return <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}><p>Loading...</p></div>
  if (!episode) return <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}><p>Episode not found.</p></div>

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif', maxWidth: '900px' }}>
      <div style={{ marginBottom: '1rem' }}>
        <Link to="/episodes" style={{ color: '#2563eb', textDecoration: 'underline' }}>
          &larr; Back to Episodes
        </Link>
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.25rem' }}>
        {episode.title}
      </h1>
      <p style={{ color: '#6b7280', fontSize: '0.85rem', marginBottom: '1.5rem' }}>{episode.id}</p>

      {episode.acts.map((act, actIdx) => {
        const segments = normalizeAct(act)
        return (
          <div
            key={act.id}
            style={{
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              padding: '1.25rem',
              marginBottom: '1.5rem',
              backgroundColor: '#ffffff',
            }}
          >
            <h2 style={{ fontSize: '1.15rem', fontWeight: 'bold', margin: '0 0 1rem 0', color: '#1f2937' }}>
              Act {actIdx + 1}: {act.title}
            </h2>

            {/* Render segments in order */}
            {segments.map((seg, segIdx) =>
              seg.kind === 'narrative' ? (
                <div key={segIdx} style={{ marginBottom: '1rem' }}>
                  {seg.lines.map((line, lineIdx) => (
                    <LineBlock key={`${segIdx}-${lineIdx}`} line={line} />
                  ))}
                </div>
              ) : (
                <div
                  key={segIdx}
                  style={{
                    backgroundColor: '#dbeafe',
                    padding: '0.6rem 0.9rem',
                    borderRadius: '6px',
                    marginBottom: '1rem',
                    fontSize: '0.85rem',
                  }}
                >
                  <strong style={{ color: '#1e40af' }}>Vocab Review:</strong>{' '}
                  <Link
                    to={`/tags?highlight=${seg.tag}`}
                    style={{ color: '#1e40af', textDecoration: 'underline' }}
                  >
                    {tags[seg.tag]?.name || seg.tag}
                  </Link>
                </div>
              )
            )}

            {/* Decision */}
            <DecisionBlock decision={act.decision} />
          </div>
        )
      })}
    </div>
  )
}

function LineBlock({ line }: { line: Line }) {
  return (
    <div style={{ marginBottom: '0.85rem' }}>
      {line.stage_directions && (
        <p style={{ fontStyle: 'italic', color: '#6b7280', fontSize: '0.78rem', margin: '0 0 0.2rem 0' }}>
          [{line.stage_directions}]
        </p>
      )}
      <p style={{ margin: 0, fontSize: '0.9rem', lineHeight: '1.5' }}>
        <strong style={{ color: '#374151' }}>{line.character}:</strong>{' '}
        {line.dialogue}
      </p>
    </div>
  )
}

function DecisionBlock({ decision }: { decision: Decision }) {
  return (
    <div
      style={{
        border: '2px solid #f59e0b',
        borderRadius: '6px',
        padding: '1rem',
        backgroundColor: '#fffbeb',
      }}
    >
      <h3 style={{ fontSize: '0.9rem', fontWeight: 'bold', margin: '0 0 0.5rem 0', color: '#92400e' }}>
        Decision
      </h3>
      <LineBlock line={decision.line} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '0.75rem' }}>
        {decision.choices.map((choice, i) => (
          <ChoiceBlock key={i} choice={choice} index={i} />
        ))}
      </div>
    </div>
  )
}

function ChoiceBlock({ choice, index }: { choice: Choice; index: number }) {
  const diffColor =
    choice.difficulty === 'easy'
      ? { bg: '#dcfce7', text: '#166534' }
      : choice.difficulty === 'medium'
        ? { bg: '#dbeafe', text: '#1e40af' }
        : { bg: '#fee2e2', text: '#991b1b' }

  return (
    <div
      style={{
        backgroundColor: '#ffffff',
        border: '1px solid #fcd34d',
        borderRadius: '4px',
        padding: '0.75rem',
      }}
    >
      <p style={{ margin: '0 0 0.4rem 0', fontSize: '0.85rem', fontWeight: 'bold' }}>
        {index + 1}. {choice.description}{' '}
        <span
          style={{
            fontSize: '0.7rem',
            padding: '0.15rem 0.4rem',
            borderRadius: '4px',
            backgroundColor: diffColor.bg,
            color: diffColor.text,
            fontWeight: 'bold',
          }}
        >
          {choice.difficulty}
        </span>
      </p>
      <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.8rem', color: '#6b7280' }}>
        Attribute:{' '}
        <Link to={`/attributes?highlight=${choice.attribute}`} style={{ color: '#2563eb', textDecoration: 'underline' }}>
          {choice.attribute}
        </Link>
      </p>
      <OutcomeBlock label="Pass" outcome={choice.pass_outcome} bg="#dcfce7" />
      <OutcomeBlock label="Fail" outcome={choice.fail_outcome} bg="#fee2e2" />
    </div>
  )
}

function OutcomeBlock({ label, outcome, bg }: { label: string; outcome: Outcome; bg: string }) {
  return (
    <div
      style={{
        backgroundColor: bg,
        padding: '0.5rem 0.6rem',
        borderRadius: '4px',
        marginTop: '0.4rem',
        fontSize: '0.8rem',
      }}
    >
      <strong>
        {label} ({outcome.delta > 0 ? '+' : ''}{outcome.delta})
      </strong>
      <p style={{ margin: '0.2rem 0 0 0', lineHeight: '1.4' }}>{outcome.line.dialogue}</p>
    </div>
  )
}
