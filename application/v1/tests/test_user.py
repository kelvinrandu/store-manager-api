
import unittest
import json
import sys

from application.app import create_app
from application.database import TestDatabaseConnect
db = TestDatabaseConnect()


REGISTER_URL = '/api/v1/auth/signup/'
LOGIN_URL = '/api/v1/auth/login/'



class UserTestCase(unittest.TestCase):

    def setUp(self):
        '''Initialize app and define test variables'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.register_user = { "email": "john23@gmail.com", "password":"12345678", "username":"johny23","user_id":1 } 
        # self.register_user1 = { "email": "testme@gmail.com", "password":"12345678", "username":"testme" }  
        self.register_user_empty_email = { "email": "", "password":"12345678", "username":"test" }
        self.register_user_invalid_email = { "email": "test.gmailcom", "password":"12345678", "username":"test" }
        self.register_user_empty_username = { "email": "test@gmail.com", "password":"12345678", "username":"" }
        self.register_user_empty_password = { "email": "test@gmail.com", "password":"", "username":"test" }    
        self.register_user_short_password = { "email": "test@gmail.com", "password":"wert", "username":"test" }                   
        self.login_user = { "email": "testme@gmail.com", "password":"12345678" }
        self.login_user_empty_email= { "email": "", "password":"12345678" }
        self.login_user_empty_password= { "email": "kelvin@gmail.com", "password":"" }

        db.create_tables()
        # self.client.post(REGISTER_URL, data=json.dumps(self.register_user1),
        #                                     content_type = 'application/json')
        


    def test_sign_up_success(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user),
                                            content_type = 'application/json')
        resp_data = json.loads(res.data.decode())
        # self.assertEqual(res.status_code, 201)
        self.assertEqual(resp_data['message'], 'Store attendant was created succesfully')


    # def test_sign_up_empty_email(self):
    #     res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_email),
    #                              content_type='application/json')
    #     resp_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 400)
    #     # self.assertEqual(resp_data['response'], 'invalid email')

    # def test_sign_up_invalid_email(self):
    #     res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_invalid_email),
    #                              content_type='application/json')
    #     resp_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 400)
    #     # self.assertEqual(resp_data['response'], 'invalid email')


    # def test_sign_up_empty_username(self):
    #     res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_username),
    #                              content_type='application/json')
    #     resp_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 400)
    #     # self.assertEqual(resp_data['response'], 'invalid username')


    # def test_sign_up_empty_password(self):
    #     res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_password),
    #                              content_type='application/json')
    #     resp_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 400)
    #     # self.assertEqual(resp_data['response'], 'password must contain 6 or more characters')


    # def test_sign_up_short_password(self):
    #     res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_short_password),
    #                              content_type='application/json')
    #     resp_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 400)
    #     # self.assertEqual(resp_data['response'], 'password must contain 6 or more characters')


    # def test_login_success(self):
    #     res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user1),
    #                                         content_type = 'application/json')
    #     resp_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 201)

    #     res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user),
    #                                    content_type='application/json')

    #     resp_data = json.loads(res_login.data.decode())
    #     self.assertTrue(resp_data['access_token'])
    #     self.assertEqual(res_login.status_code, 200)
    #     self.assertEqual(resp_data['message'], 'User was logged in succesfully')

    # def test_login_empty_email(self):

    #     res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_email),
    #                                    content_type='application/json')

    #     resp_data = json.loads(res_login.data.decode())
    #     self.assertEqual(res_login.status_code, 400)
    #     # self.assertEqual(resp_data['message'], '')


    # def test_login_empty_password(self):

    #     res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_password),
    #                                    content_type='application/json')

    #     resp_data = json.loads(res_login.data.decode())
    #     self.assertEqual(res_login.status_code, 400)
    #     # self.assertEqual(resp_data['message'], '')

    def tearDown(self):
        db.delete_tables()