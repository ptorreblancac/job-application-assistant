from django.test import TestCase, SimpleTestCase
from .models import Job,  SearchProfile, ProfileJobMatch
from jobs.matching import (
    score_role_relevance,
    score_skills,
    score_seniority,
    score_location,
    score_work_arrangement,
    calculate_job_match,
)
import json
from unittest.mock import patch
from django.urls import reverse

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
        job_title = "Backend Developer"
        target_roles = ["Software Developer", "Backend Developer", "Data Engineer"]

        result = score_role_relevance(job_title,target_roles)
        self.assertAlmostEqual(result,30)

    def test_related_but_not_exact_match(self):
        job_title = "Senior Data Scientist"
        target_roles = ["Software Developer", "Backend Developer", "Data Engineer"]

        result = score_role_relevance(job_title,target_roles)
        self.assertLess(result,30)

    def test_single_target_role(self):
        result = score_role_relevance(
            "Software Engineer",
            "Software Engineer"
        )
        self.assertEqual(result, 30)

    def test_seniority_does_not_affect_role_relevance(self):
        titles = [
            "Software Engineer",
            "Junior Software Engineer",
            "Senior Software Engineer",
            "Graduate Software Engineer",
            "Lead Software Engineer"
        ]

        for title in titles:
            with self.subTest(title=title):
                result = score_role_relevance(
                    title,
                    "Software Engineer"
                )
                self.assertEqual(result, 30)

class ScoreSkillsTests(SimpleTestCase):

    def test_all_skills_match(self):
        job = Job(
            description="We use Python, React and Django.",
            requirements="SQL experience required.",
            qualifications=""
        )
        preferred_skills = ["Python", "React", "Django", "SQL"]

        result = score_skills(job, preferred_skills)

        self.assertEqual(result, 35)

    def test_partial_skills_match(self):
        job = Job(
            description="We use Python and React.",
            requirements="",
            qualifications=""
        )
        preferred_skills = ["Python", "React", "Django", "SQL"]

        result = score_skills(job, preferred_skills)

        self.assertEqual(result, 17.5)

    def test_no_preferred_skills(self):
        job = Job(
            description="We use Python and React.",
            requirements="",
            qualifications=""
        )
        result = score_skills(job, [])

        self.assertEqual(result, 0)

    def test_no_skills_match(self):
        job = Job(
            description="We are looking for a project manager.",
            requirements="Management experience required.",
            qualifications=""
        )
        preferred_skills = ["Python", "React"]

        result = score_skills(job, preferred_skills)

        self.assertEqual(result, 0)

    def test_case_insensitive_skills(self):
        job = Job(
            description="Experience with PYTHON and react.",
            requirements="",
            qualifications=""
        )
        preferred_skills = ["Python", "React"]

        result = score_skills(job, preferred_skills)

        self.assertEqual(result, 35)

    def test_skills_across_different_fields(self):
        job = Job(
            description="Experience with Python.",
            requirements="Knowledge of React.",
            qualifications="Django experience."
        )
        preferred_skills = ["Python", "React", "Django"]

        result = score_skills(job, preferred_skills)

        self.assertEqual(result, 35)


class ScoreSeniorityTests(SimpleTestCase):

    def test_matching_seniority(self):
        job = Job(
            title="Senior Software Engineer",
            description="",
            requirements=""
        )

        result = score_seniority(job, "Senior")

        self.assertEqual(result, 15)

    def test_different_seniority(self):
        job = Job(
            title="Junior Software Engineer",
            description="",
            requirements=""
        )

        result = score_seniority(job, "Senior")

        self.assertEqual(result, 0)

    def test_unspecified_seniority(self):
        job = Job(
            title="Software Engineer",
            description="Develop software applications.",
            requirements="Python experience."
        )

        result = score_seniority(job, "Senior")

        self.assertEqual(result, 0)

    def test_seniority_in_description(self):
        job = Job(
            title="Software Engineer",
            description="We are looking for a Senior developer.",
            requirements=""
        )

        result = score_seniority(job, "Senior")

        self.assertEqual(result, 15)

    def test_seniority_in_requirements(self):
        job = Job(
            title="Software Engineer",
            description="",
            requirements="Candidates should have Senior-level experience."
        )

        result = score_seniority(job, "Senior")

        self.assertEqual(result, 15)


