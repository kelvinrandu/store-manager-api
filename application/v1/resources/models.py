from flask_restful import Resource, reqparse
from psycopg2 import connect, extras
from flask import Flask, jsonify, request, make_response
from passlib.hash import pbkdf2_sha256 as sha256
from psycopg2 import sql
from psycopg2 import connect
from application.database import conn



cur = conn.cursor(cursor_factory=extras.RealDictCursor)


class User():

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password 
        self.role = 0
 
    def create_store_attendant(self):
       
        try:
            cur.execute(
                """
                INSERT INTO users(username, email, password,role)
                VALUES(%s,%s,%s,%s)""",
                (self.username, self.email, self.password, self.role))
         
                       
            return 'attendant registered succesful'
        

        except Exception as e:
            print(e)
            return ("ran into trouble registering you")

    @staticmethod
    def find_by_id(user_id):

        cur.execute("""SELECT * FROM users WHERE id='{}' """.format(user_id))
        rows = cur.fetchone()
        if rows :
            return True
               
        return False

    @staticmethod
    def find_by_email(email):

        cur.execute("""SELECT * FROM users WHERE email='{}' """.format(email))
        rows = cur.fetchone()
               
        return rows

    @staticmethod
    def is_admin(username):

        cur.execute("""SELECT * FROM users WHERE username='{}' """.format(username))
        rows = cur.fetchone()
        if rows :
            if rows['role'] == 1:
                return True
            return False
               
        return False

    @staticmethod
    def find_by_username(username):
      
            cur.execute("""SELECT * FROM users WHERE username='{}' """.format(username))
            rows = cur.fetchone()
            conn.commit()
            return rows
               
    @staticmethod
    def make_admin(attendant_id):
        role = 1
        try:
      
            cur.execute("""UPDATE users  SET role='{}'  WHERE id='{}' """.format(role,attendant_id))
            conn.commit()
        
            return 'store attendant has been made admin'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def generate_hash(raw_password):
        return sha256.hash(raw_password)
 
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

        
class Product():

    def __init__(self,name,price,quantity,min_stock,category_id,user_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.min_stock = min_stock 
        self.category_id = category_id
        self.user_id = user_id
      
    def create_new_product(self):

        try:
            cur.execute(
                """
                INSERT INTO products(name, price, quantity,min_stock,category_id,created_by)
                VALUES(%s,%s,%s,%s,%s,%s)""",
                (self.name, self.price,self.quantity,self.min_stock,self.category_id,self.user_id))

            conn.commit()
                                 
            return 'product created succesfully' 

        except Exception as e:
            print(e)
            return ("ran into trouble creating your product ")


    @staticmethod
    def find_by_id(product_id):

        cur.execute("""SELECT * FROM products WHERE id='{}' """.format(product_id))
        rows = cur.fetchone()
        if rows :
            return True
               
        return False

    @staticmethod
    def find_product_by_name(name):

        cur.execute("""SELECT * FROM products WHERE name='{}' """.format(name))
        rows = cur.fetchone()
               
        return rows

    @staticmethod
    def find_stock(product_id):

        cur.execute("""SELECT * FROM products WHERE id='{}' """.format(product_id))
        rows = cur.fetchone()
               
        return rows

    @staticmethod  
    def get_products():
        try:
      
            cur.execute("""SELECT * FROM products """)
            rows = cur.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def get_each_product(product_id):
        try:
      
            cur.execute("""SELECT * FROM products WHERE id='{}' """.format(product_id))
            rows = cur.fetchall()
            if not rows :
                return False
        
            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


    @staticmethod
    def edit_product(product_id,name,quantity,min_stock,category_id,user_id):
  
        try:
      
            cur.execute("""UPDATE products  SET name='{}', quantity='{}',  min_stock='{}', category_id='{}', created_by='{}' WHERE id='{}' """.format(name,quantity,min_stock,category_id,user_id,product_id))
            conn.commit()
        
            return 'product edited'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def updated_product(product_id,quantity):
  
        try:
      
            cur.execute("""UPDATE products  SET quantity='{}'  WHERE id='{}' """.format(quantity,product_id))
            conn.commit()
        
            return 'product price edited'
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def delete_product(product_id,user_id):
  
        try:
      
            cur.execute("""DELETE FROM products WHERE id='{}' """.format(product_id))
            conn.commit()
        
            return 'product deleted succesfully'
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def add_category_to_product(product_id,category_id,admin_id):
  
        try:
      
            cur.execute("""UPDATE products  SET category_id='{}'  WHERE id='{}' """.format(category_id,product_id))
            conn.commit()
        
            return 'category added to product'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

class Sale():

    def __init__(self,product_id,quantity,total,user_id):
        self.product_id = product_id
        self.quantity = quantity
        self.total = total
        self.user_id = user_id

    def create_new_sale(self):
        try:
            cur.execute(
                """
                INSERT INTO sales(product_id,quantity,total,created_by)
                VALUES(%s,%s,%s,%s)""",
            (self.product_id,self.quantity,self.total,self.user_id))
            conn.commit()          
                       
            return 'sale created succesfully'
        
        except Exception as e:
            print(e)
            return ("ran into trouble creating your sale ")

    @staticmethod
    def get_sales():
        try:
      
            cur.execute("""SELECT * FROM sales  """)
            rows = cur.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def get_my_sales(user_id):
        try:
            cur.execute("""SELECT * FROM sales WHERE created_by='{}'  """.format(user_id))
            rows = cur.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


    @staticmethod
    def get_each_sale(sale_id):
        try:
      
            cur.execute("""SELECT * FROM sales WHERE id='{}' """.format(sale_id))
            rows = cur.fetchall()
        
            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class Category():

    def __init__(self,name,user_id):
        self.name = name
        self.user_id = user_id

    def create_new_category(self):
        try:
            cur.execute(
                """
                INSERT INTO categories(name,created_by)
                VALUES(%s,%s)""",
            ( self.name,self.user_id))
            conn.commit()            
                       
            return 'category created succesfully'
        
        except Exception as e:
            print(e)
            return ("ran into trouble creating category ")

    @staticmethod
    def find_category_by_name(name):

        cur.execute("""SELECT * FROM categories WHERE name='{}' """.format(name))
        rows = cur.fetchone()
               
        return rows

    @staticmethod
    def get_category_by_id(category_id):
        try:
      
            cur.execute("""SELECT * FROM categories WHERE id='{}' """.format(category_id))
            rows = cur.fetchall()
            if not rows :
                return False
        
            return rows
       
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod  
    def get_categories():
        try:
      
            cur.execute("""SELECT * FROM categories  """)
            rows = cur.fetchall()

            return rows
        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def edit_category(category_id,name,user_id):
  
        try:
      
            cur.execute("""UPDATE categories  SET name='{}', created_by='{}' WHERE id='{}' """.format(name,user_id,category_id))
            conn.commit()
        
            return 'product edited'

        
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

    @staticmethod
    def delete_category(category_id,user_id):
  
        try:
      
            cur.execute("""DELETE FROM categories WHERE id='{}' """.format(category_id))
            conn.commit()
        
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