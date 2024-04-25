from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
import random
from accounts.models import User, Profile
from ...models import Task


class Command(BaseCommand):
    help = "inserting dummy task"

    def __init__(self, *args, **kwargs) -> None:
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(email=self.fake.email(), password="123456@Ms")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.image = self.fake.image_url()
        profile.save()

        for _ in range(5):
            Task.objects.create(
                user=profile,
                title=self.fake.sentence(nb_words=10, variable_nb_words=False),
                description=self.fake.paragraph(nb_sentences=3),
                done=random.choice([True, False]),
                created_date=datetime.now(),
            )
