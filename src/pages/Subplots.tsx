import { useEffect, useState } from 'react'
import { Link } from 'react-router'

interface Subplot {
  id: string
  name: string
  description: string
}

export default function Subplots() {
  const [subplots, setSubplots] = useState<Subplot[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/subplots.json')
      .then((res) => res.json())
      .then((data) => {
        setSubplots(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load subplots:', err)
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
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>subplots</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {subplots.map((subplot, idx) => (
            <div
              key={subplot.id}
              style={{
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                padding: '1.25rem',
                backgroundColor: idx % 2 === 0 ? '#ffffff' : '#f9fafb',
              }}
            >
              <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', margin: '0 0 0.5rem 0', color: '#1f2937' }}>
                {subplot.name}
              </h3>
              <p style={{ fontSize: '0.9rem', color: '#4b5563', margin: 0, lineHeight: '1.5' }}>
                {subplot.description}
              </p>
            </div>
          ))}
        </div>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total: {subplots.length} subplots
      </p>
    </div>
  )
}
