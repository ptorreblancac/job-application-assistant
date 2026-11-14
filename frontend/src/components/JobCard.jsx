export default function JobCard( {title, company, location, employmentType, match, datePosted, postingLink} ) {
    return (
        <section className="job-card">
            <div className="job-card-header">
                <a href={postingLink} target="_blank" rel="noopener noreferrer" className="job-card-title">{title}</a>
                <p className="job-card-match">{match !== null ? `${match}/5` : "Not scored"}</p>
            </div>
            <p className="job-card-company"> {company} · {location} </p>
            <p className="job-card-details"> {employmentType} · {datePosted} </p>
            
        </section>
        
    )
}