import random
from django.core.management import BaseCommand

from api.models import Truck, Location


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            if not Truck.objects.all().exists():
                Truck.objects.bulk_create([
                    Truck(
                        plate_number=(
                            f'{random.randint(1000, 9999)}{chr(random.randint(65, 90))}'
                        ),
                        cargo_capacity=random.randint(1, 1000),
                        location=Location.get_location()
                    )
                    for _ in range(20)
                ])

                self.stdout.write(
                    self.style.SUCCESS(
                        'Trucks created successfully.'
                    )
                )
        except ValueError:
            print('Trucks already exist.')
