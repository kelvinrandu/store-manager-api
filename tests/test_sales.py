
import unittest
import json
import sys

from psycopg2 import connect, extras
from application.app import create_app
from application.database import conn, create_tables, delete_tables



CREATE_SALE_URL = '/api/v1/sales/'
GET_SINGLE_SALE = '/api/v1/sale/1/'
GET_ALL_SALE = '/api/v1/sales/'
CREATE_PRODUCT_URL = '/api/v1/products/'


class SaleTestCase(unittest.TestCase):

    def setUp(self):
        '''Initialize app and define test variables'''
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.register_user = { "email": "john23@gmail.com", "password":"12345678", "username":"johny"} 
        self.login_admin = { "email": "admin@gmail.com", "password":"12345678" }
        self.login_user = { "email": "john23@gmail.com", "password":"12345678" }
        self.products = { "name": "name", "quantity": 70, "min_stock":68, "price":2000, "category_id":1 }                              
        self.sales = {"product_id":1,"quantity":1 }
        self.empty_product_id = {"product_id":"","quantity":2 }
        self.empty_quantity = {"product_id":1,"quantity":"" }

        create_tables()

    def login(self):
        res_login = self.client.post('/api/v1/auth/login/',
                                    data = json.dumps(self.login_admin),
                                    content_type='application/json')
        return json.loads(res_login.data.decode())["access_token"]


    def attendant_login(self):
        res = self.client.post('/api/v1/auth/signup/', data=json.dumps(self.register_user),
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        res_login = self.client.post('/api/v1/auth/login/',
                                    data = json.dumps(self.login_user),
                                    content_type='application/json')
        return json.loads(res_login.data.decode())["access_token"]

    def test_create_sale(self):
        '''Test for creating a sale '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)
        response1 = self.client.post(CREATE_SALE_URL,
                                    data = json.dumps(self.sales),
                                    headers=dict(Authorization="Bearer " + self.attendant_login()), 
                                    content_type = 'application/json')
        resp_data = json.loads(response1.data.decode())
        self.assertEqual(resp_data['message'], 'sale created successfully')
        self.assertEqual(response1.status_code, 201)

    def test_create_sale_empty_token(self):
        '''Test for creating a sale '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)
        response1 = self.client.post(CREATE_SALE_URL,
                                    data = json.dumps(self.sales),
                                    content_type = 'application/json')
        resp_data = json.loads(response1.data.decode())
        self.assertEqual(resp_data['msg'], 'Missing Authorization Header')
        self.assertEqual(response1.status_code, 401)

    def test_create_sale_invalid_token(self):
        '''Test for creating a sale '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)
        response1 = self.client.post(CREATE_SALE_URL,
                                    data = json.dumps(self.sales),
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response1.data.decode())
        self.assertEqual(resp_data['message'], 'unauthorized ')
        self.assertEqual(response1.status_code, 401)

    def test_create_sale_no_empty_quantity(self):
        '''Test for creating a sale '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)
        response1 = self.client.post(CREATE_SALE_URL,
                                    data = json.dumps(self.empty_quantity),
                                    headers=dict(Authorization="Bearer " + self.attendant_login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response1.data.decode())
        # self.assertEqual(resp_data['message'], 'quantity cannot be blank')
        self.assertEqual(response1.status_code, 400)

    def test_create_sale_no_empty_product_id(self):
        '''Test for creating a sale '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)
        response1 = self.client.post(CREATE_SALE_URL,
                                    data = json.dumps(self.empty_product_id),
                                    headers=dict(Authorization="Bearer " + self.attendant_login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response1.data.decode())
        # self.assertEqual(resp_data['message'], 'quantity cannot be blank')
        self.assertEqual(response1.status_code, 400)


        delete_tables()