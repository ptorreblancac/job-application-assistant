import JobCard from "./JobCard"
import StatCard from "./StatCard"
import { useState, useEffect } from "react"

const url = "http://127.0.0.1:8000/jobs/"

export default function Dashboard() {
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    useEffect(() => {
        fetch(url)
            .then(response => {
                return response.json()
            })
            .then(data => {
                setJobs(data)
            })
            .catch(error => {
                setError("Unable to load jobs. Please try again later.")
            })
            .finally(
                setLoading(false)
            )

    }, []); //runs only on the first render

    return(
        <section className="dashboard-content">
            <div className="stats-container">
                <StatCard title="Jobs found" value={24} />
                <StatCard title="Saved jobs" value={8} />
                <StatCard title="Applications" value={3} />
            </div>
            <section className="recommended-jobs">
                <h3>Recommended Jobs</h3>
                <div className="job-list">
                    {loading ? (
                            <p>Loading jobs...</p>
                        ) : (
                            error ? (
                            <p>{error}</p>
                            ) : (
                                jobs.length === 0 ? (
                                <p>No jobs found</p>
                                
                                ) : (
                                    jobs.map(job => (
                                        <JobCard 
                                            key={job.id}
                                            title={job.title} 
                                            company={job.company} 
                                            location={job.location} 
                                            employmentType={job.job_type} 
                                        />
                                    ))
                                )
                            )
                            
                        )
                    }
                </div>
 
            </section>
        </section>
    )
}