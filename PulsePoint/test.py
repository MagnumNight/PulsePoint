from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTestCase(TestCase):
    
    def test_valid_login(self):
        user = User.objects.create_user(username='usertesting', password='testing1234!')
        response = self.client.post(reverse('login'),{'username': 'usertesting', 'password': 'testing1234!'})
        self.assertEqual(response.status_code, 302)
    
    def test_invalid_password(self):
        user = User.objects.create_user(username='usertesting', password='password')
        response = self.client.post(reverse('login'),{'username': 'usertesting', 'password': 'pass'})
        self.assertEqual(response.status_code, 200)

    def test_invalid_username(self):
        user = User.objects.create_user(username='usertesting', password='password')
        response = self.client.post(reverse('login'),{'username': 'user', 'password': 'password'})
        self.assertEqual(response.status_code, 200)