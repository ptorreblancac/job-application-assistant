from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Job, ProfileJobMatch

def job_list(request): 
    job_type = request.GET.get("job_type")
    company = request.GET.get("company")

    jobs = Job.objects.all()

    if job_type is not None:
        jobs = jobs.filter(job_type=job_type) 

    if company is not None:
        jobs = jobs.filter(company=company) 

    all_jobs = []
    for job in jobs:
        match = ProfileJobMatch.objects.filter(
            search_profile_id=1,
            job=job
        ).first()

        if match:
            relevance_score = match.relevance_score
        else:
            relevance_score = None

        all_jobs.append({"id": job.id, "title": job.title, "company": job.company, "location": job.location, "job_type": job.job_type, "relevance_score": relevance_score})

    return JsonResponse(data=all_jobs, safe=False)


def job_detail(request, job_id):
    job = get_object_or_404(Job,id=job_id)
    return JsonResponse(data={"id": job.id, "title": job.title, "company": job.company, "location": job.location, "job_type": job.job_type})
