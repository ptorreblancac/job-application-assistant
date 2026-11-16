export default function Sidebar({ activePage, setActivePage }) {
    return (
        <aside className="sidebar">
            <h2>Job Assistant</h2>
            <nav>
                <a href="placeholder" className={activePage === "dashboard" ? "active" : ""} 
                onClick={() => {
                    event.preventDefault()
                    setActivePage("dashboard")
                }}>Dashboard</a>
                <a href="placeholder" className={activePage === "job-search" ? "active" : ""} 
                    onClick={(event) => {
                        event.preventDefault()
                        setActivePage("job-search")
                    }}>Job Search</a>
                <a href="placeholder" className={activePage === "profile" ? "active" : ""} 
                    onClick={() => {
                        event.preventDefault()
                        setActivePage("profile")
                        }}>Profile</a>
                <a href="placeholder">Saved Jobs</a>
                <a href="placeholder">Applications</a>
            </nav>
        </aside>
    )
}

