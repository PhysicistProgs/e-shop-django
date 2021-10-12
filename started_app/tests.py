from django.contrib.sessions.models import Session
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from started_app.models import Shoe, Brand, Size, Material


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
        self.assertIn('Please enter a correct username and password', str(response.content))
        self.assertTemplateUsed(response, 'started_app/login.html')
        self.assertIs(200, response.status_code)

    def test_correct_login(self):
        with self.assertTemplateNotUsed('started_app/login.html'):
            url = reverse('started_app:login')
            response = self.client.post(url, {
                'username': self.user.username,
                'password': self.password,
            }, follow=True)
        self.assertTemplateUsed(response, 'started_app/index.html')
        self.assertNotIn('Please enter a correct username and password', str(response.content))
        self.assertIs(200, response.status_code)

    def test_registration_success_password(self):
        url = reverse('started_app:register')
        response = self.client.post(url, {
            'username': 'test_username',
            'password1': 'My-test-password1',
            'password2': 'My-test-password1',
        }, follow=True)
        self.assertTemplateUsed(response, 'started_app/login.html')
        self.assertIs(200, response.status_code)
        self.assertIn('Регистрация прошла успешно', response.content.decode())

    def test_registration_wrong_password(self):
        url = reverse('started_app:register')
        response = self.client.post(url, {
            'username': 'test_username',
            'password1': 'My-test-password1',
            'password2': 'My-test-password1',
        }, follow=True)
        self.assertTemplateUsed(response, 'started_app/login.html')
        self.assertIs(200, response.status_code)
        self.assertIn('Регистрация прошла успешно', response.content.decode())

    def test_not_available_shoe_not_in_queryset(self):
        test_brand = Brand.objects.create(name='test', description='test', country='test')
        test_material = Material.objects.create(name='test', description='test')
        not_available_shoe = Shoe.objects.create(
            name='test', brand=test_brand,
            price=1, description='test',
            is_available=False,
            material=test_material
        )
        self.assertIs(0, Shoe.available_shoes.all().count())

    def test_available_shoe_in_queryset(self):
        test_brand = Brand.objects.create(name='test', description='test', country='test')
        test_material = Material.objects.create(name='test', description='test')
        not_available_shoe = Shoe.objects.create(
            name='test', brand=test_brand,
            price=1, description='test',
            is_available=True,
            material=test_material
        )
        self.assertIs(1, Shoe.available_shoes.all().count())

    def test_shoe_is_not_available(self):
        test_brand = Brand.objects.create(name='test', description='test', country='test')
        test_material = Material.objects.create(name='test', description='test')
        not_available_shoe = Shoe.objects.create(
            name='test', brand=test_brand,
            price=1, description='test',
            is_available=False,
            material=test_material
        )
        url = reverse('started_app:shoe_info', kwargs={'pk': not_available_shoe.pk})
        response = self.client.get(url)
        self.assertIn('Нет в наличии', str(response.content.decode()))
        self.assertTemplateUsed('started_app/shoe_info.html')
        self.assertIs(200, response.status_code)
