import datetime
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import os
from factory import LazyAttribute, Sequence, Faker
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyDateTime
from accounts.models import Follow, CustomUser

tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    username = Sequence(lambda n: f'user{n}')
    email = LazyAttribute(lambda o: f'{o.username}@example.com')
    password = "refwdqsa"
    photo = ImageField()
    is_staff = False
    is_active = True
    date_joined = FuzzyDateTime(start_dt=timezone.datetime(2021, 1, 1, tzinfo=tzinfo))

class SampleFollowFactory(DjangoModelFactory):
    class Meta:
        model = Follow
    
    follower = LazyAttribute(lambda x: random.choice(CustomUser.objects.all()))
    following = LazyAttribute(lambda x: random.choice(CustomUser.objects.all()))

# class SampleUserFactory(UserFactory):
#     username = Faker('profile', locale=FAKER_LOCALE)
#     photo = LazyAttribute(lambda x: random.choice(os.listdir("media/setup/account")))