from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Job

def job_list(request): 
    jobs = Job.objects.all()
    all_jobs = []
    for job in jobs:
        all_jobs.append({"id": job.id, "title": job.title, "company": job.company, "location": job.location, "job_type": job.job_type})

    return JsonResponse(data=all_jobs, safe=False)


def job_detail(request, job_id):
    job = get_object_or_404(Job,id=job_id)
    return JsonResponse(data={"id": job.id, "title": job.title, "company": job.company, "location": job.location, "job_type": job.job_type})
