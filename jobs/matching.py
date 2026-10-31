from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def calculate_similarity(job_title,target_role):
    job_title = model.encode(job_title)
    target_role = model.encode(target_role)

    similarity = util.cos_sim(job_title, target_role).item()
    return similarity


def predict_relevance(similarity):
    prediction = -3.7103 + (9.1598 * similarity)
    prediction = max(0, min(5,prediction))
    return prediction

def score_role_relevance(job_title, target_roles):
    for role in target_roles:
        if role.lower() in job_title.lower():
            return 25
    
    return 0


similarity = calculate_similarity(
    "Junior Software Engineer",
    "Software Engineer"
)

score = predict_relevance(similarity)

print("Similarity:", similarity)
print("Predicted relevance:", score)