from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

import json
from .models import *
from .views import *
from .serializers import *

# Create your tests here.
class FriendTest(TestCase):
    friend = None
    friendRequest = None

    def setUp(self):
        # create sample friend 
        self.user1 = User.objects.create(username='user1', email='user1@gmail.com', first_name='user1fn', last_name='user1ln', password='user1password')
        self.friend1 = Friend.objects.create(current_user=self.user1)
        self.user2 = User.objects.create(username='user2', email='user2@gmail.com', first_name='user2fn', last_name='user2ln', password='user2password')
        self.friend2 =  Friend.objects.create(current_user=self.user2)

        self.friendSerializer = FriendSerializer(instance=self.friend1)

        self.good_url = reverse('friends_api', kwargs={'pk': 1})
        self.bad_url = "api/friendlist/qwerty"

    def tearDown(self):
        User.objects.all().delete()
        Friend.objects.all().delete()

    # test that the data in the model matches the details of user account created with UserAccountFactory
    def test_friend_model(self):
        friend1 = self.friend1
        friend2 = self.friend2
        self.assertIsInstance(friend1, Friend)
        self.assertIsInstance(friend2, Friend)

        self.assertEqual(friend1.current_user.username, 'user1')
        self.assertEqual(friend1.current_user.email, 'user1@gmail.com')
        self.assertEqual(friend1.current_user.first_name, 'user1fn')
        self.assertEqual(friend1.current_user.last_name, 'user1ln')
        self.assertEqual(friend1.current_user.password, 'user1password')

        self.assertEqual(friend2.current_user.username, 'user2')
        self.assertEqual(friend2.current_user.email, 'user2@gmail.com')
        self.assertEqual(friend2.current_user.first_name, 'user2fn')
        self.assertEqual(friend2.current_user.last_name, 'user2ln')
        self.assertEqual(friend2.current_user.password, 'user2password')

    # test that serializer has the correct fields
    def test_friend_serializer(self):
        data = self.friendSerializer.data
        self.assertEqual(set(data.keys()), set(['pk', 'current_user', 'friends']))

    # test that api returns correct fields when success
    def test_user_account_profile_api_success(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertTrue(response.status_code, 200)
        data = json.loads(response.content)

        # api has these fields
        self.assertTrue(data['pk'])
        self.assertTrue(data['current_user']['username'])
        self.assertTrue(data['current_user']['email'])
        self.assertTrue(data['current_user']['first_name'])
        self.assertTrue(data['current_user']['last_name'])
        self.assertTrue(data['current_user']['password'])

    # test that api returns correct error code when there is an error
    def test_user_account_profile_api_error(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertTrue(response.status_code, 404)



class FriendRequestTest(TestCase):
    friend = None
    friendRequest = None
    friendRequestSerializer = None

    def setUp(self):
        # create sample friend 
        self.user1 = User.objects.create(username='user1', email='user1@gmail.com', first_name='user1fn', last_name='user1ln', password='user1password')
        self.friend1 = Friend.objects.create(current_user=self.user1)
        self.user2 = User.objects.create(username='user2', email='user2@gmail.com', first_name='user2fn', last_name='user2ln', password='user2password')
        self.friend2 =  Friend.objects.create(current_user=self.user2)

        self.friendRequest = FriendRequest(sender=self.user1, receiver=self.user2, pending="True")
        self.friendRequestSerializer = FriendRequestSerializer()

        self.good_url = reverse('friend_request_api', kwargs={'pk': 1})
        self.bad_url = "api/friendrequest/qwerty"

    def tearDown(self):
        User.objects.all().delete()
        Friend.objects.all().delete()
        FriendRequest.objects.all().delete()

    # test that the data in the model matches
    def test_friend_model(self):
        self.assertIsInstance(self.friendRequest, FriendRequest)

        self.assertEqual(self.friendRequest.sender, self.user1)
        self.assertEqual(self.friendRequest.receiver, self.user2)
        self.assertEqual(self.friendRequest.pending, "True")

    # test that serializer has the correct fields
    def test_friend_request_serializer(self):
        data = self.friendRequestSerializer.data
        self.assertEqual(set(data.keys()), set(['sender', 'receiver', 'pending']))

    # test that api returns correct fields when success
    def test_friendRequest_api_success(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertTrue(response.status_code, 200)
        data = json.loads(response.content)

    # test that api returns correct error code when there is an error
    def test_friendRequest_api_error(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertTrue(response.status_code, 404)
