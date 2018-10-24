from flask_restful import Resource,reqparse
from flask import Flask,jsonify,request, make_response
from passlib.hash import pbkdf2_sha256 as sha256
from psycopg2 import sql
from psycopg2 import connect
from application.database import DatabaseConnect

# users= []
# products = []
# sales = []
db = DatabaseConnect()


class User():

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password 
        self.role = 0


  
    def create_store_attendant(self):
       
        try:
            db.cursor.execute(
                """
                INSERT INTO users(username, email, password,role)
                VALUES(%s,%s,%s,%s)""",
                (self.username, self.email,self.password,self.role))

            
                       
            return 'attendant registered succesful'
        

        except Exception as e:
            print(e)
            return ("ran into trouble registering you")


# checks if email exists
    @staticmethod
    def find_by_email(email):

        db.cursor.execute("""SELECT * FROM users WHERE email='{}' """.format(email))
        rows = db.cursor.fetchone()
               
        return rows

# checks if username exists
    @staticmethod
    def find_by_username(username):

        db.cursor.execute("""SELECT * FROM users WHERE username='{}' """.format(username))
        rows = db.cursor.fetchone()
               
        return rows


    # make admin
    @staticmethod
    def make_admin(user_id):
        role = 1
        try:
      
            db.cursor.execute("""UPDATE users  SET role='{}'  WHERE id='{}' """.format(role,user_id))
            # db.cursor.commit()
        
            return 'store attendant has been made admin'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

#     # generate hash
    @staticmethod
    def generate_hash(raw_password):
        return sha256.hash(raw_password)

    # compare user password with hashed password 
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

        

# this class handles product
class Product():

    # product class constructor
    def __init__(self,name,price,quantity,user_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.user_id = user_id

# create a product by admin
        
    def create_new_product(self):

        try:
            db.cursor.execute(
                """
                INSERT INTO products(name, price, quantity,created_by)
                VALUES(%s,%s,%s,%s)""",
                (self.name, self.price,self.quantity,self.user_id))

            
                       
            return 'product created succesfully'
        

        except Exception as e:
            print(e)
            return ("ran into trouble creating your product ")

# checks if product name exists
    @staticmethod
    def find_product_by_name(name):

        db.cursor.execute("""SELECT * FROM products WHERE name='{}' """.format(name))
        rows = db.cursor.fetchone()
               
        return rows

# fetch all products by admin
    @staticmethod  
    def get_products():
        try:
      
            db.cursor.execute("""SELECT * FROM products  """)
            # db.cursor.commit()
            rows = db.cursor.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


# fetch a single product 
    @staticmethod
    def get_each_product(product_id):
        try:
      
            db.cursor.execute("""SELECT * FROM products WHERE id='{}' """.format(product_id))
            # db.cursor.commit()
            rows = db.cursor.fetchall()
        
            return rows

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


# checks if product name exists
    @staticmethod
    def find_product_by_name(name):

        db.cursor.execute("""SELECT * FROM products WHERE name='{}' """.format(name))
        rows = db.cursor.fetchone()
               
        return rows

  #  modify an entry
    @staticmethod
    def edit_product(product_id,name,user_id):
  
        try:
      
            db.cursor.execute("""UPDATE products  SET name='{}', created_by='{}' WHERE id='{}' """.format(name,user_id,product_id))
            # db.cursor.commit()
        
            return 'product edited'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

  #  delete a product
    @staticmethod
    def delete_product(product_id,user_id):
  
        try:
      
            db.cursor.execute("""DELETE FROM products WHERE id='{}' """.format(product_id))
            # db.cursor.commit()
        
            return 'product deleted succesfully'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

class Sale():

# product class constructor
    def __init__(self,description,items,total,user_id):
        self.description = description
        self.items = items
        self.total = total
        self.user_id = user_id

# create a sale record by store attendant
    def create_new_sale(self):
        try:
            db.cursor.execute(
                """
                INSERT INTO sales(description, items, total,created_by)
                VALUES(%s,%s,%s,%s)""",
            (self.description, self.items,self.total,self.user_id))

            
                       
            return 'sale created succesfully'
        

        except Exception as e:
            print(e)
            return ("ran into trouble creating your sale ")


# fetch all sales
    @staticmethod
    def get_sales():
        try:
      
            db.cursor.execute("""SELECT * FROM sales  """)
            # db.cursor.commit()
            rows = db.cursor.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


# fetch a single sale
    @staticmethod
    def get_each_sale(sale_id):
        try:
      
            db.cursor.execute("""SELECT * FROM sales WHERE id='{}' """.format(sale_id))
            # db.cursor.commit()
            rows = db.cursor.fetchall()
        
            return rows

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class Category():

# product class constructor
    def __init__(self,name,user_id):
        self.name = name
        self.user_id = user_id

# create a sale record by store attendant
    def create_new_category(self):
        try:
            db.cursor.execute(
                """
                INSERT INTO categories( name,created_by)
                VALUES(%s,%s)""",
            ( self.name,self.user_id))

            
                       
            return 'category created succesfully'
        

        except Exception as e:
            print(e)
            return ("ran into trouble creating category ")

# checks if category name exists
    @staticmethod
    def find_category_by_name(name):

        db.cursor.execute("""SELECT * FROM categories WHERE name='{}' """.format(name))
        rows = db.cursor.fetchone()
               
        return rows

# fetch all categoies by admin
    @staticmethod  
    def get_categories():
        try:
      
            db.cursor.execute("""SELECT * FROM categories  """)
            # db.cursor.commit()
            rows = db.cursor.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

  #  modify an entry
    @staticmethod
    def edit_category(category_id,name,user_id):
  
        try:
      
            db.cursor.execute("""UPDATE categories  SET name='{}', created_by='{}' WHERE id='{}' """.format(name,user_id,category_id))
            # db.cursor.commit()
        
            return 'product edited'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

  #  delete a category
    @staticmethod
    def delete_category(category_id,user_id):
  
        try:
      
            db.cursor.execute("""DELETE FROM categories WHERE id='{}' """.format(category_id))
            # db.cursor.commit()
        
            return 'product deleted succesfully'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class RevokedTokenModel():
    # __tablename__ = 'revoked_tokens'
    # id = db.Column(db.Integer, primary_key = True)
    # jti = db.Column(db.String(120))
    
    def add(self):
        # db.session.add(self)
        # db.session.commit()
        pass
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        # query = cls.query.filter_by(jti = jti).first()
        # return bool(query)
        pass