from django.utils import timezone
from faker import Faker
from affiliate.models import Category
from django.core.management import setup_environ

# Replace 'myproject' with the actual name of your Django project
import safka.settings as settings
setup_environ(settings)

fake = Faker()

# Create 5000 demo data entries
for _ in range(5000):
    # Keep generating a unique name
    while True:
        category_name = fake.word()
        if not Category.objects.filter(name=category_name).exists():
            break

    created_at = fake.date_time_this_decade()
    updated_at = created_at + timezone.timedelta(minutes=fake.random_int(1, 60))

    Category.objects.create(
        name=category_name,
        created_at=created_at,
        updated_at=updated_at
    )
