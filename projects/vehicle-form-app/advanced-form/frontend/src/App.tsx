import { BrowserRouter, Routes, Route } from 'react-router-dom'

// pages
import Dashboard from './pages/dashboard/Dashboard.tsx'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        {/* dashboard */}
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
