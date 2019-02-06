from rest_framework.test import APIClient

from testing.testcases import TestCase


# Create your tests here.

class AccountTests(TestCase):
    def setUp(self):
        self.user = self.createUser('ncjxjj')

    def test_login(self):
        url = '/api/account/login/'
        data = {
            'username': 'ncjxjj',
            'password': 'ncjxjjncjnb'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        data = {
            'username123': 'ncjxjadaj',
            'passwo123rd': 'ncjxjjncjnb'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'ncjdjj',
            'password': 'ncjxjjncjnb'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 406)

    def test_logout(self):
        url = '/api/account/logout/'
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.user)
        response = client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        user = self.createUser(username='ncj')
        data = {
            'old_password': 'ncjncjnb',
            'new_password': 'ncj233'
        }
        url = '/api/account/change_password/'
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(user)
        response = client.post(url, data=data, decode=False)
        self.assertEqual(response.status_code, 202)

    def test_change_password_with_incorrect_old_password(self):
        user = self.createUser(username='ncj')
        data = {
            'old_password': 'ncjnb',
            'new_password': 'ncj233'
        }
        url = '/api/account/change_password/'
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(user)
        response = client.post(url, data=data, decode=False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], '原密码错误')

    def test_change_password_with_invalid_form(self):
        user = self.createUser(username='ncj')
        data = {
            'old_password23': 'ncjnb',
            'new_password1': 'ncj233'
        }
        url = '/api/account/change_password/'
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(user)
        response = client.post(url, data=data, decode=False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], '表单填写错误')
