import JobCard from "./JobCard"
import StatCard from "./StatCard"
import { useState, useEffect } from "react"

const url = "http://127.0.0.1:8000/jobs/"

export default function Dashboard() {
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const sortedJobs = jobs.slice().filter(job => job.relevance_score != null).sort((a,b) => b.relevance_score - a.relevance_score).slice(0,5)

    const recentJobs = jobs.slice().filter(job => job.date_posted != null).sort((a,b) => new Date(b.date_posted) - new Date(a.date_posted)).slice(0,5)

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
            .catch(() => {
                setError("Unable to load jobs. Please try again later.")
            })
            .finally(() => {
                setLoading(false);
            });

    }, []); //runs only on the first render

    const validScore = jobs.filter(job => job.relevance_score != null)
    const sumScores = validScore.reduce((accumulator, currentItem) => {
        return accumulator + currentItem.relevance_score
    }, 0)

    const averageMatchScore = (validScore.length == 0)? "N/A" : (sumScores/validScore.length).toFixed(1)

    const listScores = validScore.map(score => score.relevance_score)
    const highestMatchScore = (validScore.length == 0)? "N/A" : Math.max(...listScores)

    return(
        <section className="dashboard-content">
            <div className="stats-container">
                <StatCard title="Jobs found" value={jobs.length} />
                <StatCard title="Average Match Score" value={averageMatchScore} />
                <StatCard title="Highest Match Score" value={highestMatchScore} />
            </div>
            <div>
                {loading ? (
                    <p>Loading jobs...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : jobs.length === 0 ? (
                    <p>No jobs found</p>
                    ) : ( 
                        <div className="jobs">                              
                            <section className="recommended-jobs">
                                <h3>Recommended Jobs</h3>
                                <div className="job-list">
                                    {sortedJobs.map(job => (
                                        <JobCard 
                                            key={job.id}
                                            title={job.title} 
                                            company={job.company} 
                                            location={job.location} 
                                            employmentType={job.job_type} 
                                            match={job.relevance_score}
                                            datePosted={job.date_posted}
                                            postingLink={job.posting_link}
                                        />
                                    ))}
                                </div>
                            </section>
                            <section className="recent-jobs">
                                <h3>Recently Posted</h3>
                                <div className="job-list">
                                    {recentJobs.map(job => (
                                        <JobCard 
                                            key={job.id}
                                            title={job.title} 
                                            company={job.company} 
                                            location={job.location} 
                                            employmentType={job.job_type} 
                                            match={job.relevance_score}
                                            datePosted={job.date_posted}
                                            postingLink={job.posting_link}
                                        />
                                    ))}
                                </div>
                            </section>
                        </div>
                    )
                }
            </div>

            

            
        </section>
    )
}