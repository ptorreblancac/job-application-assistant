import {useState, useEffect} from "react"

const url = "http://127.0.0.1:8000/jobs/profiles/1/"
const updateUrl = "http://127.0.0.1:8000/jobs/profiles/1/update/"

export default function Profile() {
    const [profile, setProfile] = useState(null)
    const [loading, setLoading] = useState(true)
    const [loadError, setLoadError] = useState(null)
    const [saveError, setSaveError] = useState(null)
    const [skillsInput, setSkillsInput] = useState("")
    const [saveMessage, setSaveMessage] = useState("")

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
                setSkillsInput(data.preferred_skills.join(", "))
            })
            .catch((error) => {
                setLoadError(error.message)
            })
            .finally(() => {
                setLoading(false)
            })
    }, [])

    const handleSave = () => {
        setSaveError(null)
        setSaveMessage("")

        const updatedProfile = {
            ...profile,
            preferred_skills: skillsInput.split(",").map(skill => skill.trim()).filter((skill) => skill !== "")       
        }

        fetch(updateUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedProfile)
        })
        .then(async (response) => {
            const data = await response.text()

            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${data}`)
            }

            return JSON.parse(data)
        })
        .then(() => {
            setSaveMessage("Profile saved successfully!")
        })
        .catch((error) => {
            setSaveError(error.message)
        })
    }

    return(
        <div>
        {loading ? (
            <p>Loading...</p>
        ) : loadError ? (
            <p>{loadError}</p>
        ) : (
            <div className="profile-content">
                <section className="basic-info">
                    <h3>Basic information</h3>
                    <label>Target role
                        <input 
                            value={profile.target_role}
                            onChange={(event) => {
                                setProfile({...profile, target_role: event.target.value})
                            }}
                        />
                    </label>
                    <label>
                        Location
                        <input 
                            value={profile.location}
                            onChange={(event) => {
                                setProfile({...profile, location: event.target.value})
                            }}
                        />
                    </label>
                    <label>
                        Country
                        <input 
                            value={profile.country}
                            onChange={(event) => {
                                setProfile({...profile, country: event.target.value})
                            }}
                        />
                    </label>
                    <label>
                        Seniority
                        <select 
                            value={profile.seniority}
                            onChange={(event) => {
                                setProfile({...profile, seniority: event.target.value})
                            }}
                        >
                            <option value="Graduate">Graduate</option>
                            <option value="Junior">Junior</option>
                            <option value="Mid-level">Mid-level</option>
                            <option value="Senior">Senior</option>
                        </select>
                    </label>
                </section>
                <section className="work-preferences">
                    <h3>Work preferences</h3>
                    <label>
                        <input
                            type="checkbox"
                            checked={profile.work_arrangements.includes("Remote")}
                            onChange={(event) => {
                                const updatedWorkArrangements = event.target.checked
                                    ? [...profile.work_arrangements, "Remote"]
                                    : profile.work_arrangements.filter(
                                        (arrangement) => arrangement !== "Remote"
                                    )

                                setProfile({...profile, work_arrangements: updatedWorkArrangements})
                            }}
                        />
                        Remote
                    </label>
                    <label>
                        <input
                            type="checkbox"
                            checked={profile.work_arrangements.includes("Hybrid")}
                            onChange={(event) => {
                                const updatedWorkArrangements = event.target.checked
                                    ? [...profile.work_arrangements, "Hybrid"]
                                    : profile.work_arrangements.filter(
                                        (arrangement) => arrangement !== "Hybrid"
                                    )

                                setProfile({...profile, work_arrangements: updatedWorkArrangements})
                            }}
                        />
                        Hybrid
                    </label>
                    <label>
                    <input
                            type="checkbox"
                            checked={profile.work_arrangements.includes("On-site")}
                            onChange={(event) => {
                                const updatedWorkArrangements = event.target.checked
                                    ? [...profile.work_arrangements, "On-site"]
                                    : profile.work_arrangements.filter(
                                        (arrangement) => arrangement !== "On-site"
                                    )

                                setProfile({...profile, work_arrangements: updatedWorkArrangements})
                            }}
                        /> 
                        On-site
                    </label>
                </section>
                <section className="skills">
                    <h3>Skills</h3>
                    <label>
                        Preferred skills
                        <input 
                            value={skillsInput}
                            placeholder="e.g. Python, React, Django, SQL"
                            onChange={(event) => setSkillsInput(event.target.value.filter)}
                        />
                    </label>
                </section>
                
                
                <button onClick={handleSave}>
                    Save changes
                </button>
                {saveMessage && <p className="save-message">{saveMessage}</p>}
                {saveError && <p className="save-error">{saveError}</p>}
            </div>
        )    
        }
        </div>
    )
}