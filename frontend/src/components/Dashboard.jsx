import JobCard from "./JobCard"
import StatCard from "./StatCard"
import { useState, useEffect } from "react"

const url = "http://127.0.0.1:8000/jobs/"

export default function Dashboard() {
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const sortedJobs = jobs.slice().sort((a,b) => {
            if (a.relevance_score === null && b.relevance_score === null) return 0
            if (a.relevance_score === null) return 1
            if (b.relevance_score === null) return -1

            return b.relevance_score - a.relevance_score
        }
    ).slice(0,5)

    const recentJobs = jobs.slice().sort((a,b) => {
        if (a.date_posted === null && b.date_posted === null) return 0
        if (a.date_posted === null) return 1 //if positive, returns b first
        if (b.date_posted === null) return -1 //if negative, returns a first

        return new Date(b.date_posted) - new Date(a.date_posted)
    }).slice(0,5)

    useEffect(() => {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Something went wrong")
                }
                return response.json()
            })
            .then(data => {
                setJobs(data)
            })
            .catch(error => {
                setError("Unable to load jobs. Please try again later.")
            })
            .finally(() => {
                setLoading(false);
            });

    }, []); //runs only on the first render

    return(
        <section className="dashboard-content">
            <div className="stats-container">
                <StatCard title="Jobs found" value={jobs.length} />
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
                                    sortedJobs.map(job => (
                                        <JobCard 
                                            key={job.id}
                                            title={job.title} 
                                            company={job.company} 
                                            location={job.location} 
                                            employmentType={job.job_type} 
                                            match={job.relevance_score}
                                            datePosted={job.date_posted}
                                        />
                                    ))
                                )
                            )
                            
                        )
                    }
                </div>
 
            </section>

            <section className="recent-jobs">
                <h3>Recently Posted</h3>
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
                                    recentJobs.map(job => (
                                        <JobCard 
                                            key={job.id}
                                            title={job.title} 
                                            company={job.company} 
                                            location={job.location} 
                                            employmentType={job.job_type} 
                                            match={job.relevance_score}
                                            datePosted={job.date_posted}
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