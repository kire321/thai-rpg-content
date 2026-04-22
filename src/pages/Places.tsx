import { useEffect, useState } from 'react'
import { Link } from 'react-router'

interface Place {
  id: string
  name: string
  picture: string
  description: string
}

export default function Places() {
  const [places, setPlaces] = useState<Place[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/places.json')
      .then((res) => res.json())
      .then((data) => {
        setPlaces(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load places:', err)
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
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>places</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {places.map((place) => (
            <div
              key={place.id}
              style={{
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                overflow: 'hidden',
                backgroundColor: '#ffffff',
              }}
            >
              <img
                src={place.picture}
                alt={place.name}
                style={{ width: '100%', height: '240px', objectFit: 'cover', display: 'block' }}
              />
              <div style={{ padding: '1rem' }}>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 'bold', margin: '0 0 0.5rem 0' }}>{place.name}</h3>
                <p style={{ fontSize: '0.9rem', color: '#4b5563', margin: 0, lineHeight: '1.5' }}>
                  {place.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total: {places.length} places
      </p>
    </div>
  )
}
