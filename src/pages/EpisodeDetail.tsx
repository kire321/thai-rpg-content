import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router'
import { fetchCmsJson } from '../lib/cms'
import type {
  Act,
  ActSegment,
  CatalogCharacter,
  CatalogPlace,
  CatalogTag,
  Choice,
  Decision,
  Episode,
  Line,
} from '../types/content'

interface RenderNarrative {
  kind: 'narrative'
  lines: Line[]
}

interface RenderTag {
  kind: 'tag'
  tag: string
}

type RenderSegment = RenderNarrative | RenderTag

function isSegmentedAct(act: Act): act is Extract<Act, { segments: ActSegment[] }> {
  return 'segments' in act && Array.isArray(act.segments)
}

function isSteppedAct(act: Act): act is Extract<Act, { steps: ActSegment[] }> {
  return 'steps' in act && Array.isArray(act.steps)
}

/** Normalize legacy and ordered-list acts into one renderable sequence. */
function normalizeAct(act: Act): RenderSegment[] {
  if (isSegmentedAct(act)) {
    return act.segments.flatMap<RenderSegment>((segment): RenderSegment[] =>
      segment.type === 'narrative'
        ? [{ kind: 'narrative' as const, lines: segment.lines }]
        : [{ kind: 'tag' as const, tag: segment.tag }],
    )
  }

  if (isSteppedAct(act)) {
    return act.steps.flatMap<RenderSegment>((segment): RenderSegment[] =>
      segment.type === 'narrative'
        ? [{ kind: 'narrative' as const, lines: segment.lines }]
        : [{ kind: 'tag' as const, tag: segment.tag }],
    )
  }

  return [
    { kind: 'narrative', lines: act.lines_before },
    { kind: 'tag', tag: act.tag },
    { kind: 'narrative', lines: act.lines_after },
  ]
}

export default function EpisodeDetail() {
  const { episodeId } = useParams<{ episodeId: string }>()
  const [episode, setEpisode] = useState<Episode | null>(null)
  const [tags, setTags] = useState<Record<string, CatalogTag>>({})
  const [characters, setCharacters] = useState<Record<string, CatalogCharacter>>({})
  const [places, setPlaces] = useState<Record<string, CatalogPlace>>({})
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchCmsJson<Episode[]>('episodes.json'),
      fetchCmsJson<CatalogTag[]>('tags.json'),
      fetchCmsJson<CatalogCharacter[]>('characters.json'),
      fetchCmsJson<CatalogPlace[]>('places.json'),
    ])
      .then(([episodeData, tagData, characterData, placeData]) => {
        const found = episodeData.find((candidate) => candidate.id === episodeId)
        const tagMap: Record<string, CatalogTag> = {}
        const characterMap: Record<string, CatalogCharacter> = {}
        const placeMap: Record<string, CatalogPlace> = {}

        tagData.forEach((tag) => { tagMap[tag.id] = tag })
        characterData.forEach((character) => { characterMap[character.id] = character })
        placeData.forEach((place) => { placeMap[place.id] = place })

        setEpisode(found || null)
        setTags(tagMap)
        setCharacters(characterMap)
        setPlaces(placeMap)
        setLoading(false)
      })
      .catch((loadError: unknown) => {
        console.error('Failed to load episode:', loadError)
        setError(loadError instanceof Error ? loadError.message : 'Unable to load CMS data')
        setLoading(false)
      })
  }, [episodeId])

  if (loading) return <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}><p>Loading...</p></div>
  if (error) return <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}><p>Unable to load episode: {error}</p></div>
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
        let quizNumber = 0
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

            {segments.map((segment, segmentIndex) => {
              if (segment.kind === 'narrative') {
                return (
                  <div key={segmentIndex} style={{ marginBottom: '1rem' }}>
                    {segment.lines.map((line, lineIndex) => (
                      <LineBlock
                        key={`${segmentIndex}-${lineIndex}`}
                        line={line}
                        characters={characters}
                        places={places}
                      />
                    ))}
                  </div>
                )
              }

              quizNumber += 1
              return (
                <div
                  key={segmentIndex}
                  style={{
                    backgroundColor: '#dbeafe',
                    padding: '0.6rem 0.9rem',
                    borderRadius: '6px',
                    marginBottom: '1rem',
                    fontSize: '0.85rem',
                  }}
                >
                  <strong style={{ color: '#1e40af' }}>Vocab Quiz {quizNumber}:</strong>{' '}
                  <Link
                    to={`/tags?highlight=${segment.tag}`}
                    style={{ color: '#1e40af', textDecoration: 'underline' }}
                  >
                    {tags[segment.tag]?.name || segment.tag}
                  </Link>
                </div>
              )
            })}

            <DecisionBlock
              decision={'decision' in act ? act.decision : undefined}
              characters={characters}
              places={places}
            />
          </div>
        )
      })}
    </div>
  )
}

function LineBlock({
  line,
  characters,
  places,
}: {
  line: Line
  characters: Record<string, CatalogCharacter>
  places: Record<string, CatalogPlace>
}) {
  const characterName = characters[line.character]?.name || line.character
  const placeName = places[line.place]?.name

  return (
    <div style={{ marginBottom: '0.85rem' }}>
      {line.stage_directions && (
        <p style={{ fontStyle: 'italic', color: '#6b7280', fontSize: '0.78rem', margin: '0 0 0.2rem 0' }}>
          [{line.stage_directions}]
        </p>
      )}
      <p style={{ margin: 0, fontSize: '0.9rem', lineHeight: '1.5' }}>
        <strong style={{ color: '#374151' }}>{characterName}:</strong>{' '}
        {line.dialogue}
      </p>
      {placeName && (
        <span style={{ color: '#9ca3af', fontSize: '0.7rem' }}>at {placeName}</span>
      )}
    </div>
  )
}

function DecisionBlock({
  decision,
  characters,
  places,
}: {
  decision: Decision | undefined
  characters: Record<string, CatalogCharacter>
  places: Record<string, CatalogPlace>
}) {
  if (!decision) return null

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
        Options
      </h3>
      <LineBlock line={decision.line} characters={characters} places={places} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '0.75rem' }}>
        {decision.choices.map((choice, index) => (
          <ChoiceBlock key={index} choice={choice} index={index} characters={characters} places={places} />
        ))}
      </div>
    </div>
  )
}

function ChoiceBlock({
  choice,
  index,
  characters,
  places,
}: {
  choice: Decision['choices'][number]
  index: number
  characters: Record<string, CatalogCharacter>
  places: Record<string, CatalogPlace>
}) {
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
        Subplot:{' '}
        <Link to={`/subplots?highlight=${choice.subplot}`} style={{ color: '#2563eb', textDecoration: 'underline' }}>
          {choice.subplot}
        </Link>
      </p>
      <OutcomeBlock label="Pass" outcome={choice.pass_outcome} bg="#dcfce7" characters={characters} places={places} />
      <OutcomeBlock label="Fail" outcome={choice.fail_outcome} bg="#fee2e2" characters={characters} places={places} />
    </div>
  )
}

function OutcomeBlock({
  label,
  outcome,
  bg,
  characters,
  places,
}: {
  label: string
  outcome: Choice['pass_outcome']
  bg: string
  characters: Record<string, CatalogCharacter>
  places: Record<string, CatalogPlace>
}) {
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
      <LineBlock line={outcome.line} characters={characters} places={places} />
    </div>
  )
}
