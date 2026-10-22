from django.test import TestCase, SimpleTestCase
from .models import Job
from jobs.matching import score_role_relevance

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

    def test_job_list_can_filter_by_job_type(self):
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

        Job.objects.create(
            title =  "Frontend Developer",
            company =  "Test2 Company",
            location =  "Barcelona",
            job_type = "Internship",
            description = "none",
            requirements = "none",
            qualifications = "none",
            posting_link = "https://anotherexample.com/test-job"
        )

        response = self.client.get("/jobs/?job_type=Internship")
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),1)
        self.assertEqual(response.json()[0]['title'], "Frontend Developer")

    def test_job_list_can_filter_by_company(self):
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
    
            Job.objects.create(
                title =  "Frontend Developer",
                company =  "Test2 Company",
                location =  "Barcelona",
                job_type = "Internship",
                description = "none",
                requirements = "none",
                qualifications = "none",
                posting_link = "https://anotherexample.com/test-job"
            )
    
            response = self.client.get("/jobs/?company=Test Company")
            self.assertEqual(response.status_code,200)
            self.assertEqual(len(response.json()),1)
            self.assertEqual(response.json()[0]['title'], "Backend Developer")

    def test_job_list_can_filter_by_job_type_and_company(self):
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
    
            Job.objects.create(
                title =  "Frontend Developer",
                company =  "Test2 Company",
                location =  "Barcelona",
                job_type = "Internship",
                description = "none",
                requirements = "none",
                qualifications = "none",
                posting_link = "https://anotherexample.com/test-job"
            )
    
            response = self.client.get("/jobs/?job_type=Internship&company=Test2 Company")
            self.assertEqual(response.status_code,200)
            self.assertEqual(len(response.json()),1)
            self.assertEqual(response.json()[0]['title'], "Frontend Developer")


    def test_job_list_filter_with_no_matches(self):
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
    
            Job.objects.create(
                title =  "Frontend Developer",
                company =  "Test2 Company",
                location =  "Barcelona",
                job_type = "Internship",
                description = "none",
                requirements = "none",
                qualifications = "none",
                posting_link = "https://anotherexample.com/test-job"
            )
    
            response = self.client.get("/jobs/?job_type=Internship&company=Sony")
            self.assertEqual(response.status_code,200)
            self.assertEqual(len(response.json()),0)

class ScoreRoleRelevanceTests(SimpleTestCase):

    def test_case_insensitive_match(self):
        job_title = "BACKEND DEVELOPER"
        target_roles = ["Backend Developer"]

        result = score_role_relevance(job_title,target_roles)
        self.assertEqual(result,30)

    def test_partial_title_match(self):
        job_title = "Junior Backend Developer"
        target_roles = ["Software Developer", "Backend Developer", "Data Engineer"]

        result = score_role_relevance(job_title,target_roles)
        self.assertEqual(result,30)

    def test_no_match(self):
        job_title = "Senior Data Scientist"
        target_roles = ["Software Developer", "Backend Developer", "Data Engineer"]

        result = score_role_relevance(job_title,target_roles)
        self.assertEqual(result,0)
