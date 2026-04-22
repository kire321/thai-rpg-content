import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router'

interface VocabItem {
  id: string
  thai: string
  phonetics: string
  english: string
  tag_ids: string[]
}

interface Tag {
  id: string
  name: string
}

export default function VocabItems() {
  const [items, setItems] = useState<VocabItem[]>([])
  const [tags, setTags] = useState<Record<string, Tag>>({})
  const [loading, setLoading] = useState(true)
  const [searchParams] = useSearchParams()
  const highlightVocabId = searchParams.get('highlight')

  useEffect(() => {
    Promise.all([
      fetch('/vocab_items.json').then((res) => res.json()),
      fetch('/tags.json').then((res) => res.json()),
    ])
      .then(([vocabData, tagsData]) => {
        setItems(vocabData)
        const tagMap: Record<string, Tag> = {}
        tagsData.forEach((tag: Tag) => {
          tagMap[tag.id] = tag
        })
        setTags(tagMap)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load data:', err)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    if (highlightVocabId) {
      const el = document.getElementById(`vocab-${highlightVocabId}`)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }
  }, [highlightVocabId, loading])

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ marginBottom: '1rem' }}>
        <Link to="/" style={{ color: '#2563eb', textDecoration: 'underline' }}>
          &larr; Back to Tables
        </Link>
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>
        vocab_items
      </h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div style={{ overflowX: 'auto' }}>
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
                  Thai
                </th>
                <th
                  style={{
                    border: '1px solid #d1d5db',
                    padding: '0.5rem 0.75rem',
                    textAlign: 'left',
                    fontWeight: 'bold',
                  }}
                >
                  English
                </th>
                <th
                  style={{
                    border: '1px solid #d1d5db',
                    padding: '0.5rem 0.75rem',
                    textAlign: 'left',
                    fontWeight: 'bold',
                  }}
                >
                  Tags
                </th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, idx) => (
                <tr
                  key={item.id}
                  id={`vocab-${item.id}`}
                  style={{
                    backgroundColor:
                      item.id === highlightVocabId
                        ? '#fef3c7'
                        : idx % 2 === 0
                          ? '#ffffff'
                          : '#f9fafb',
                  }}
                >
                  <td
                    style={{
                      border: '1px solid #d1d5db',
                      padding: '0.5rem 0.75rem',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {item.id}
                  </td>
                  <td
                    style={{
                      border: '1px solid #d1d5db',
                      padding: '0.5rem 0.75rem',
                    }}
                  >
                    {item.thai}
                  </td>
                  <td
                    style={{
                      border: '1px solid #d1d5db',
                      padding: '0.5rem 0.75rem',
                    }}
                  >
                    {item.english}
                  </td>
                  <td
                    style={{
                      border: '1px solid #d1d5db',
                      padding: '0.5rem 0.75rem',
                    }}
                  >
                    {item.tag_ids.map((tid, i) => (
                      <span key={tid}>
                        <Link
                          to={`/tags?highlight=${tid}`}
                          style={{ color: '#2563eb', textDecoration: 'underline' }}
                        >
                          {tags[tid]?.name || tid}
                        </Link>
                        {i < item.tag_ids.length - 1 && ', '}
                      </span>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p style={{ marginTop: '1rem', color: '#6b7280', fontSize: '0.85rem' }}>
        Total rows: {items.length}
      </p>
    </div>
  )
}
