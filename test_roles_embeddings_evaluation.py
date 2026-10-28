from sentence_transformers import SentenceTransformer, util
from jobs.evaluation import load_evaluation_data
from scipy.stats import spearmanr
from sklearn.model_selection import train_test_split
from jobs.matching import score_role_relevance
from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

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

X = [[row["similarity"]] for row in result]
y = [[row["expected_relevance"]] for row in result]
cv = KFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Linear regression": LinearRegression(),

    "Polynomial regression (degree 2)": make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        LinearRegression()
    ),

    "Decision tree (depth 2)": DecisionTreeRegressor(
        max_depth=2,
        random_state=42
    ),
}

for name, estimator in models.items():
    scores = cross_val_score(
        estimator,
        X,
        y,
        cv=cv,
        scoring="neg_mean_absolute_error"
    )

    mae_scores = -scores

    print(
        f"{name}: MAE = {mae_scores.mean():.3f} "
        f"(fold std = {mae_scores.std():.3f})"
    )

linear_model = LinearRegression()

oof_predictions = cross_val_predict(
    linear_model,
    X,
    y,
    cv=cv
)

for row, prediction in zip(result, oof_predictions):
    prediction = float(prediction.item())
    prediction = max(0, min(5, prediction))

    row["oof_prediction"] = prediction
    row["oof_error"] = abs(
        row["expected_relevance"] - prediction
    )

worst_predictions = sorted(
    result,
    key=lambda row: row["oof_error"],
    reverse=True
)

print("\nLargest out-of-fold errors:")

for row in worst_predictions[:10]:
    print({
        "target_role": row["target_role"],
        "job_title": row["job_title"],
        "expected": row["expected_relevance"],
        "predicted": round(row["oof_prediction"], 2),
        "error": round(row["oof_error"], 2),
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

keyword_fold_maes = []

for train_indices, test_indices in cv.split(result):
    fold_errors = []
    for index in test_indices:
        row = result[index]
        prediction = score_role_relevance(
            row["job_title"],
            [row["target_role"]]
        ) / 5

        error = abs(row["expected_relevance"] - prediction)
        fold_errors.append(error)

    fold_mae = sum(fold_errors) / len(fold_errors)
    keyword_fold_maes.append(fold_mae)

keyword_cv_mae = sum(keyword_fold_maes) / len(keyword_fold_maes)

print("\nKeyword matcher 5-fold CV MAE:", round(keyword_cv_mae, 3))


print("Keyword test MAE:", round(keyword_mae, 3))
print("BGE test MAE:", round(bge_mae, 3))
