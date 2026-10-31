from datetime import datetime
from .models import Job, ProfileJobMatch
from dotenv import load_dotenv
import requests
import os
from .matching import calculate_similarity, predict_relevance

def fetch_adzuna_jobs(profile):
    load_dotenv()
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    url = "https://api.adzuna.com/v1/api/jobs/es/search/1"

    params = {
        "app_id": app_id, 
        "app_key": app_key,
        "what": profile.target_role,
        "results_per_page": 10
    }

    if profile.location:
        params["where"] = profile.location

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

def import_adzuna_jobs(profile):
    jobs = fetch_adzuna_jobs(profile)
    created_count = 0
    existing_count = 0

    for job in jobs:
        transformed_job = transform_job(job)
        job_object, created = save_job(transformed_job)

        similarity = calculate_similarity(
            job_object.title,
            profile.target_role
        )

        score = predict_relevance(similarity)

        score = round(score)

        ProfileJobMatch.objects.update_or_create(
            search_profile=profile,
            job=job_object,
            defaults={
                "relevance_score": score
            }
        )

        if created:
            created_count += 1
        else:
            existing_count += 1

    return created_count, existing_count

def save_job(transformed):
    transformed_copy = transformed.copy()
    transformed_copy.pop("posting_link")
    job, created = Job.objects.get_or_create(
        posting_link = transformed["posting_link"],
        defaults = transformed_copy
    )

    return job, created

def transform_job(job):
    result = {
        "title": job["title"],
        "company": job["company"]["display_name"],
        "location": job["location"]["display_name"],
        "description": job["description"],
        "posting_link": job["redirect_url"],
        "date_posted": datetime.fromisoformat(
            job["created"].replace("Z", "+00:00")
        ).date(),
        "job_type": "",
        "requirements": "",
        "qualifications": "",
        "pay": ""
    }
    return result