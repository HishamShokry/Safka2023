# orders/management/commands/create_fake_orders.py

import random
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from faker import Faker
from affiliate.models import ShippingPrice, City, Order, generate_unique_barcode
from accounts.models import User
from django.utils import timezone
from datetime import timedelta
import calendar




fake = Faker()
marketer_user = User.objects.get(id=4)
governorate = ShippingPrice.objects.get(id=2)
city = City.objects.get(id=1)

class Command(BaseCommand):
    help = 'Populate the Orders model with fake data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of fake orders to create')

    def handle(self, *args, **options):
        total = options['total']
        self.stdout.write(self.style.SUCCESS(f'Creating {total} fake orders...'))

        for _ in range(total):

            created_at = fake.date_time_between(start_date="-365d", end_date=timezone.now())
            print(created_at)


            Order.objects.create(
                status= Order.PENDING,
                barcode= generate_unique_barcode(),
                # barcode_returned=get_random_string(11) if random.choice([True, False]) else None,
                marketer=marketer_user,  # Assuming the marketer field is optional
                client_name=fake.name(),
                client_phone1 = '01' + fake.phone_number()[2:][:9],
                client_phone2= '01' + fake.phone_number()[2:][:9],
                client_address=fake.address(),
                governorate=governorate,   # Assuming the governorate field is optional
                city=city,  # Assuming the city field is optional
                shiping_price=50,
                shipping_company=None,  # Assuming the shipping_company field is optional
                commission= 100,
                total=random.randint(50, 1000),
                total_items_price=random.uniform(10, 1000),
                note=fake.text(),
                whats1_clicked=random.randint(0, 10),
                phone1_clicked=random.randint(0, 10),
                sms1_clicked=random.randint(0, 10),
                whats2_clicked=random.randint(0, 10),
                phone2_clicked=random.randint(0, 10),
                sms2_clicked=random.randint(0, 10),
                created_at=created_at,
                updated_at=created_at,
            )

        self.stdout.write(self.style.SUCCESS('Fake orders created successfully.'))
