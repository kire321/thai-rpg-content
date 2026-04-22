import { useEffect, useState } from 'react'
import { Link } from 'react-router'

interface Character {
  id: string
  name: string
  picture: string
  type: string
  description: string
}

export default function Characters() {
  const [characters, setCharacters] = useState<Character[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/characters.json')
      .then((res) => res.json())
      .then((data) => {
        setCharacters(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load characters:', err)
        setLoading(false)
      })
  }, [])

  const typeLabel = (type: string) => {
    switch (type) {
      case 'party': return 'Party Member'
      case 'npc': return 'NPC Type'
      case 'narrator': return 'Narrator'
      default: return type
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ marginBottom: '1rem' }}>
        <Link to="/" style={{ color: '#2563eb', textDecoration: 'underline' }}>
          &larr; Back to Tables
        </Link>
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>characters</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' }}>
          {characters.map((char) => (
            <div
              key={char.id}
              style={{
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                overflow: 'hidden',
                backgroundColor: '#ffffff',
              }}
            >
              <img
                src={char.picture}
                alt={char.name}
                style={{ width: '100%', height: '280px', objectFit: 'cover', display: 'block' }}
              />
              <div style={{ padding: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', margin: 0 }}>{char.name}</h3>
                  <span style={{
                    fontSize: '0.75rem',
                    padding: '0.2rem 0.5rem',
                    borderRadius: '9999px',
                    backgroundColor: char.type === 'party' ? '#dbeafe' : char.type === 'narrator' ? '#fef3c7' : '#f3f4f6',
                    color: char.type === 'party' ? '#1e40af' : char.type === 'narrator' ? '#92400e' : '#374151',
                  }}>
                    {typeLabel(char.type)}
                  </span>
                </div>
                <p style={{ fontSize: '0.85rem', color: '#4b5563', margin: 0, lineHeight: '1.4' }}>
                  {char.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total: {characters.length} characters
      </p>
    </div>
  )
}
