import './App.css'

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h2>Job Assistant</h2>
        <nav>
          <a href="placeholder" className="active">Dashboard</a>
          <a href="placeholder">Job Search</a>
          <a href="placeholder">Saved Jobs</a>
          <a href="placeholder">Applications</a>
          <a href="placeholder">Profile</a>
        </nav>
      </aside>

      <main className="main-content">
        <header className="header">
          <h1>Dashboard</h1>
        </header>

        <section className="dashboard-content">
          <h2>Welcome back!</h2>
          <p>Your job search overview will appear here.</p>
        </section>
      </main>
    </div>
  )
}

export default App