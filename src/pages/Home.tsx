import { Link } from 'react-router'

export default function Home() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <div style={{
        backgroundColor: '#fef3c7',
        border: '1px solid #f59e0b',
        borderRadius: '6px',
        padding: '0.75rem 1rem',
        marginBottom: '1rem',
        fontSize: '0.85rem',
        color: '#92400e',
      }}>
        <strong>Staging Environment</strong> — This preview contains unreleased content including 170 new episodes with the expanded 2-tag-per-act format, 10 new NPCs, and 10 new locations.
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>Tables</h1>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        <li style={{ marginBottom: '0.5rem' }}>
          <Link to="/vocab_items" style={{ color: '#2563eb', textDecoration: 'underline', fontSize: '1.1rem' }}>
            Vocab Items
          </Link>
        </li>
        <li style={{ marginBottom: '0.5rem' }}>
          <Link to="/tags" style={{ color: '#2563eb', textDecoration: 'underline', fontSize: '1.1rem' }}>
            Tags
          </Link>
        </li>
        <li style={{ marginBottom: '0.5rem' }}>
          <Link to="/characters" style={{ color: '#2563eb', textDecoration: 'underline', fontSize: '1.1rem' }}>
            Characters
          </Link>
        </li>
        <li style={{ marginBottom: '0.5rem' }}>
          <Link to="/places" style={{ color: '#2563eb', textDecoration: 'underline', fontSize: '1.1rem' }}>
            Places
          </Link>
        </li>
        <li style={{ marginBottom: '0.5rem' }}>
          <Link to="/subplots" style={{ color: '#2563eb', textDecoration: 'underline', fontSize: '1.1rem' }}>
            Subplots
          </Link>
        </li>
        <li>
          <Link to="/episodes" style={{ color: '#2563eb', textDecoration: 'underline', fontSize: '1.1rem' }}>
            Episodes
          </Link>
        </li>
      </ul>
    </div>
  )
}
