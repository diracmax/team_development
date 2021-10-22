from django.test import Client, TestCase
from accounts.models import CustomUser
from accounts.tests.factories import UserFactory
from django.core.exceptions import ValidationError


class UserValidatorTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory()
    
    def test_validators(self):
        self.assertEqual(None, self.user1.full_clean())
        self.assertRaises(ValidationError, UserFactory(github_id='-invalid').full_clean)
        self.assertRaises(ValidationError, UserFactory(github_id='\invalid/').full_clean)
        # user = UserFactory(description='a'*401)
        # user.save()
        # print(user)
        # with self.assertRaises(ValidationError):
        #     UserFactory(description='a'*401).full_clean()
        user = UserFactory(photo__width=201, photo__height=201)
        self.assertEqual([200, 200], [user.photo.height, user.photo.width])
        user = UserFactory(photo__width=1, photo__height=1)
        self.assertEqual([200, 200], [user.photo.height, user.photo.width])
        

class HogeTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('HogeTaro', 'taro@hoge.com', 'password')

        self.client = Client()

        self.client.login(username='HogeTaro', password='password')
		