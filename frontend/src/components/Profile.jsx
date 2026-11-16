import {useState, useEffect} from "react"

const url = "http://127.0.0.1:8000/jobs/profiles/1/"

export default function Profile() {
    const [profile, setProfile] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetch(url)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Something went wrong")
                }
                return response.json()
            })
            .then((data) => {
                setProfile(data)
            })
            .catch((error) => {
                setError(error.message)
            })
            .finally(() => {
                setLoading(false)
            })
    }, [])

    return(
        <div>
        {loading ? (
            <p>Loading...</p>
        ) : error ? (
            <p>{error}</p>
        ) : (
            <div>
                <p>{profile.target_role}</p>
                <p>{profile.location}</p>
                <p>{profile.seniority}</p>
            </div>
        )    
        }
        </div>
    )
}