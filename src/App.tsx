import { Routes, Route } from 'react-router'
import Home from './pages/Home'
import VocabItems from './pages/VocabItems'
import Tags from './pages/Tags'
import Characters from './pages/Characters'
import Places from './pages/Places'
import Subplots from './pages/Subplots'
import Episodes from './pages/Episodes'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/vocab_items" element={<VocabItems />} />
      <Route path="/tags" element={<Tags />} />
      <Route path="/characters" element={<Characters />} />
      <Route path="/places" element={<Places />} />
      <Route path="/subplots" element={<Subplots />} />
      <Route path="/episodes" element={<Episodes />} />
    </Routes>
  )
}
