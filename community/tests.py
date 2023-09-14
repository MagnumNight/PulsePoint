from django.test import TestCase
from .models import Forum
from django.urls import reverse
from .views import create_forum

# Create your tests here.
class ForumTestCase(TestCase):

    #Without need for credentials
    def test_forum_create(self):
        forum = Forum.objects.create(title='titletest', description='testdescription')
        response = self.client.post(reverse('community:create_forum'),{'title': 'titletest', 'description': 'testdescription'})
        self.assertEqual(response.status_code, 302)

    def authorizedUser(self):
        self.url = reverse('community:create_forum')
        self.user = User.objects.create_user(username='usertest', password='passwordtest1234!')
        self.client.login(username='usertest', password='passwordtest1234!')

    def test_authForumCreate(self):
        response = self.client.get(reverse('community:create_forum'))
        self.assertRedirects(response, reverse('community:home'))
        response = self.client.post(reverse('community:create_forum'), {'title': 'title', 'description': 'description'})
        #Intended Value = 1
        self.assertEqual(Forum.objects.count(), 0)
        new_forum = Forum.objects.first()
        self.assertEqual(new_forum.title, 'title')
        self.assertEqual(new_forum.description, 'description')
        self.assertEqual(new_forum.user, self.user)

    def test_blankForumEntry(self):
        response = self.client.post(reverse('community:create_forum'), {'title': '', 'description': ''})
        #Intended Value = 302
        self.assertEqual(response.status_code, 302)


    
