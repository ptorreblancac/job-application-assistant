from django.core.management.base import BaseCommand
from jobs.services import import_adzuna_jobs

class Command(BaseCommand):
    def handle(self, *args, **options):
        created_count, existing_count = import_adzuna_jobs()
        self.stdout.write(
            f"Successfully imported {created_count} new jobs. {existing_count} already in the database."
        )