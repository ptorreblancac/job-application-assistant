import os
import requests
from dotenv import load_dotenv
from datetime import datetime

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
data = response.json()

print(data.keys())
print(len(data.get("results", [])))

first_job = data["results"][0]
print(first_job.keys())
print("title " + first_job["title"])
print(first_job["company"])
print(first_job["location"])
print(first_job["created"])
print(first_job["description"])
print(first_job["redirect_url"])
print(first_job["category"])

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

transformed = transform_job(first_job)
print(transformed)
print(transformed["date_posted"])
print(type(transformed["date_posted"]))