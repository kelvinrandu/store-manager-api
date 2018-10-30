
# import unittest
# import json
# import sys

# from application.app import create_app



# CREATE_SALE_URL = '/api/v1/sales/'
# GET_SINGLE_SALE = '/api/v1/sale/1/'
# GET_ALL_SALE = '/api/v1/sales/'


# class SaleTestCase(unittest.TestCase):

#     def setUp(self):
#         '''Initialize app and define test variables'''
#         self.app = create_app('testing')
#         self.client = self.app.test_client()
#         self.sales = { "description": "ps4","items":{"id":1,"name":"rubber shoes","price":300,"quantity":12} }
#         self.empty_sale_description = { "description": "", "items":{"id":1,"name":"rubber shoes","price":300,"quantity":12} }
#         self.empty_sale_items = { "description": "gjjgjg", "items":"" }
#         self.client.post('api/v1/auth/signup', data=json.dumps(
#             dict(email='test@gmail.com', username='testme', password='12345678')),
#                            content_type='application/json')

#     def login(self):
#         res_login = self.client.post('/api/v1/auth/login/', data=json.dumps(
#             dict(email='test@gmail.com', password='12345678')),
#                                        content_type='application/json')
#         return json.loads(res_login.data.decode())["access_token"]


#     def test_create_sale(self):
#         '''Test for creating a sale '''
#         response = self.client.post(CREATE_SALE_URL,
#                                     data = json.dumps(self.sales),
#                                     headers=dict(Authorization="Bearer " + self.login()), 
#                                     content_type = 'application/json')
#         resp_data = json.loads(response.data.decode())
#         self.assertTrue(resp_data['message'] == 'Sale created successfully')
#         self.assertEqual(response.status_code, 201)


#     def test_create_sale_no_token(self):
#         '''Test for creating a sale '''
#         response = self.client.post(CREATE_SALE_URL,
#                                     data = json.dumps(self.sales),
#                                     content_type = 'application/json')
#         self.assertEqual(response.status_code, 401)


#     def test_get_sales(self):
#         '''Test for Get all sale'''
#         response = self.client.post(CREATE_SALE_URL,
#                                     data = json.dumps(self.sales), 
#                                     headers=dict(Authorization="Bearer " + self.login()),
#                                     content_type = 'application/json')
#         self.assertEqual(response.status_code, 201)

#         '''Test  gets sales '''
#         response = self.client.get(GET_ALL_SALE,
#                                    headers=dict(Authorization="Bearer " + self.login()),
#                                    content_type = 'application/json')   
#         resp_data = json.loads(response.data.decode())
#         self.assertTrue(resp_data['message'] == 'sales retrieved succesfully')
#         self.assertEqual(response.status_code, 200)



#     def test_empty_description(self):
#         '''Test for empty sale description '''
#         response = self.client.post(CREATE_SALE_URL,
#                                     data = json.dumps(self.empty_sale_description), 
#                                     headers=dict(Authorization="Bearer " + self.login()),
#                                     content_type = 'application/json')
#         resp_data = json.loads(response.data.decode())
#         self.assertTrue(resp_data['message'] == 'Sale description  can not be empty')
#         self.assertEqual(response.status_code, 400)



#     def test_empty_items(self):
#         '''Test for empty sale item '''
#         response = self.client.post(CREATE_SALE_URL,
#                                     data = json.dumps(self.empty_sale_items),
#                                     headers=dict(Authorization="Bearer " + self.login()), 
#                                     content_type = 'application/json')
#         resp_data = json.loads(response.data.decode())
#         self.assertTrue(resp_data['message'] == 'Sale items  can not be empty')
#         self.assertEqual(response.status_code, 400)



#     def test_get_single_sale(self):
#         '''Test to get a single sale'''

#         '''Add sale'''
#         response = self.client.post(CREATE_SALE_URL,
#                                     headers=dict(Authorization="Bearer " + self.login()),
#                                     data = json.dumps(self.sales), 
#                                     content_type = 'application/json')
#         self.assertEqual(response.status_code, 201)

#         '''return a single sale'''
#         response = self.client.get(GET_SINGLE_SALE,
#                                     headers=dict(Authorization="Bearer " + self.login()),
#                                     data = json.dumps(self.sales), 
#                                     content_type = 'application/json')
#         resp_data = json.loads(response.data.decode())
#         self.assertTrue(resp_data['message'] == 'sale retrieved succesfully')
#         self.assertEqual(response.status_code, 200)