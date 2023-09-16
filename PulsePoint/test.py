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

    def test_empty_username(self):
        user = User.objects.create_user(username='usertesting', password='password')
        response = self.client.post(reverse('login'),{'username': '', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

    def test_empty_password(self):
        user = User.objects.create_user(username='usertesting', password='password')
        response = self.client.post(reverse('login'),{'username': 'usertesting', 'password': ''})
        self.assertEqual(response.status_code, 200)

class RegisterTestCase(TestCase):
    def test_valid_signup(self):
        response = self.client.post(reverse('signup'), {'first_name': 'first', 'last_name': 'last', 'username': 'testuser', 'email':'testing@gmail.com', 'password1': 'testing1234!', 'password2': 'testing1234!'})
        self.assertEqual(response.status_code, 200)

    def test_weak_password(self):
        response = self.client.post(reverse('signup'), {'first_name': 'first', 'last_name': 'last', 'username': 'testuser', 'email':'testing@gmail.com', 'password1': '1234', 'password2': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_create_nonunique_user(self):
        user = User.objects.create_user(username='usertesting', password='password')
        response = self.client.post(reverse('signup'), {'first_name': 'first', 'last_name': 'last', 'username': 'usertesting', 'email':'testing@gmail.com', 'password1': '1234', 'password2': '1234'})
        self.assertEqual(response.status_code, 200)