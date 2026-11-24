export default function JobCard( {title, company, location, employmentType, match, datePosted, postingLink} ) {
    const displayedEmploymentType = employmentType || "Not specified"
    const displayedDate = datePosted ?  new Date(datePosted).toLocaleDateString() : "Date unknown"
    const displayedMatch = match != null ? `${match}/100` : "Not scored"
    
    return (
        <section className="job-card">
            <div className="job-card-header">
                {postingLink ?
                    <a href={postingLink} target="_blank" rel="noopener noreferrer" className="job-card-title">{title}</a>
                    : <p className="job-card-title">{title}</p>
                }
                <p className="job-card-match">{displayedMatch}</p>
            </div>
            <p className="job-card-company"> {company} · {location} </p>
            <p className="job-card-details"> {displayedEmploymentType} · {displayedDate} </p>
            
        </section>
        
    )
}