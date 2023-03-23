from django.test import TestCase
from django.urls import reverse

import json
from .models import *
from .model_factories import *
from .views import *
from .serializers import *

# Create your tests here.
class UserAccountTest(TestCase):
    userAccount = None
    userAccountSerializer = None

    def setUp(self):
        self.userAccount = UserAccountFactory.create()
        self.userAccountSerializer = UserAccountSerializer(instance=self.userAccount)

        self.good_url = reverse('user_detail_api', kwargs={'pk': 1})
        self.bad_url = "api/user/qwerty"

    def tearDown(self):
        User.objects.all().delete()
        UserAccount.objects.all().delete()
        UserFactory.reset_sequence()
        UserAccountFactory.reset_sequence()

    # test that the data in the model matches the details of user account created with UserAccountFactory
    def test_user_account_model(self):
        userAcc = self.userAccount
        self.assertIsInstance(userAcc, UserAccount)

        self.assertEqual(userAcc.user.username, 'testuser')
        self.assertEqual(userAcc.user.email, 'testuser@gmail.com')
        self.assertEqual(userAcc.user.first_name, 'apple')
        self.assertEqual(userAcc.user.last_name, 'pineapple')
        self.assertEqual(userAcc.user.password, 'testuserpassword')

        self.assertEqual(userAcc.image, './static/userAccounts/user.png')
        self.assertEqual(userAcc.phone_number, '80008008')
        self.assertEqual(userAcc.dob, '2000-10-10')

    # test that the view returns correct code with redirect
    def test_user_account_profile_view(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 302)

    # test that the view returns correct code with redirect
    def test_user_account_editprofile_view(self):
        response = self.client.get(reverse('user_editProfile'))
        self.assertEqual(response.status_code, 302)

    # test that serializer has the correct fields
    def test_user_account_profile_serializer(self):
        data = self.userAccountSerializer.data
        self.assertEqual(set(data.keys()), set(['pk', 'user', 'image','phone_number','dob']))

    # test that api returns correct fields when success
    def test_user_account_profile_api_success(self):
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
        self.assertTrue(data['image'])
        self.assertTrue(data['phone_number'])
        self.assertTrue(data['dob'])

    # test that api returns correct error code when there is an error
    def test_user_account_profile_api_error(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertTrue(response.status_code, 404)



class RegistrationLoginTest(TestCase):
    userAccount = None
    userAccountSerializer = None

    def setUp(self):
        self.userAccount = UserAccountFactory.create()
        self.userAccountSerializer = UserAccountSerializer(instance=self.userAccount)

        self.good_url = reverse('createusers_api')
        self.bad_url = "api/createuserrr/"

    def tearDown(self):
        User.objects.all().delete()
        UserAccount.objects.all().delete()
        UserFactory.reset_sequence()
        UserAccountFactory.reset_sequence()

    # test that the view returns correct code
    def test_user_account_registration_view(self):
        response = self.client.get(reverse('user_register'))
        self.assertEqual(response.status_code, 200)
        # test that the correct template is used
        self.assertTemplateUsed(response, 'register.html')

    # test that the view returns correct code
    def test_user_account_login_view(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        # test that the correct template is used
        self.assertTemplateUsed(response, 'login.html')

    # test that api returns correct fields when success
    def test_user_account_registration_api_success(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertTrue(response.status_code, 200)

    # test that api returns correct error code when there is an error
    def test_user_account_registration_api_error(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertTrue(response.status_code, 404)



class UserSearchTest(TestCase):
    userAccount = None
    userAccountSerializer = None

    def setUp(self):
        self.userAccount = UserAccountFactory.create()
        self.userAccountSerializer = UserAccountSerializer(instance=self.userAccount)

    def tearDown(self):
        User.objects.all().delete()
        UserAccount.objects.all().delete()
        UserFactory.reset_sequence()
        UserAccountFactory.reset_sequence()

    # test that the view returns correct code with redirect
    def test_user_account_search_view(self):
        response = self.client.get(reverse('user_search'))
        self.assertEqual(response.status_code, 302)