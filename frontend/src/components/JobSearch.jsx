import {useState, useEffect} from "react"
import JobCard from "./JobCard"

const url = "http://127.0.0.1:8000/jobs/"

export default function JobSearch() {
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [selectedCompany, setSelectedCompany] = useState("")
    const [selectedLocation, setSelectedLocation] = useState("")
    const [selectedEmploymentType, setSelectedEmploymentType] = useState("")
    const [searchTerm, setSearchTerm] = useState("")

    const sortedJobs = [...jobs].sort((a, b) => {
        if (a.relevance_score === null && b.relevance_score === null) return 0
        if (a.relevance_score === null) return 1
        if (b.relevance_score === null) return -1

        return b.relevance_score - a.relevance_score
    })

    const companies = [...new Set(jobs.filter(job => job.company).map(job => (job.company)))]
    const locations = [...new Set(jobs.filter(job => job.location).map(job => (job.location)))]
    const employmentTypes = [...new Set(jobs.filter(job => job.job_type).map(job => (job.job_type)))]

    const normalizedSearch = searchTerm.toLowerCase()

    const filteredJobs = sortedJobs.filter(job => {
        const matchesCompany = selectedCompany === "" || job.company === selectedCompany
        const matchesLocation = selectedLocation === "" || job.location === selectedLocation
        const matchesEmploymentType = selectedEmploymentType === "" || job.job_type === selectedEmploymentType
        
        const matchesSearch = searchTerm === "" || (job.title || "").toLowerCase().includes(normalizedSearch) || (job.description || "").toLowerCase().includes(normalizedSearch) || (job.company || "").toLowerCase().includes(normalizedSearch)

        return matchesCompany && matchesLocation && matchesEmploymentType && matchesSearch
    })


    useEffect(() => {
        fetch(url)
            .then(response => {
                if(!response.ok) {
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
                setLoading(false)
            })
    }, [])

    return (
        <section className="job-search">
            <header>Job Search</header>
            <p>Explore and discover opportunities matching your profile.</p>
            <label>
                <input
                    type="text"
                    value={searchTerm}
                    onChange={(event) => setSearchTerm(event.target.value)}
                    placeholder="Search jobs by title, company or keyword..."
                />
                Search jobs:
            </label>
            <select
                value={selectedCompany}
                onChange={(event) => setSelectedCompany(event.target.value)}
            >
                <option value="">All companies</option>

                {companies.map(company => (
                    <option key={company} value={company}>{company}</option>
                ))}
            </select>
            <select
                value={selectedLocation}
                onChange={(event) => setSelectedLocation(event.target.value)}
            >
                <option value="">All locations</option>

                {locations.map(location => (
                    <option key={location} value={location}>{location}</option>
                ))}
            </select>
            <select
                value={selectedEmploymentType}
                onChange={(event) => setSelectedEmploymentType(event.target.value)}
            >
                <option value="">All employment types</option>

                {employmentTypes.map(employmentType => (
                    <option key={employmentType} value={employmentType}>{employmentType}</option>
                ))}
            </select>
            <button
                onClick={() => {
                    setSelectedCompany("")
                    setSearchTerm("")
                    setSelectedEmploymentType("")
                    setSelectedLocation("")
                }}
            >
                Clear filters
            </button>
                { loading ? (
                    <p>Loading jobs...</p>
                ) : error ? (
                    <p>{error} </p>
                ) : jobs.length === 0 ? (
                    <p>No jobs found</p>
                ) : filteredJobs.length === 0 ? (
                    <p>No jobs match your filters</p>
                ) :
                    <section className="job-list">
                        {filteredJobs.map(job => (
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
                    </section>
                }     
                
        </section>
    )
} 