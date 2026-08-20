import { useEffect, useState } from 'react'
import { Link } from 'react-router'

interface Attribute {
  id: string
  name: string
  description: string
}

export default function Attributes() {
  const [attributes, setAttributes] = useState<Attribute[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/cms/attributes.json')
      .then((res) => res.json())
      .then((data) => {
        setAttributes(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load attributes:', err)
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
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>attributes</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {attributes.map((attribute, idx) => (
            <div
              key={attribute.id}
              style={{
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                padding: '1.25rem',
                backgroundColor: idx % 2 === 0 ? '#ffffff' : '#f9fafb',
              }}
            >
              <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', margin: '0 0 0.5rem 0', color: '#1f2937' }}>
                {attribute.name}
              </h3>
              <p style={{ fontSize: '0.9rem', color: '#4b5563', margin: 0, lineHeight: '1.5' }}>
                {attribute.description}
              </p>
            </div>
          ))}
        </div>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total: {attributes.length} attributes
      </p>
    </div>
  )
}
