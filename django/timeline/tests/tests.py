from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from timeline.models import Post, Category

class TimelineTestCase(TestCase):

    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_loggedin_index(self):
        client = Client()
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password')

        client.login(email='test@example.com',password='password')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        
        tmp = Category.objects.create(
                display="カテゴリー")
        tmp.save()
        client.post('/create/', {'category': tmp.pk, 'title': 'タイトル', 'text': '本文', 'photo': '', })
        latest_post = Post.objects.latest('created_at')
        self.assertEqual(latest_post.text, '本文')

