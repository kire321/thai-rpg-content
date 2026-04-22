import { Link } from 'react-router'

export default function Home() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
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
