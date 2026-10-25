from sentence_transformers import SentenceTransformer, util
from jobs.evaluation import load_evaluation_data

model = SentenceTransformer("all-MiniLM-L6-v2")

data = load_evaluation_data()
job_title = model.encode(data[1]["job_title"])
target_role = model.encode(data[1]["target_role"])

print(data[1]["job_title"])
print(data[1]["target_role"])
print(util.cos_sim(job_title, target_role).item())