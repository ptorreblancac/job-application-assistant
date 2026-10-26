from sentence_transformers import SentenceTransformer, util
from jobs.evaluation import load_evaluation_data
from scipy.stats import spearmanr
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from jobs.matching import score_role_relevance

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

calibration_data, test_data = train_test_split(
    result,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

X_calibration = [
    [row["similarity"]]
    for row in calibration_data
]

y_calibration = [
    row["expected_relevance"]
    for row in calibration_data
]

model.fit(X_calibration, y_calibration)
print("Regression coefficient:", model.coef_[0])
print("Regression intercept:", model.intercept_)

for row in test_data:
    prediction = model.predict([[row["similarity"]]])[0]

    prediction = max(0, min(5, prediction))

    row["predicted_relevance"] = prediction
    row["error"] = abs(
        row["expected_relevance"] - prediction
    )

print("Calibration examples:", len(calibration_data))
print("Test examples:", len(test_data))

similarities = [row["similarity"] for row in result]
expected_scores = [row["expected_relevance"] for row in result]

correlation, p_value = spearmanr(similarities, expected_scores)

print("Spearman correlation:", correlation)
print("P-value:", p_value)

print(result)

print("\nBGE test predictions:")

for row in test_data:
    print({
        "target_role": row["target_role"],
        "job_title": row["job_title"],
        "expected": row["expected_relevance"],
        "predicted": round(row["predicted_relevance"], 2),
        "error": round(row["error"], 2),
    })

total_error = 0

for row in test_data:
    total_error += row["error"]

bge_mae = total_error / len(test_data)

print("BGE test MAE:", round(bge_mae, 3))


keyword_errors = []

for row in test_data:
    prediction = score_role_relevance(
        row["job_title"],
        [row["target_role"]]
    ) / 5

    error = abs(row["expected_relevance"] - prediction)
    keyword_errors.append(error)

keyword_mae = sum(keyword_errors) / len(keyword_errors)

print("Keyword test MAE:", round(keyword_mae, 3))
print("BGE test MAE:", round(bge_mae, 3))
