from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

SENIORITY_CATEGORIES = {
    "Entry-level": ["Graduate", "Entry-level", "Trainee", "Junior", "Associate"],
    "Intern": ["Intern", "Internship"],
    "Mid-level": ["Mid-level", "Intermediate"],
    "Senior": ["Senior"],
    "Lead/Principal": ["Lead", "Principal", "Staff"]
}

def remove_seniority(job):
    for category, keywords in SENIORITY_CATEGORIES.items():
        for keyword in keywords:
            job = re.sub(r"\b" + keyword + r"\b", "", job, flags=re.IGNORECASE)                

    return job.strip()

def calculate_similarity(job_title,target_roles):
    if isinstance(target_roles, str):
        target_roles = [target_roles]

    job_title = model.encode(job_title)
    max_similarity = 0

    for role in target_roles:
        target_role = model.encode(role)
        similarity = util.cos_sim(job_title, target_role).item()
        max_similarity = max(similarity,max_similarity)

    return max_similarity


def predict_relevance(similarity):
    prediction = (-3.7103 + (9.1598 * similarity))*6
    prediction = max(0, min(30,prediction))
    return prediction

def score_role_relevance(job_title, target_roles):
    job = remove_seniority(job_title)
    similarity = calculate_similarity(job,target_roles)
    return predict_relevance(similarity)

def score_skills(job, preferred_skills):
    if not preferred_skills: 
        return 0
    
    job_text = (job.description + " " + job.requirements + " " + job.qualifications)

    matching_skills = 0
    for skill in preferred_skills:
        if skill.lower() in job_text.lower():
            matching_skills += 1

    return (matching_skills/len(preferred_skills))*35

def detect_seniority(text):
    for category, keywords in SENIORITY_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                return category

    return None

def score_seniority(job, profile_seniority):
    fields = []
    fields.append(job.title)
    fields.append(job.description)
    fields.append(job.requirements)

    for field in fields:
        seniority = detect_seniority(field)
        if (seniority is not None and seniority != profile_seniority):
            return 0
        elif (seniority == profile_seniority):
            return 15
    return 0

def score_location(job, profile_location):
    if not job.location or not profile_location:
        return 0 
    elif job.location.strip().lower() == profile_location.strip().lower():
        return 10

    return 0

def score_work_arrangement(job, preferred_arrangements):
    if not preferred_arrangements:
        return 0

    job_text = (job.description + " " + job.requirements + " " + job.qualifications).lower()

    for arrang in preferred_arrangements:
        if arrang.lower() in job_text:
            return 10

    return 0

def calculate_job_match(job,profile):  
    points = (
        score_role_relevance(job.title,profile.target_role) 
        + score_skills(job,profile.preferred_skills) 
        + score_seniority(job,profile.seniority) 
        + score_location(job,profile.location) 
        + score_work_arrangement(job,profile.work_arrangements)
    )

    return points

#similarity = calculate_similarity(
#    "Junior Software Engineer",
#    "Software Engineer"
#)

#score = predict_relevance(similarity)

#print("Similarity:", similarity)
#print("Predicted relevance:", score)
