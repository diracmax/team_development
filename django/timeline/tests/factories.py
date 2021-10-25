from factory.django import DjangoModelFactory
from factory import Faker, post_generation, Sequence, SubFactory, LazyAttribute
import random

from accounts.models import CustomUser
from timeline.models import Post, Category, Like, Apply
from accounts.tests.factories import UserFactory


FAKER_LOCALE = 'ja_JP'


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    
    display = Faker('word', locale=FAKER_LOCALE)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker('word', locale=FAKER_LOCALE)
    text = Faker('text', max_nb_chars=30, locale=FAKER_LOCALE)
    author = SubFactory(UserFactory)
    category = SubFactory(CategoryFactory)

class SamplePostFactory(PostFactory):
    author = LazyAttribute(lambda x: random.choice(CustomUser.objects.all()))
    category = LazyAttribute(lambda x: random.choice(Category.objects.all()))
