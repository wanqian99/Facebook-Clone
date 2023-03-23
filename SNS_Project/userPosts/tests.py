from django.test import TestCase
from django.urls import reverse

import json
from .models import *
from .model_factories import *
from .views import *
from .serializers import *

# Create your tests here.
class UserPostTest(TestCase):
    userPost = None
    userPostSerializer = None
    good_url = None
    bad_url = None

    def setUp(self):
        self.userPost = UserPostFactory.create()
        self.userPostSerializer = UserPostSerializer(instance=self.userPost)

        self.good_url = reverse('user_post_api', kwargs={'pk': 1})
        self.bad_url = "api/userpost/qwerty"

    def tearDown(self):
        User.objects.all().delete()
        UserAccount.objects.all().delete()
        UserPost.objects.all().delete()
        UserFactory.reset_sequence()
        UserAccountFactory.reset_sequence()
        UserPostFactory.reset_sequence()

    # test that the data in the model matches the details of post created with UserPostFactory
    def test_post_model(self):
        userPost = self.userPost
        self.assertIsInstance(userPost, UserPost)
        
        self.assertEqual(userPost.user.username, 'testuser')
        self.assertEqual(userPost.user.email, 'testuser@gmail.com')
        self.assertEqual(userPost.user.first_name, 'apple')
        self.assertEqual(userPost.user.last_name, 'pineapple')
        self.assertEqual(userPost.user.password, 'testuserpassword')

        self.assertEqual(userPost.content, 'Hello!!')
        self.assertEqual(userPost.content_image, './static/userAccounts/user.png')

    # test that the view returns correct code with HttpResponseRedirect
    # [status code = 302, so means it's a HttpResponseRedirect, 
    # therefore there's no template used for the HTTP response]
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    # test that serializer has the correct fields
    def test_post_serializer(self):
        data = self.userPostSerializer.data
        self.assertEqual(set(data.keys()), set(['pk', 'user', 'content','content_image','timestamp']))

    # test that api returns correct fields when success
    def test_post_api_success(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertTrue(response.status_code, 200)
        data = json.loads(response.content)

        # api has these fields
        self.assertTrue(data['pk'])
        self.assertTrue(data['user'])
        self.assertTrue(data['user']['username'])
        self.assertTrue(data['user']['email'])
        self.assertTrue(data['user']['first_name'])
        self.assertTrue(data['user']['last_name'])
        self.assertTrue(data['user']['password'])
        self.assertTrue(data['content'])
        self.assertTrue(data['content_image'])
        self.assertTrue(data['timestamp'])

    # test that api returns correct error code when there is an error
    def test_post_api_error(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertTrue(response.status_code, 404)