import csv
from django.core.management.base import BaseCommand
from ...models import Governorate

class Command(BaseCommand):
    help = 'Load cities data from CSV file'

    def handle(self, *args, **kwargs):
        with open('affiliate/management/commands/governorates.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            cities = [Governorate(
                governorate_name_ar=row['governorate_name_ar'],
            ) for row in reader]

        Governorate.objects.bulk_create(cities)
        self.stdout.write(self.style.SUCCESS('Governorates data loaded successfully.'))
