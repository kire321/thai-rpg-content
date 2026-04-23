import { useEffect, useState } from 'react'
import { Link } from 'react-router'

interface Episode {
  id: string
  title: string
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
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>episodes</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table
          style={{
            borderCollapse: 'collapse',
            width: '100%',
            fontSize: '0.9rem',
          }}
        >
          <thead>
            <tr style={{ backgroundColor: '#f3f4f6' }}>
              <th
                style={{
                  border: '1px solid #d1d5db',
                  padding: '0.5rem 0.75rem',
                  textAlign: 'left',
                  fontWeight: 'bold',
                }}
              >
                id
              </th>
              <th
                style={{
                  border: '1px solid #d1d5db',
                  padding: '0.5rem 0.75rem',
                  textAlign: 'left',
                  fontWeight: 'bold',
                }}
              >
                Title
              </th>
            </tr>
          </thead>
          <tbody>
            {episodes.map((ep, idx) => (
              <tr
                key={ep.id}
                style={{
                  backgroundColor: idx % 2 === 0 ? '#ffffff' : '#f9fafb',
                }}
              >
                <td
                  style={{
                    border: '1px solid #d1d5db',
                    padding: '0.5rem 0.75rem',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {ep.id}
                </td>
                <td
                  style={{
                    border: '1px solid #d1d5db',
                    padding: '0.5rem 0.75rem',
                  }}
                >
                  <Link
                    to={`/episodes/${ep.id}`}
                    style={{ color: '#2563eb', textDecoration: 'underline' }}
                  >
                    {ep.title}
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total: {episodes.length} episode(s)
      </p>
    </div>
  )
}
