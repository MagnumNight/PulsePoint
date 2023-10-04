from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
class MoodTrackerTestCase(TestCase):
    def userEntity(self):
        self.user = User.objects.create_user(
            username="usertesting", password="testing1234!"
        )

    # Testing logged in user.

    def test_initial_tracker(self):
        self.client.login(username="usertesting", password="testing1234")
        response = self.client.post(reverse("moodtracker:home"))
        self.assertEqual(response.status_code, 302)

    def test_initial_questionnaire(self):
        self.client.login(username="usertesting", password="testing1234")
        response = self.client.post(reverse("moodtracker:questionnaire"))
        self.assertEqual(response.status_code, 302)

    def test_save_mood(self):
        self.client.login(username="usertesting", password="testing1234")
        response = self.client.post(reverse("moodtracker:save_mood"))
        self.assertEqual(response.status_code, 302)

    # Testing non-auth user.

    def test_initial_tracker_logout(self):
        self.client.logout()
        self.client.login(username="usertesting", password="testing1234")
        response = self.client.post(reverse("moodtracker:home"))
        self.assertEqual(response.status_code, 302)

    def test_initial_questionnaire_logout(self):
        self.client.logout()
        self.client.login(username="usertesting", password="testing1234")
        response = self.client.post(reverse("moodtracker:questionnaire"))
        self.assertEqual(response.status_code, 302)
