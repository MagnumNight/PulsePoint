from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse


class MoodTrackerTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="usertesting", password="testing1234!"
        )

    # Testing logged in user.
    def test_initial_tracker(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("moodtracker:home"))
        self.assertEqual(response.status_code, 302)

    def test_initial_questionnaire(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("moodtracker:questionnaire"))
        self.assertEqual(response.status_code, 302)

    def test_save_mood(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("moodtracker:save_mood"))
        self.assertEqual(response.status_code, 302)

    # Testing non-auth user.
    def test_initial_tracker_logout(self):
        self.client.logout()
        response = self.client.post(reverse("moodtracker:home"))
        self.assertEqual(response.status_code, 302)

    def test_initial_questionnaire_logout(self):
        self.client.logout()
        response = self.client.post(reverse("moodtracker:questionnaire"))
        self.assertEqual(response.status_code, 302)
