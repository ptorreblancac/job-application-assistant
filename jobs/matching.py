from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

SENIORITY_CATEGORIES = {
    "Entry-level": ["Graduate", "Entry-level", "Trainee", "Junior", "Associate"],
    "Intern": ["Intern", "Internship"],
    "Mid-level": ["Mid-level", "Intermediate"],
    "Senior": ["Senior"],
    "Lead/Principal": ["Lead", "Principal", "Staff"]
}

def calculate_similarity(job_title,target_role):
    job_title = model.encode(job_title)
    target_role = model.encode(target_role)

    similarity = util.cos_sim(job_title, target_role).item()
    return similarity


def predict_relevance(similarity):
    prediction = (-3.7103 + (9.1598 * similarity))*6
    prediction = max(0, min(30,prediction))
    return prediction

def score_role_relevance(job_title, target_roles):
    for role in target_roles:
        if role.lower() in job_title.lower():
            return 25
    
    return 0

def score_skills(job, preferred_skills):
    if not preferred_skills: 
        return 0
    
    job_text = (job.description + " " + job.requirements + " " + job.qualifications)

    matching_skills = 0
    for skill in preferred_skills:
        if skill.lower() in job_text.lower():
            matching_skills += 1

    return (matching_skills/len(preferred_skills))*30

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

    

#similarity = calculate_similarity(
#    "Junior Software Engineer",
#    "Software Engineer"
#)

#score = predict_relevance(similarity)

#print("Similarity:", similarity)
#print("Predicted relevance:", score)

from types import SimpleNamespace
from jobs.matching import score_work_arrangement

job1 = SimpleNamespace(
    description="We offer remote work opportunities.",
    requirements="Python experience required.",
    qualifications=""
)

job2 = SimpleNamespace(
    description="This is a hybrid position.",
    requirements="",
    qualifications=""
)

job3 = SimpleNamespace(
    description="Work from our Barcelona office.",
    requirements="",
    qualifications=""
)

job4 = SimpleNamespace(
    description="REMOTE position available.",
    requirements="",
    qualifications=""
)

# 1. Remote preference matches
print(score_work_arrangement(job1, ["Remote"]))  # 10

# 2. Hybrid preference matches
print(score_work_arrangement(job2, ["Hybrid"]))  # 10

# 3. No matching arrangement
print(score_work_arrangement(job3, ["Remote"]))  # 0

# 4. Case-insensitive matching
print(score_work_arrangement(job4, ["Remote"]))  # 10

# 5. Multiple preferences, one matches
print(score_work_arrangement(job2, ["Remote", "Hybrid"]))  # 10

# 6. Empty preferences
print(score_work_arrangement(job1, []))  # 0