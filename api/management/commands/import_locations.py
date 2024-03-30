import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import Location


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='The path to the CSV file'
        )

    def handle(self, *args, **options):
        csv_path = options['path'] or str(
                Path(settings.BASE_DIR) / 'data',
            )

        self.import_csv_data(
            csv_path, 'uszips.csv',
            self.import_locations
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Locations imported successfully.'
            )
        )

    def import_csv_data(self, csv_path, filename, import_func):
        file_path = Path(csv_path) / filename
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_data = csv.DictReader(file)
            import_func(csv_data)

    def import_locations(self, csv_data):
        try:
            if not Location.objects.all().exists():

                locations = [Location(
                    city=row['city'],
                    state=row['state_name'],
                    zip=row['zip'],
                    latitude=row['lat'],
                    longitude=row['lng'],
                ) for row in csv_data
                ]
                Location.objects.bulk_create(locations)
        except ValueError:
            print('Locations already imported.')