class ScoreLocationTests(SimpleTestCase):

    def test_matching_location(self):
        job = Job(location="Barcelona")

        result = score_location(job, "Barcelona")

        self.assertEqual(result, 10)

    def test_different_location(self):
        job = Job(location="Madrid")

        result = score_location(job, "Barcelona")

        self.assertEqual(result, 0)

    def test_case_insensitive_location(self):
        job = Job(location="BARCELONA")

        result = score_location(job, "Barcelona")

        self.assertEqual(result, 10)

    def test_location_with_extra_spaces(self):
        job = Job(location=" Barcelona ")

        result = score_location(job, "Barcelona")

        self.assertEqual(result, 10)

    def test_missing_job_location(self):
        job = Job(location="")

        result = score_location(job, "Barcelona")

        self.assertEqual(result, 0)

    def test_missing_profile_location(self):
        job = Job(location="Barcelona")

        result = score_location(job, "")

        self.assertEqual(result, 0)


class ScoreWorkArrangementTests(SimpleTestCase):

    def test_matching_work_arrangement(self):
        job = Job(
            description="This is an on-site position.",
            requirements="",
            qualifications=""
        )

        result = score_work_arrangement(job, ["On-site"])

        self.assertEqual(result, 10)

    def test_no_preferred_arrangements(self):
        job = Job(
            description="Remote position.",
            requirements="",
            qualifications=""
        )

        result = score_work_arrangement(job, [])

        self.assertEqual(result, 0)

    def test_no_arrangement_mentioned(self):
        job = Job(
            description="We are looking for a software developer.",
            requirements="",
            qualifications=""
        )

        result = score_work_arrangement(job, ["Remote"])

        self.assertEqual(result, 0)

    def test_multiple_preferred_arrangements(self):
        job = Job(
            description="This is a remote position.",
            requirements="",
            qualifications=""
        )

        result = score_work_arrangement(
            job,
            ["On-site", "Hybrid", "Remote"]
        )

        self.assertEqual(result, 10)

    def test_case_insensitive_arrangement(self):
        job = Job(
            description="REMOTE position available.",
            requirements="",
            qualifications=""
        )

        result = score_work_arrangement(job, ["Remote"])

        self.assertEqual(result, 10)


class CalculateJobMatchTests(SimpleTestCase):

    def test_maximum_match_score(self):
        job = Job(
            title="Senior Software Engineer",
            location="Barcelona",
            description="Python, React, Django and SQL. On-site position.",
            requirements="",
            qualifications=""
        )

        profile = type("Profile", (), {
            "target_role": "Software Engineer",
            "preferred_skills": ["Python", "React", "Django", "SQL"],
            "seniority": "Senior",
            "location": "Barcelona",
            "work_arrangements": ["On-site"]
        })()

        result = calculate_job_match(job, profile)

        self.assertEqual(result, 100)

    def test_combined_score_is_sum_of_components(self):
        job = Job(
            title="Software Engineer",
            location="Barcelona",
            description="Python experience required. On-site position.",
            requirements="",
            qualifications=""
        )

        profile = type("Profile", (), {
            "target_role": "Software Engineer",
            "preferred_skills": ["Python", "React"],
            "seniority": "Senior",
            "location": "Barcelona",
            "work_arrangements": ["On-site"]
        })()

        result = calculate_job_match(job, profile)

        self.assertAlmostEqual(result, 67.5)

