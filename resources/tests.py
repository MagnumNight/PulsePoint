from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class ResourceTestCase(TestCase):

    def test_resource_access(self):
         response = self.client.post(reverse('resources:home'))
         self.assertEqual(response.status_code, 200)

    def test_link_resources(self):
        response = self.client.post(reverse('resources:home'))

        self.assertContains(response, "General Anxiety Disorder")
        self.assertContains(response, "https://adaa.org/understanding-anxiety/generalized-anxiety-disorder-gad")

        self.assertContains(response, "Post Traumatic Stress Disorder")
        self.assertContains(response, "https://www.maketheconnection.net/conditions/ptsd/")

        self.assertContains(response, "Bipolar Disorder Type I and II")
        self.assertContains(response, "https://www.nimh.nih.gov/health/topics/bipolar-disorder")

        self.assertContains(response, "Obsessive Compulsive Disorder")
        self.assertContains(response, "https://iocdf.org/about-ocd/")

        self.assertContains(response, "Major Depressive Disorder")
        self.assertContains(response, "https://www.psychiatry.org/patients-families/depression/what-is-depression")

        self.assertContains(response, "Attention-Deficit Hyperactivity Disorder")
        self.assertContains(response, "https://www.nimh.nih.gov/health/topics/attention-deficit-hyperactivity-disorder-adhd")


        

