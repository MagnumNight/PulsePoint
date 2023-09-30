from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from .tokens import account_activation_token, password_reset_token

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


    #def test_email_verification(self):
    #    response = self.client.post(reverse('signup'), {'first_name': 'first', 'last_name': 'last', 'username': 'testuser', 'email':'testing@gmail.com', 'password1': 'testing1234!', 'password2': 'testing1234!'})
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTemplateUsed(response, 'registration/signup.html')

    #    self.assertEqual(len(mail.outbox), 0)
    #    self.assertEqual(mail.outbox[0].subject, 'Activate your PulsePoint account.')

    #    user = User.objects.get(username = 'testuser')
    #    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    #    token = account_activation_token.make_token(user)
    #    response = self.client.get(reverse('activate', arg= [uidb64, token]))
    #    self.assertEqual(response.status_code, 302)

    def test_account_delete(self):
        user = User.objects.create_user(username='usertesting', password='testing1234!')
        response = self.client.post(reverse('login'),{'username': 'usertesting', 'password': 'testing1234!'})

        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/delete_account.html')

        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(User.objects.filter(username = 'usertesting').exists())