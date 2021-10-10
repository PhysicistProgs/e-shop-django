from django.contrib.sessions.models import Session
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class test_auth(TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.password = 'test'
        cls.user = User(
            username='test',
            email='test@glamil.com',
        )
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.client = Client()

    def test_incorrect_login(self):
        url = reverse('started_app:login')
        response = self.client.post(url, {
            'username': self.user.username,
            'password': 'some-incorrect-passwosrd',
        }, follow=True)
        print('mypassword', self.password)
        print(Session.objects.filter().count())
        self.assertIn('Please enter a correct username and password', str(response.content))

    def test_correct_login(self):
        url = reverse('started_app:login')
        response = self.client.post(url, {
            'username': self.user.username,
            'password': self.password,
        }, follow=True)
        print(Session.objects.filter().count())
        self.assertNotIn('Please enter a correct username and password', str(response.content))
