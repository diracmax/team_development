from factory.django import DjangoModelFactory
from factory import Faker

from timeline.models import Post, Category, Like, Apply


FAKER_LOCALE = 'ja_JP'

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Article

    # 'word'というprovider
    title = Faker('word', max_nb_chars=15, locale=FAKER_LOCALE)
    # 'text'というprovider
    text = Faker('text', max_nb_chars=30, locale=FAKER_LOCALE)