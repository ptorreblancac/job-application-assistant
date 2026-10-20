from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    pay = models.CharField(max_length=200, blank=True)
    job_type = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    date_posted = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    posting_link = models.URLField(unique=True)
    
