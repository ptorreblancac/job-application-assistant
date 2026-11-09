import JobCard from "./JobCard"
import StatCard from "./StatCard"

export default function Dashboard() {
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
                    <JobCard title="Junior Backend Developer" company="TechCorp" location="Barcelona" workArrangement="Hybrid" employmentType="Full-time" match={92} />
                    <JobCard title="Graduate Software Engineer" company="CloudTech" location="Barcelona" workArrangement="Remote" employmentType="Full-time" match={88} />
                    <JobCard title="Frontend Developer" company="Digital Solutions" location="Madrid" workArrangement="On-site" employmentType="Internship" match={85} />
                </div>
 
            </section>
        </section>
    )
}