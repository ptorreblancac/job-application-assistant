from django.test import TestCase
from .models import Job

class JobListTests(TestCase):

    def test_job_list_returns_200(self):
        response = self.client.get("/jobs/")
        self.assertEqual(response.status_code, 200)

    def test_job_list_returns_job_data(self):
        Job.objects.create(
            title =  "Backend Developer",
            company =  "Test Company",
            location =  "Barcelona",
            job_type = "Full-time",
            description = "none",
            requirements = "none",
            qualifications = "none",
            posting_link = "https://example.com/test-job"
        )

        response = self.client.get("/jobs/")
        self.assertEqual(response.json()[0]['title'], "Backend Developer")

    def test_job_detail_returns_404_for_missing_job(self):
        response = self.client.get("/jobs/999/")
        self.assertEqual(response.status_code, 404)