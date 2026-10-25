from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

target_role = "Backend Developer"

job_titles = [
    "Junior Backend Engineer",
    "API Developer",
    "Frontend Developer",
    "Data Engineer",
    "Graphic Designer",
]

target_vector = model.encode(target_role)

for title in job_titles:
    job_vector = model.encode(title)
    similarity = util.cos_sim(target_vector, job_vector)
    print(title, similarity.item())