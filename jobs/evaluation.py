import csv
from jobs.matching import score_role_relevance
from pathlib import Path

folder = Path(__file__).parent
path = folder / "data" / "role_matching_evaluation.csv"

def load_evaluation_data():
    with open(path,mode="r",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        result = list(reader)
    return result


def evaluate_role_matching():
    sample_data = load_evaluation_data()
    result = []

    for row in sample_data:
        predicted_relevance = score_role_relevance(row["job_title"],[row["target_role"]])/5
        expected_relevance = int(row["expected_relevance"])
        result.append({
            "target_role": row["target_role"],
            "job_title": row["job_title"],
            "expected_relevance": expected_relevance,
            "predicted_relevance": predicted_relevance,
            "error": abs(expected_relevance - predicted_relevance)
        })

    return result

def calculate_mae(results):
    total_error = 0
    for row in results:
        total_error += abs(row["expected_relevance"] - row["predicted_relevance"])
    error = total_error/len(results)
    return error

def count_incorrect_predictions(results):
    count = 0
    for row in results:
        error = abs(row["expected_relevance"] - row["predicted_relevance"])
        if (error > 0):
            count += 1

    return count

if __name__ == "__main__":
    data = evaluate_role_matching()
    print(count_incorrect_predictions(data))
    print(calculate_mae(data))
    print(len(data))
    print(data[:5])