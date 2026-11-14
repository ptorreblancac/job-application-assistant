import './App.css'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import { useState } from 'react'
import JobSearch from './components/JobSearch'

function App() {
  const [activePage, setActivePage] = useState("dashboard")

  return (
    <div className="app">
      <Sidebar 
        activePage={activePage}
        setActivePage={setActivePage} 
      />

      <main className="main-content">
        <Header />

        {activePage === "dashboard" ? <Dashboard /> : <JobSearch />}
      </main>
    </div>
  )
}

export default App