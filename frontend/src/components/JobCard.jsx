export default function JobCard( {title, company, location, employmentType, match, datePosted} ) {
    return (
        <section className="job-card">
            <div className="job-card-header">
                <h3 className="job-card-title">{title}</h3>
                {<p className="job-card-match">{match !== null ? `${match}/5` : "Not scored"}</p>}
            </div>
            <p className="job-card-company"> {company} · {location} </p>
            <p className="job-card-details"> {employmentType} · {datePosted} </p>
            
        </section>
        
    )
}