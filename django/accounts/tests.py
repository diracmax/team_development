
from django.test import Client, TestCase
from .models import CustomUser

class HogeTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('HogeTaro', 'taro@hoge.com', 'password')

        self.client = Client()

        self.client.login(username='HogeTaro', password='password')
		