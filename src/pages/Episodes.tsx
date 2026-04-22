import { useEffect, useState } from 'react'
import { Link } from 'react-router'

interface Episode {
  id: string
  title: string
  acts: Act[]
}

interface Act {
  id: string
  title: string
  lines_before: Line[]
  tag: string
  lines_after: Line[]
  decision: Decision
}

interface Line {
  character: string
  place: string
  dialogue: string
  stage_directions: string
}

interface Decision {
  line: Line
  choices: Choice[]
}

interface Choice {
  description: string
  difficulty: string
  subplot: string
  pass_outcome: Outcome
  fail_outcome: Outcome
}

interface Outcome {
  line: Line
  subplot: string
  delta: number
}

export default function Episodes() {
  const [episodes, setEpisodes] = useState<Episode[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/episodes.json')
      .then((res) => res.json())
      .then((data) => {
        setEpisodes(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load episodes:', err)
        setLoading(false)
      })
  }, [])

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ marginBottom: '1rem' }}>
        <Link to="/" style={{ color: '#2563eb', textDecoration: 'underline' }}>
          &larr; Back to Tables
        </Link>
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>
        episodes
      </h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          {episodes.map((ep) => (
            <div key={ep.id} style={{ marginBottom: '2rem' }}>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '1rem' }}>
                {ep.title}
              </h2>
              {ep.acts.map((act, actIdx) => (
                <div
                  key={act.id}
                  style={{
                    border: '1px solid #d1d5db',
                    borderRadius: '8px',
                    padding: '1.25rem',
                    marginBottom: '1rem',
                    backgroundColor: actIdx % 2 === 0 ? '#ffffff' : '#f9fafb',
                  }}
                >
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 'bold', margin: '0 0 0.75rem 0', color: '#374151' }}>
                    Act {actIdx + 1}: {act.title}
                  </h3>

                  {/* Lines Before */}
                  <div style={{ marginBottom: '1rem' }}>
                    {act.lines_before.map((line, i) => (
                      <LineBlock key={`before-${i}`} line={line} />
                    ))}
                  </div>

                  {/* Tag */}
                  <div
                    style={{
                      backgroundColor: '#dbeafe',
                      padding: '0.5rem 0.75rem',
                      borderRadius: '6px',
                      marginBottom: '1rem',
                      fontSize: '0.85rem',
                      color: '#1e40af',
                    }}
                  >
                    <strong>Vocab Review:</strong>{' '}
                    <Link to={`/tags?highlight=${act.tag}`} style={{ color: '#1e40af', textDecoration: 'underline' }}>
                      {act.tag}
                    </Link>
                  </div>

                  {/* Lines After */}
                  <div style={{ marginBottom: '1rem' }}>
                    {act.lines_after.map((line, i) => (
                      <LineBlock key={`after-${i}`} line={line} />
                    ))}
                  </div>

                  {/* Decision */}
                  <DecisionBlock decision={act.decision} />
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total: {episodes.length} episode(s)
      </p>
    </div>
  )
}

function LineBlock({ line }: { line: Line }) {
  return (
    <div style={{ marginBottom: '0.75rem' }}>
      {line.stage_directions && (
        <p style={{ fontStyle: 'italic', color: '#6b7280', fontSize: '0.8rem', margin: '0 0 0.25rem 0' }}>
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
      <h4 style={{ fontSize: '0.9rem', fontWeight: 'bold', margin: '0 0 0.5rem 0', color: '#92400e' }}>
        Decision
      </h4>
      <LineBlock line={decision.line} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {decision.choices.map((choice, i) => (
          <div
            key={i}
            style={{
              backgroundColor: '#ffffff',
              border: '1px solid #fcd34d',
              borderRadius: '4px',
              padding: '0.75rem',
            }}
          >
            <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.85rem', fontWeight: 'bold' }}>
              {i + 1}. {choice.description}{' '}
              <span
                style={{
                  fontSize: '0.7rem',
                  padding: '0.1rem 0.4rem',
                  borderRadius: '4px',
                  backgroundColor:
                    choice.difficulty === 'easy' ? '#dcfce7' : choice.difficulty === 'medium' ? '#dbeafe' : '#fee2e2',
                  color:
                    choice.difficulty === 'easy' ? '#166534' : choice.difficulty === 'medium' ? '#1e40af' : '#991b1b',
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
            <OutcomeBlock label="Pass" outcome={choice.pass_outcome} color="#dcfce7" />
            <OutcomeBlock label="Fail" outcome={choice.fail_outcome} color="#fee2e2" />
          </div>
        ))}
      </div>
    </div>
  )
}

function OutcomeBlock({ label, outcome, color }: { label: string; outcome: Outcome; color: string }) {
  return (
    <div
      style={{
        backgroundColor: color,
        padding: '0.5rem',
        borderRadius: '4px',
        marginTop: '0.5rem',
        fontSize: '0.8rem',
      }}
    >
      <strong>{label}</strong> ({outcome.delta > 0 ? '+' : ''}{outcome.delta})
      <p style={{ margin: '0.25rem 0 0 0' }}>{outcome.line.dialogue.substring(0, 100)}...</p>
    </div>
  )
}