class ProfileAPITests(TestCase):

    def setUp(self):
        self.profile = SearchProfile.objects.create(
            target_role="Software Engineer",
            location="Barcelona",
            country="Spain",
            seniority="Graduate",
            work_arrangements=["On-site"],
            preferred_skills=["Python", "React"]
        )

        self.profile_url = f"/jobs/profiles/{self.profile.id}/"
        self.update_url = f"/jobs/profiles/{self.profile.id}/update/"

    def test_get_profile_returns_200(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)

    def test_get_profile_returns_correct_data(self):
        response = self.client.get(self.profile_url)
        data = response.json()

        self.assertEqual(data["id"], self.profile.id)
        self.assertEqual(data["target_role"], "Software Engineer")
        self.assertEqual(data["location"], "Barcelona")
        self.assertEqual(data["country"], "Spain")
        self.assertEqual(data["seniority"], "Graduate")
        self.assertEqual(data["work_arrangements"], ["On-site"])
        self.assertEqual(data["preferred_skills"], ["Python", "React"])

    def test_get_nonexistent_profile_returns_404(self):
        response = self.client.get("/jobs/profiles/9999/")

        self.assertEqual(response.status_code, 404)

    def test_update_profile_returns_200(self):
        data = {
            "target_role": "Backend Developer",
            "location": "Madrid",
            "country": "Spain",
            "seniority": "Junior",
            "work_arrangements": ["Remote"],
            "preferred_skills": ["Python", "Django"]
        }

        with patch("jobs.views.recalculate_profile_matches"):
            response = self.client.put(
                self.update_url,
                data=json.dumps(data),
                content_type="application/json"
            )

        self.assertEqual(response.status_code, 200)

    def test_update_profile_returns_updated_data(self):
        data = {
            "target_role": "Backend Developer",
            "location": "Madrid",
            "country": "Spain",
            "seniority": "Junior",
            "work_arrangements": ["Remote"],
            "preferred_skills": ["Python", "Django"]
        }

        with patch("jobs.views.recalculate_profile_matches"):
            response = self.client.put(
                self.update_url,
                data=json.dumps(data),
                content_type="application/json"
            )

        response_data = response.json()

        self.assertEqual(response_data["target_role"], "Backend Developer")
        self.assertEqual(response_data["location"], "Madrid")
        self.assertEqual(response_data["preferred_skills"], ["Python", "Django"])

    def test_update_profile_persists_changes(self):
        data = {
            "target_role": "Full-Stack Developer",
            "location": "Barcelona",
            "country": "Spain",
            "seniority": "Graduate",
            "work_arrangements": ["Hybrid"],
            "preferred_skills": ["JavaScript", "React"]
        }

        with patch("jobs.views.recalculate_profile_matches"):
            self.client.put(
                self.update_url,
                data=json.dumps(data),
                content_type="application/json"
            )

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.target_role, "Full-Stack Developer")
        self.assertEqual(self.profile.work_arrangements, ["Hybrid"])
        self.assertEqual(self.profile.preferred_skills, ["JavaScript", "React"])

    @patch("jobs.views.recalculate_profile_matches")
    def test_update_profile_recalculates_matches(self, mock_recalculate):
        data = {
            "target_role": "Backend Developer",
            "location": "Barcelona",
            "country": "Spain",
            "seniority": "Graduate",
            "work_arrangements": ["On-site"],
            "preferred_skills": ["Python", "Django"]
        }

        self.client.put(
            self.update_url,
            data=json.dumps(data),
            content_type="application/json"
        )

        mock_recalculate.assert_called_once()

        updated_profile = mock_recalculate.call_args[0][0]
        self.assertEqual(updated_profile.id, self.profile.id)

    def test_update_nonexistent_profile_returns_404(self):
        data = {
            "target_role": "Backend Developer",
            "location": "Barcelona",
            "country": "Spain",
            "seniority": "Graduate",
            "work_arrangements": ["On-site"],
            "preferred_skills": ["Python"]
        }

        response = self.client.put(
            "/jobs/profiles/9999/update/",
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)

    def test_update_profile_only_accepts_put(self):
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 405)


class JobDetailTests(TestCase):

    def setUp(self):
        self.job = Job.objects.create(
            title="Junior Software Engineer",
            company="Example Company",
            location="Barcelona",
            country="Spain",
            job_type="Full-time",
            description="Python and Django development.",
            requirements="Python",
            qualifications="",
            posting_link="https://example.com/job/1"
        )

    def test_get_job_detail_returns_200(self):
        response = self.client.get(f"/jobs/{self.job.id}/")

        self.assertEqual(response.status_code, 200)

    def test_get_job_detail_returns_correct_data(self):
        response = self.client.get(f"/jobs/{self.job.id}/")
        data = response.json()

        self.assertEqual(data["id"], self.job.id)
        self.assertEqual(data["title"], "Junior Software Engineer")
        self.assertEqual(data["company"], "Example Company")
        self.assertEqual(data["location"], "Barcelona")
        self.assertEqual(data["country"], "Spain")
        self.assertEqual(data["job_type"], "Full-time")
        self.assertEqual(data["posting_link"], "https://example.com/job/1")

    def test_get_job_detail_returns_null_date_when_missing(self):
        response = self.client.get(f"/jobs/{self.job.id}/")

        self.assertIsNone(response.json()["date_posted"])


