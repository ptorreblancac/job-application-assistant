from datetime import datetime
from .models import Job
from dotenv import load_dotenv
import requests
import os

def fetch_adzuna_jobs():
    load_dotenv()
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    url = "https://api.adzuna.com/v1/api/jobs/es/search/1"

    params = {
        "app_id": app_id, 
        "app_key": app_key,
        "what": "software engineer",
        "where": "Barcelona",
        "results_per_page": 10
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

def import_adzuna_jobs():
    jobs = fetch_adzuna_jobs()
    created_count = 0
    existing_count = 0

    for job in jobs:
        transformed_job = transform_job(job)
        _, created = save_job(transformed_job)
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