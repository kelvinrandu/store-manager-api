from flask_restful import Resource,reqparse
from flask import Flask,jsonify,request, make_response
from passlib.hash import pbkdf2_sha256 as sha256



products = []
cart = []
users = [{
    "id" : 1,
	"username":"kelvin",
	"email":"kelvin@gmail.com",
	"password":"$pbkdf2-sha256$29000$tBZizDmHkLIWAsA4J4Rwrg$2K6y68IgBSKwnpAplRupNrKZJF9ZhV6w2Jj5eRRTqMw"
    },
    { 
    "id" : 2,
	"username":"kim",
	"email":"kim@gmail.com",
	"password":"$pbkdf2-sha256$29000$tBZizDmHkLIWAsA4J4Rwrg$2K6y68IgBSKwnpAplRupNrKZJF9ZhV6w2Jj5eRRTqMw"
    }]





class User():
 

    @staticmethod
    def create_user(username,email,password):
        role = 'user'
        id = len(users) + 1
        new_user = { 'id':id ,'username':username,'email':email,'password':password,'role':role}
        users.append(new_user)
        return new_user

# # find if email exists
    @staticmethod
    def find_by_email(email):
        return next((item for item in users if item["email"] == email), False)


# # find if username exists
    @staticmethod
    def find_by_username(username):
        return next((item for item in users if item["username"] == username), False)




#     # generate hash
    @staticmethod
    def generate_hash(raw_password):
        return sha256.hash(raw_password)

#     # compare user password with hashed password 
    @staticmethod
    def verify_hash(password,email):
         user = next((item for item in users if item["email"] == email), False)
         if user == False:
             return False
         return sha256.verify(password, user['password'] )
        





class Product():

# create a product by admin
        @staticmethod
        def create_product(name,price,quantity):
            id = len(products) + 1
            new_product = { 'id':id ,'name':name,'price':price,'quantity':quantity}
            products.append(new_product)
            return products

# fetch all products by admin
        @staticmethod
        def get_products():

            return products


# fetch a single product 
        @staticmethod
        def get_each_product(product_id):
            product_index= product_id - 1

            return products[product_index]


class Sale():

# create a sale record by store attendant
        @staticmethod
        def create_sale(description,items,total):
            id = len(cart) + 1
            order = { 'id':id ,'description':description,'items':items,'total':total}
            cart.append(order)
            return cart


# fetch all sales
        @staticmethod
        def get_sales():

            return cart



# fetch a single sale
        @staticmethod
        def get_each_sale(sale_id):
            sale_index = sale_id - 1
            return cart[sale_index]

