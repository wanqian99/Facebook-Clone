from django.test import TestCase
from django.urls import reverse

import json
from .models import *
from .model_factories import *
from .views import *
from .serializers import *

# Create your tests here.
class ChatroomTest(TestCase):
    chatroom = None
    ChatroomSerializer = None

    def setUp(self):
        self.chatroom = ChatroomFactory.create()
        self.ChatroomSerializer = ChatroomSerializer(instance=self.chatroom)

        self.good_url = reverse('chatroom-api', kwargs={'pk': 1})
        self.bad_url = "api/chatroom/qwerty"

    def tearDown(self):
        Chatroom.objects.all().delete()
        ChatroomFactory.reset_sequence()

    # test that the data in the model matches the details
    def test_chatroom_model(self):
        chatroom = self.chatroom
        self.assertIsInstance(chatroom, Chatroom)

        self.assertEqual(chatroom.chatroom, 'testchatroom')

    # test that the view returns correct code with redirect
    def test_chatroom_view(self):
        response = self.client.get(reverse('chat'))
        self.assertEqual(response.status_code, 302)

    # test that serializer has the correct fields
    def test_chatroom_serializer(self):
        data = self.ChatroomSerializer.data
        self.assertEqual(set(data.keys()), set(['pk', 'chatroom', 'user']))

    # test that api returns correct fields when success
    def test_chatroom_api_success(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertTrue(response.status_code, 200)
        data = json.loads(response.content)

        # api has these fields
        self.assertTrue(data['pk'])
        self.assertTrue(data['chatroom'])

    # test that api returns correct error code when there is an error
    def test_chatroom_api_error(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertTrue(response.status_code, 404)



class ChatroomContentTest(TestCase):
    chatroomContent = None
    ChatroomSerializer = None

    def setUp(self):
        self.chatroomContent = ChatroomContentFactory.create()
        self.ChatroomContentSerializer = ChatroomContentSerializer()

        self.good_url = reverse('chatroom-api', kwargs={'pk': 1})
        self.bad_url = "api/chatroom/qwerty"

    def tearDown(self):
        Chatroom.objects.all().delete()
        ChatroomContent.objects.all().delete()
        ChatroomFactory.reset_sequence()
        ChatroomContentFactory.reset_sequence()

    # test that the data in the model matches the details
    def test_chatroom_content_model(self):
        chatroomContent = self.chatroomContent
        self.assertIsInstance(chatroomContent, ChatroomContent)

        self.assertEqual(chatroomContent.content, 'chat msg 1')
        self.assertEqual(chatroomContent.user.username, 'testuser')
        self.assertEqual(chatroomContent.user.email, 'testuser@gmail.com')
        self.assertEqual(chatroomContent.user.first_name, 'apple')
        self.assertEqual(chatroomContent.user.last_name, 'pineapple')
        self.assertEqual(chatroomContent.user.password, 'testuserpassword')
        self.assertEqual(chatroomContent.chatroom.chatroom, 'testchatroom')