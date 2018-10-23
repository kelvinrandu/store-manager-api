from flask_restful import Resource,reqparse,Api
from flask import Flask,jsonify,request, make_response,Blueprint
import re
from application.v1.resources.models import users
from application.v1.resources.models import User
from application.v1.resources.models import Sale
from application.v1.resources.models import Product
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)




store_manager = Blueprint('api',__name__)

app = Flask(__name__)
api = Api(store_manager)




class UserRegistration(Resource):
    

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username cannot be blank', type=str)
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank', type=str)
  

    # handle create user logic

    def post(self):
        

        # remove all whitespaces from input
        args =  UserRegistration.parser.parse_args()
        raw_password = args.get('password')
        confirm_password = args.get('confirm_password')
        username = args.get('username').strip()
        email = args.get('email')



        # validate user input
        email_format = re.compile(
        r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)")
        username_format = re.compile(r"(^[A-Za-z0-9-]+$)")


        if not email:
            return make_response(jsonify({'message': 'email can not be empty'}),400)
        if not raw_password:
            return make_response(jsonify({'message': 'password cannot be empty'}),400)
        if not username:
            return make_response(jsonify({'message': 'username cannot be empty'}),400)
        if len(raw_password) < 6:
            return make_response(jsonify({'message' : 'Password should be atleast 6 characters'}), 400)
        if not (re.match(email_format, email)):
            return make_response(jsonify({'message' : 'Invalid email'}), 400)
        if not (re.match(username_format, username)):
            return make_response(jsonify({'message' : 'Please input only characters and numbers'}), 400)



     

        # # # upon successful validation check if user by the username exists 
        this_user = User.find_by_username(username)
        if this_user != False:
            return {'message': 'username already exist'},400

         # # # upon successful validation check if user by the email exists 
        this_user = User.find_by_email(email)
        if this_user != False:
            return {'message': 'email already exist'},400 
  

        # send validated user input to user model
        new_user = User(
            username=username ,
            email=email,
            password = User.generate_hash(password)
     
        )

        # attempt creating a new user in user model
        try:
            result = new_user.create_store_attendant()
            access_token = create_access_token(identity = username)
            refresh_token = create_refresh_token(identity = username)
            return {
                'message': 'User was created succesfully',
                'status': 'ok',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': result
                },201

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

 
        # # # attempt sending user to user model
        # try:
        #     result= User.create_user(username,email,password)

        #     access_token = create_access_token(identity = username)
        #     refresh_token = create_refresh_token(identity = username)

        #     return {
        #         'message': 'User was created succesfully',
        #         'status': 'ok',
        #         'access_token': access_token,
        #         'refresh_token': refresh_token,
        #         'user': result
        #         }, 201

        # except Exception as e:
        #     print(e)
        #     return {'message': 'Something went wrong'}, 500
 


# handle user login
class UserLogin(Resource):
    
    # validate user input
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank')


    def post(self):

        # check for white spaces
        args =  UserLogin.parser.parse_args()
        password = args.get('password').strip()
        email = args.get('email').strip()
        if not email:
            return {'message': 'email can not be empty'},400
        if not password:
            return {'message': 'password cannot be empty'},400

  # upon successful validation check if user by the email exists 
        current_user = User.find_by_email(email)
        if current_user is None:
            return {'message': 'email {} doesn\'t exist'.format(email)},400


        
        # compare user's password and the hashed password in database
        if User.verify_hash(password, current_user['password']):
            access_token = create_access_token(identity =  current_user['name'])
            refresh_token = create_refresh_token(identity = current_user['name'])
            return {
                'message': 'User was created succesfully',
                'status': 'ok',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': current_user

                },200
        else:
            return {'message': 'Wrong credentials'},400





# handles posting of product by admin
class PostProducts(Resource):
       

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
        parser.add_argument('price', required=True, help=' Product price cannot be blank',type=int)
        parser.add_argument('quantity', required=True, help='Product quantity cannot be blank', type=int)

        @jwt_required
        def post(self):

 # validate input

            args =  PostProducts.parser.parse_args()
            name = args.get('name').strip()
            price = args.get('price')
            quantity = args.get('quantity')


# error response
            if not name:
                return make_response(jsonify({'message': 'product name can not be empty'}),400)
            if not price:
                return make_response(jsonify({'message': 'price of product cannot be empty'}),400)
            if not quantity:
                return make_response(jsonify({'message': 'quantity of product cannot be empty'}),400)



            try:

                products = Product.create_product(name,price,quantity)

                return {
                'message': 'product created successfully','product': products,'status':'ok'

                 },201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500



# fetch all product
class GetProducts(Resource):
        @jwt_required
        def get(self):
            products = Product.get_products()
            
            return {'message': 'products retrieved succesfully','status':'ok','products': products}, 200



# fetch a specific product
class EachProduct(Resource):
        @jwt_required
        def get(self,product_id):

            products = Product.get_each_product(product_id)

            return {'message': 'product retrieved succesfully','status':'ok','products': products}, 200

# delete  specific product
class DeleteProduct(Resource):
        @jwt_required
        def delete(self,product_id):

# modify specific product
class ModifiProduct(Resource):
        @jwt_required
        def put(self,product_id):

# handles posting of a sale by store attendant

class PostSale(Resource):
        
        # validate sale input

        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True, help='Sale description  cannot be blank', type=str)
        parser.add_argument('items', required=True, help=' items cannot be blank')

        @jwt_required
        def post(self):

            args =  PostSale.parser.parse_args()
            description = args.get('description').strip()
            items = args.get('items')
            total = 400
 
 # error response
            if not description:
                return make_response(jsonify({'message': 'Sale description  can not be empty'}),400)
            if not items:
                return make_response(jsonify({'message': 'Sale items  can not be empty'}),400)

            try:

                sale = Sale.create_sale(description,items,total)

                return {
                'message': 'Sale created successfully','sales': sale,'status':'ok'

                 },201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500



# fetch all product
class GetSales(Resource):

        @jwt_required
        def get(self):
                
            result = Sale.get_sales()
            return {'message': 'sales retrieved succesfully','status':'ok','sale':result}, 200



# fetch each sale
class EachSale(Resource):

        @jwt_required
        def get(self,sale_id):

            result = Sale.get_each_sale(sale_id)

            return {'message': 'sale retrieved succesfully','status':'ok','products': result}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

# test jwt
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

# routes
api.add_resource(UserRegistration, '/api/v1/auth/signup/')
api.add_resource(UserLogin, '/api/v1/auth/login/')
api.add_resource(UserLogoutAccess, '/api/v1/logout/access/')
api.add_resource(UserLogoutRefresh, '/api/v1/logout/refresh/')
# api.add_resource(TokenRefresh, '/api/v1/token/refresh/')
api.add_resource(SecretResource, '/api/v1/secret/')
api.add_resource(PostProducts, '/api/v1/products/')
api.add_resource(GetProducts, '/api/v1/products/')
api.add_resource(EachProduct, '/api/v1/product/<int:product_id>/')
api.add_resource(DeleteProduct, '/api/v1/product/<int:product_id>/')
api.add_resource(ModifyProduct, '/api/v1/product/<int:product_id>/')
api.add_resource(PostSale, '/api/v1/sales/')
api.add_resource(GetSales, '/api/v1/sales/')
api.add_resource(EachSale, '/api/v1/sale/<int:sale_id>/')
