import unittest
import json
import sys
from psycopg2 import connect, extras
from application.app import create_app
from application.database import conn,create_tables,delete_tables

db = conn.cursor(cursor_factory=extras.RealDictCursor)

REGISTER_URL = '/api/v1/auth/signup/'
LOGIN_URL = '/api/v1/auth/login/'



class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.register_user = { "email": "john23@gmail.com", "password":"12345678", "username":"johny"} 
        # self.register_user1 = { "email": "testme@gmail.com", "password":"12345678", "username":"testme" }  
        self.register_user_empty_email = { "email": "", "password":"12345678", "username":"test" }
        self.register_user_invalid_email = { "email": "test.gmailcom", "password":"12345678", "username":"test" }
        self.register_user_empty_username = { "email": "test@gmail.com", "password":"12345678", "username":"" }
        self.register_user_empty_password = { "email": "test@gmail.com", "password":"", "username":"test" }    
        self.register_user_short_password = { "email": "test@gmail.com", "password":"wert", "username":"test" }                   
        self.login_user = { "email": "admin@gmail.com", "password":"12345678" }
        self.login_user_empty_email= { "email": "", "password":"12345678" }
        self.login_user_empty_password= { "email": "kelvin@gmail.com", "password":"" }

        create_tables()
    def login(self):
        res_login = self.client.post('/api/v1/auth/login/', data=json.dumps(
            dict(email='admin@gmail.com', password='12345678')),
                                       content_type='application/json')
        return json.loads(res_login.data.decode())["access_token"]

        
    def test_sign_up_without_token(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user),
 
                                            content_type = 'application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
     

    def test_sign_up_success(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user),
                                            headers=dict(Authorization="Bearer " + self.login()),
                                            content_type = 'application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(resp_data['message'], 'Store attendant has been created succesfully')


    def test_sign_up_empty_email(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_email),
                                headers=dict(Authorization="Bearer " + self.login()),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'email can not be empty')

    def test_sign_up_invalid_email(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_invalid_email),
                                headers=dict(Authorization="Bearer " + self.login()),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'Invalid email')


    def test_sign_up_empty_username(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_username),
                                headers=dict(Authorization="Bearer " + self.login()),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'username is empty')


    def test_sign_up_empty_password(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_empty_password),
                                headers=dict(Authorization="Bearer " + self.login()),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'password cannot be empty')


    def test_sign_up_short_password(self):
        res = self.client.post(REGISTER_URL, data=json.dumps(self.register_user_short_password),
                                headers=dict(Authorization="Bearer " + self.login()),
                                 content_type='application/json')
        resp_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(resp_data['message'], 'Password should be atleast 6 characters')


    def test_login_success(self):

        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user),
                                       content_type='application/json')

        resp_data = json.loads(res_login.data.decode())
        self.assertTrue(resp_data['access_token'])
        self.assertEqual(res_login.status_code, 200)
        self.assertEqual(resp_data['message'], 'User has logged in succesfully')

    def test_login_empty_email(self):

        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_email),
                                       content_type='application/json')

        resp_data = json.loads(res_login.data.decode())
        self.assertEqual(res_login.status_code, 400)
        self.assertEqual(resp_data['message'], 'email can not be empty')


    def test_login_empty_password(self):

        res_login = self.client.post(LOGIN_URL, data=json.dumps(self.login_user_empty_password),
                                       content_type='application/json')

        resp_data = json.loads(res_login.data.decode())
        self.assertEqual(res_login.status_code, 400)
        self.assertEqual(resp_data['message'], 'password cannot be empty')

        delete_tables()