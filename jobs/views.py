from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def job_list(request): 
    return JsonResponse(data={"name": "app", "count": 2})