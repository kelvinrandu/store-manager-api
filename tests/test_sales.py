
# import unittest
# import json
# import sys

# from psycopg2 import connect, extras
# from application.app import create_app
# from application.database import conn, create_tables, delete_tables



# CREATE_SALE_URL = '/api/v1/sales/'
# GET_SINGLE_SALE = '/api/v1/sale/1/'
# GET_ALL_SALE = '/api/v1/sales/'
# CREATE_PRODUCT_URL = '/api/v1/products/'


# class SaleTestCase(unittest.TestCase):

#     def setUp(self):
#         '''Initialize app and define test variables'''
#         self.app = create_app("testing")
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#         self.login_user = { "email": "admin@gmail.com", "password":"12345678" }
#         self. products = { "name": "ps5", "quantity":12, "price":2000, "min_stock":5 } 
#         self.sales = { "description": "sony gaming console","product_id":1,"user_id":1,"quantity":6 }
#         self.empty_sale_description = { "": "sony gaming console","product_id":1,"user_id":1,"quantity":6 }
#         self.empty_sale_product = { "description": "sony gaming console","product_id":"","user_id":1,"quantity":6 }
#         self.empty_sale_user = { "description": "sony gaming console","product_id":1,"user_id":"","quantity":6 }
#         self.empty_sale_quantity = { "description": "sony gaming console","product_id":1,"user_id":1,"quantity":"" }

#         create_tables()

#     def login(self):
#         res_login = self.client.post('/api/v1/auth/login/',
#                                     data = json.dumps(self.login_user),
#                                     content_type='application/json')
#         return json.loads(res_login.data.decode())["access_token"]



#     def test_create_sale(self):
#         '''Test for creating a sale '''
#         response = self.client.post(CREATE_PRODUCT_URL,
#                                     data = json.dumps(self.products), 
#                                     headers=dict(Authorization="Bearer " + self.login()),
#                                     content_type = 'application/json')
#         self.assertEqual(response.status_code, 201)
#         response = self.client.post(CREATE_SALE_URL,
#                                     data = json.dumps(self.sales),
#                                     headers=dict(Authorization="Bearer " + self.login()), 
#                                     content_type = 'application/json')
#         resp_data = json.loads(response.data.decode())
#         self.assertTrue(resp_data['message'] == 'Sale created successfully')
#         self.assertEqual(response.status_code, 201)


# #     def test_create_sale_no_token(self):
# #         '''Test for creating a sale '''
# #         response = self.client.post(CREATE_SALE_URL,
# #                                     data = json.dumps(self.sales),
# #                                     content_type = 'application/json')
# #         self.assertEqual(response.status_code, 401)


# #     def test_get_sales(self):
# #         '''Test for Get all sale'''
# #         response = self.client.post(CREATE_SALE_URL,
# #                                     data = json.dumps(self.sales), 
# #                                     headers=dict(Authorization="Bearer " + self.login()),
# #                                     content_type = 'application/json')
# #         self.assertEqual(response.status_code, 201)

# #         '''Test  gets sales '''
# #         response = self.client.get(GET_ALL_SALE,
# #                                    headers=dict(Authorization="Bearer " + self.login()),
# #                                    content_type = 'application/json')   
# #         resp_data = json.loads(response.data.decode())
# #         self.assertTrue(resp_data['message'] == 'sales retrieved succesfully')
# #         self.assertEqual(response.status_code, 200)



# #     def test_empty_description(self):
# #         '''Test for empty sale description '''
# #         response = self.client.post(CREATE_SALE_URL,
# #                                     data = json.dumps(self.empty_sale_description), 
# #                                     headers=dict(Authorization="Bearer " + self.login()),
# #                                     content_type = 'application/json')
# #         resp_data = json.loads(response.data.decode())
# #         self.assertTrue(resp_data['message'] == 'Sale description  can not be empty')
# #         self.assertEqual(response.status_code, 400)



# #     def test_empty_items(self):
# #         '''Test for empty sale item '''
# #         response = self.client.post(CREATE_SALE_URL,
# #                                     data = json.dumps(self.empty_sale_items),
# #                                     headers=dict(Authorization="Bearer " + self.login()), 
# #                                     content_type = 'application/json')
# #         resp_data = json.loads(response.data.decode())
# #         self.assertTrue(resp_data['message'] == 'Sale items  can not be empty')
# #         self.assertEqual(response.status_code, 400)



# #     def test_get_single_sale(self):
# #         '''Test to get a single sale'''

# #         '''Add sale'''
# #         response = self.client.post(CREATE_SALE_URL,
# #                                     headers=dict(Authorization="Bearer " + self.login()),
# #                                     data = json.dumps(self.sales), 
# #                                     content_type = 'application/json')
# #         self.assertEqual(response.status_code, 201)

# #         '''return a single sale'''
# #         response = self.client.get(GET_SINGLE_SALE,
# #                                     headers=dict(Authorization="Bearer " + self.login()),
# #                                     data = json.dumps(self.sales), 
# #                                     content_type = 'application/json')
# #         resp_data = json.loads(response.data.decode())
# #         self.assertTrue(resp_data['message'] == 'sale retrieved succesfully')
# #         self.assertEqual(response.status_code, 200)

# #         delete_tables()