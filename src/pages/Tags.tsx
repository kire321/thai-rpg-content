import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router'

interface Tag {
  id: string
  name: string
  vocab_item_ids: string[]
}

interface VocabItem {
  id: string
  thai: string
  english: string
}

export default function Tags() {
  const [tags, setTags] = useState<Tag[]>([])
  const [vocabMap, setVocabMap] = useState<Record<string, VocabItem>>({})
  const [loading, setLoading] = useState(true)
  const [searchParams] = useSearchParams()
  const highlightTagId = searchParams.get('highlight')

  useEffect(() => {
    Promise.all([
      fetch('/tags.json').then((res) => res.json()),
      fetch('/vocab_items.json').then((res) => res.json()),
    ])
      .then(([tagsData, vocabData]) => {
        setTags(tagsData)
        const vocabMap: Record<string, VocabItem> = {}
        vocabData.forEach((item: VocabItem & { tag_ids: string[]; phonetics: string }) => {
          vocabMap[item.id] = { id: item.id, thai: item.thai, english: item.english }
        })
        setVocabMap(vocabMap)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load data:', err)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    if (highlightTagId) {
      const el = document.getElementById(`tag-${highlightTagId}`)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }
  }, [highlightTagId, loading])

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ marginBottom: '1rem' }}>
        <Link to="/" style={{ color: '#2563eb', textDecoration: 'underline' }}>
          &larr; Back to Tables
        </Link>
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>
        tags
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
                  Name
                </th>
                <th
                  style={{
                    border: '1px solid #d1d5db',
                    padding: '0.5rem 0.75rem',
                    textAlign: 'left',
                    fontWeight: 'bold',
                  }}
                >
                  Vocab Items
                </th>
              </tr>
            </thead>
            <tbody>
              {tags.map((tag, idx) => (
                <tr
                  key={tag.id}
                  id={`tag-${tag.id}`}
                  style={{
                    backgroundColor:
                      tag.id === highlightTagId
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
                    {tag.id}
                  </td>
                  <td
                    style={{
                      border: '1px solid #d1d5db',
                      padding: '0.5rem 0.75rem',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {tag.name}
                  </td>
                  <td
                    style={{
                      border: '1px solid #d1d5db',
                      padding: '0.5rem 0.75rem',
                    }}
                  >
                    {tag.vocab_item_ids.map((vid, i) => (
                      <span key={vid}>
                        <Link
                          to={`/vocab_items?highlight=${vid}`}
                          style={{ color: '#2563eb', textDecoration: 'underline' }}
                        >
                          {vocabMap[vid]?.english?.substring(0, 40) || vid}
                          {vocabMap[vid]?.english && vocabMap[vid].english.length > 40 ? '...' : ''}
                        </Link>
                        {i < tag.vocab_item_ids.length - 1 && ', '}
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
        Total rows: {tags.length}
      </p>
    </div>
  )
}
