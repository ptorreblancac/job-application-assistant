from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def __str__(self):
        return f"{self.title} at {self.company}"
    
class SearchProfile(models.Model):
    target_role = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    seniority = models.CharField(max_length=200, blank=True)
    work_arrangements = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    jobs = models.ManyToManyField(
        Job,
        through="ProfileJobMatch",
        related_name="search_profiles",
        blank=True
    )

    def __str__(self):
        return self.target_role

class ProfileJobMatch(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["search_profile", "job"],
                name="unique_profile_job"
            )
        ]

    search_profile = models.ForeignKey(
        SearchProfile,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )
    relevance_score = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title} - {self.search_profile.target_role}"