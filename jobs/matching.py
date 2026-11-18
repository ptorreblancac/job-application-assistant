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



#similarity = calculate_similarity(
#    "Junior Software Engineer",
#    "Software Engineer"
#)

#score = predict_relevance(similarity)

#print("Similarity:", similarity)
#print("Predicted relevance:", score)

from types import SimpleNamespace

test_job = SimpleNamespace(
    description="We are looking for a developer with Python and Django experience.",
    requirements="Knowledge of SQL and database management.",
    qualifications="Previous experience with React is desirable."
)

preferred_skills = ["Java", "AWS", "Docker", "Node.js"]

score = score_skills(test_job, preferred_skills)

print("Actual score:", score)

print(detect_seniority("Junior Software Engineer"))
print(detect_seniority("Graduate Developer"))
print(detect_seniority("Software Engineer Intern"))
print(detect_seniority("Senior Backend Developer"))
print(detect_seniority("Lead Software Engineer"))
print(detect_seniority("Software Engineer"))