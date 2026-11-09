export default function JobCard( {title, company, location, workArrangement, employmentType, match} ) {
    return (
        <section className="job-card">
            <div className="job-card-header">
                <h3 className="job-card-title">{title}</h3>
                <p className="job-card-match">{match}%</p>
            </div>
            <p className="job-card-company"> {company} · {location} </p>
            <p className="job-card-details">{workArrangement} · {employmentType} </p>
            
        </section>
        
    )
}