from django.core.management.base import BaseCommand
from jobs.models import SearchProfile
from jobs.services import import_adzuna_jobs

class Command(BaseCommand):
    def handle(self, *args, **options):
        profile_id = options["profile_id"]
        profile = SearchProfile.objects.get(id=profile_id)
        created_count, existing_count = import_adzuna_jobs(profile)
        self.stdout.write(
            f"Successfully imported {created_count} new jobs. {existing_count} already in the database."
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "--profile-id",
            type=int,
            required=True
        )