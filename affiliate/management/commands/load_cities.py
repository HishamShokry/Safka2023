import csv
from django.core.management.base import BaseCommand
from ...models import City

class Command(BaseCommand):
    help = 'Load cities data from CSV file'

    def handle(self, *args, **kwargs):
        with open('affiliate/management/commands/cities.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            cities = [City(
                governorate_id=row['governorate_id'],
                city_name_ar=row['city_name_ar'],
                city_name_en=row['city_name_en'],
            ) for row in reader]

        City.objects.bulk_create(cities)
        self.stdout.write(self.style.SUCCESS('Cities data loaded successfully.'))