class RecalculateProfileMatchesTests(TestCase):

    def setUp(self):
        self.profile = SearchProfile.objects.create(
            target_role="Software Engineer",
            location="Barcelona",
            country="Spain",
            seniority="Graduate",
            work_arrangements=["On-site"],
            preferred_skills=["Python", "React"]
        )

        self.job = Job.objects.create(
            title="Software Engineer",
            company="Example Company",
            location="Barcelona",
            country="Spain",
            job_type="Full-time",
            description="Python and React development. On-site position.",
            requirements="",
            qualifications="",
            posting_link="https://example.com/job/1"
        )

        self.match = ProfileJobMatch.objects.create(
            search_profile=self.profile,
            job=self.job,
            relevance_score=50
        )

    @patch("jobs.services.calculate_job_match", return_value=85.4)
    def test_recalculates_existing_match(self, mock_calculate):
        from jobs.services import recalculate_profile_matches

        recalculate_profile_matches(self.profile)

        self.match.refresh_from_db()

        self.assertEqual(self.match.relevance_score, 85)
        mock_calculate.assert_called_once_with(self.job, self.profile)

    @patch("jobs.services.calculate_job_match", return_value=72.6)
    def test_recalculation_rounds_score(self, mock_calculate):
        from jobs.services import recalculate_profile_matches

        recalculate_profile_matches(self.profile)

        self.match.refresh_from_db()

        self.assertEqual(self.match.relevance_score, 73)

    @patch("jobs.services.calculate_job_match", return_value=90)
    def test_recalculates_only_matches_for_given_profile(self, mock_calculate):
        other_profile = SearchProfile.objects.create(
            target_role="Backend Developer",
            location="Madrid",
            country="Spain",
            seniority="Junior",
            work_arrangements=["Remote"],
            preferred_skills=["Django"]
        )

        other_match = ProfileJobMatch.objects.create(
            search_profile=other_profile,
            job=self.job,
            relevance_score=40
        )

        from jobs.services import recalculate_profile_matches

        recalculate_profile_matches(self.profile)

        self.match.refresh_from_db()
        other_match.refresh_from_db()

        self.assertEqual(self.match.relevance_score, 90)
        self.assertEqual(other_match.relevance_score, 40)

    @patch("jobs.services.calculate_job_match", return_value=80)
    def test_does_not_create_matches_for_unmatched_jobs(self, mock_calculate):
        another_job = Job.objects.create(
            title="Backend Developer",
            company="Another Company",
            location="Barcelona",
            country="Spain",
            job_type="Full-time",
            description="Django development.",
            requirements="",
            qualifications="",
            posting_link="https://example.com/job/2"
        )

        from jobs.services import recalculate_profile_matches

        recalculate_profile_matches(self.profile)

        self.assertFalse(
            ProfileJobMatch.objects.filter(
                search_profile=self.profile,
                job=another_job
            ).exists()
        )

    def test_recalculation_with_no_matches_does_not_fail(self):
        empty_profile = SearchProfile.objects.create(
            target_role="Frontend Developer",
            location="Barcelona",
            country="Spain",
            seniority="Graduate"
        )

        from jobs.services import recalculate_profile_matches

        recalculate_profile_matches(empty_profile)

        self.assertEqual(
            ProfileJobMatch.objects.filter(
                search_profile=empty_profile
            ).count(),
            0
        )


@patch("jobs.services.calculate_job_match", return_value=88)
def test_profile_update_recalculates_existing_match(self, mock_calculate):
    job = Job.objects.create(
        title="Backend Developer",
        company="Example Company",
        location="Barcelona",
        country="Spain",
        job_type="Full-time",
        description="Python and Django development.",
        requirements="",
        qualifications="",
        posting_link="https://example.com/job/3"
    )

    match = ProfileJobMatch.objects.create(
        search_profile=self.profile,
        job=job,
        relevance_score=40
    )

    data = {
        "target_role": "Backend Developer",
        "location": "Barcelona",
        "country": "Spain",
        "seniority": "Graduate",
        "work_arrangements": ["On-site"],
        "preferred_skills": ["Python", "Django"]
    }

    response = self.client.put(
        self.update_url,
        data=json.dumps(data),
        content_type="application/json"
    )

    match.refresh_from_db()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(match.relevance_score, 88)
    mock_calculate.assert_called_once()