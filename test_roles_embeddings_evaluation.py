from sentence_transformers import SentenceTransformer, util
from jobs.evaluation import load_evaluation_data
from scipy.stats import spearmanr

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

data = load_evaluation_data()
result = []

for row in data:    
    job_title = model.encode(row["job_title"])
    target_role = model.encode(row["target_role"])

    similarity = util.cos_sim(job_title, target_role).item()
    expected_relevance = int(row["expected_relevance"])
    result.append({
        "target_role": row["target_role"],
        "job_title": row["job_title"],
        "expected_relevance": expected_relevance,
        "similarity": similarity,
    })

similarities = [row["similarity"] for row in result]
expected_scores = [row["expected_relevance"] for row in result]

correlation, p_value = spearmanr(similarities, expected_scores)

print("Spearman correlation:", correlation)
print("P-value:", p_value)

print(result)
