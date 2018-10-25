
import unittest
import json
import sys

from application.app import create_app



REGISTER_URL = '/api/v1/register/'
LOGIN_URL = '/api/v1/login/'



class UserTestCase(unittest.TestCase):

    def setUp(self):
        '''Initialize app and define test variables'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.register_user = { "email": "test@gmail.com", "password":"12345678", "username":"test" }  
        self.register_user_empty_email = { "email": "", "password":"12345678", "username":"test" }
        self.register_user_invalid_email = { "email": "test.gmailcom", "password":"12345678", "username":"test" }
        self.register_user_empty_username = { "email": "test@gmail.com", "password":"12345678", "username":"" }
        self.register_user_empty_password = { "email": "test@gmail.com", "password":"", "username":"test" }    
        self.register_user_short_password = { "email": "test@gmail.com", "password":"wert", "username":"test" }                   
        self.login_user = { "email": "kelvin@gmail.com", "password":"12345678" }
        self.login_user_empty_email= { "email": "", "password":"12345678" }
        self.login_user_empty_password= { "email": "kelvin@gmail.com", "password":"" }


    def test_sign_up_success(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user),
                                            content_type = 'application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(resp_data['message'], 'User was created succesfully')


    def test_sign_up_empty_email(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_email),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'email can not be empty')

    def test_sign_up_invalid_email(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_invalid_email),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'Invalid email')


    def test_sign_up_empty_username(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_username),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'username cannot be empty')


    def test_sign_up_empty_password(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_password),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        # self.assertEqual(resp_data['response'], 'password must contain 6 or more characters')


    def test_sign_up_short_password(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_short_password),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        # self.assertEqual(resp_data['response'], 'password must contain 6 or more characters')


    def test_login_success(self):

        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user),
                                       content_type='application/json')

        resp_data = json.loads(res_login.data.decode())
        self.assertTrue(resp_data['access_token'])
        self.assertEqual(res_login.status_code, 200)
        self.assertEqual(resp_data['message'], 'User was logged in succesfully')

    def test_login_empty_email(self):

        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_email),
                                       content_type='application/json')

        resp_data = json.loads(res_login.data.decode())
        self.assertEqual(res_login.status_code, 400)
        # self.assertEqual(resp_data['message'], '')


    def test_login_empty_password(self):

        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_password),
                                       content_type='application/json')

        resp_data = json.loads(res_login.data.decode())
        self.assertEqual(res_login.status_code, 400)
        # self.assertEqual(resp_data['message'], '')