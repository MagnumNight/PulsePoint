from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class ResourceTestCase(TestCase):

    def test_resource_access(self):
         response = self.client.post(reverse('resources:home'))
         self.assertEqual(response.status_code, 200)