from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Job, ProfileJobMatch, SearchProfile
from .services import recalculate_profile_matches
import json

def job_list(request): 
    job_type = request.GET.get("job_type")
    company = request.GET.get("company")

    jobs = Job.objects.all()

    if job_type is not None:
        jobs = jobs.filter(job_type=job_type) 

    if company is not None:
        jobs = jobs.filter(company=company) 

    profile = SearchProfile.objects.first()   

    all_jobs = []
    for job in jobs:
        match = None

        if profile: 
            match = ProfileJobMatch.objects.filter(
                search_profile_id=profile,
                job=job
            ).first()

        if match:
            relevance_score = match.relevance_score
        else:
            relevance_score = None

        all_jobs.append({"id": job.id, "title": job.title, "company": job.company, "location": job.location, "country": job.country, "job_type": job.job_type, "posting_link": job.posting_link, "relevance_score": relevance_score, "date_posted": job.date_posted.isoformat() if job.date_posted else None})

    return JsonResponse(data=all_jobs, safe=False)


def job_detail(request, job_id):
    job = get_object_or_404(Job,id=job_id)
    return JsonResponse(data={"id": job.id, "title": job.title, "company": job.company, "location": job.location, "country": job.country, "job_type": job.job_type, "posting_link": job.posting_link, "date_posted": job.date_posted.isoformat() if job.date_posted else None})

def profile_detail(request, profile_id):
    profile = get_object_or_404(SearchProfile, id=profile_id)
    return JsonResponse(data={"id":profile.id, "target_role": profile.target_role, "location": profile.location, "country": profile.country, "seniority": profile.seniority, "work_arrangements": profile.work_arrangements, "preferred_skills": profile.preferred_skills})

@csrf_exempt
@require_http_methods(["PUT"])
def profile_update(request, profile_id):
    profile = get_object_or_404(SearchProfile, id=profile_id)
    data = json.loads(request.body)

    profile.target_role = data["target_role"]
    profile.location = data["location"]
    profile.country = data["country"]
    profile.seniority = data["seniority"]
    profile.work_arrangements = data["work_arrangements"]
    profile.preferred_skills = data["preferred_skills"]    

    profile.save()
    recalculate_profile_matches(profile)
    return JsonResponse(data={"id":profile.id, "target_role": profile.target_role, "location": profile.location, "country": profile.country, "seniority": profile.seniority, "work_arrangements": profile.work_arrangements, "preferred_skills": profile.preferred_skills})


def active_profile(request):
    profile = SearchProfile.objects.first()

    if not profile:
        return JsonResponse({"error": "No search profile found"}, status=404)

    return JsonResponse({"id": profile.id})