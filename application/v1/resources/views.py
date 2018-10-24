from flask_restful import Resource,reqparse,Api
from flask import Flask,jsonify,request, make_response,Blueprint
import re
from application.v1.resources.models import User
from application.v1.resources.models import Sale
from application.v1.resources.models import Product
from application.v1.resources.models import Category
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
        # confirm_password = args.get('confirm_password')
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



     
        
        # # # # upon successful validation check if user by the username exists 
        this_user = User.find_by_username(username)
        if this_user:
            return {'message': 'username already exist'},400

         # # # upon successful validation check if user by the email exists 
        this_user = User.find_by_email(email)
        if this_user:
            return {'message': 'email already exist'},400 
  

        # send validated user input to user model
        new_user = User(
            username=username ,
            email=email,
            password = User.generate_hash(raw_password)
     
        )


        # attempt creating a new user in user model
        try:
            result = new_user.create_store_attendant()
            access_token = create_access_token(identity = username)
            refresh_token = create_refresh_token(identity = username)
            return {
                'message': 'Store attendant was created succesfully',
                'status': 'ok',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': result
                },201

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

 

 


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

        # upon successful validation check if user by the email exists in database and return response if not
        current_user = User.find_by_email(email)
        if current_user is None:
            return {'message': 'email {} doesn\'t exist'.format(email)},400

        
        # compare user's password and the hashed password in database
        if User.verify_hash(password, current_user['password']):
            access_token = create_access_token(identity =  current_user['username'])
            refresh_token = create_refresh_token(identity = current_user['username'])
            return {
                'message': 'User was logged in succesfully',
                'status':'ok',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': current_user['username']

                },200
        else:
            return {'message': 'Wrong credentials'},400





# handles posting of product by admin
class PostProducts(Resource):
       

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
        parser.add_argument('price', required=True, help=' Product price cannot be blank',type=int)
        parser.add_argument('quantity', required=True, help='Product quantity cannot be blank', type=int)
        parser.add_argument('user_id', required=True, help='User_id quantity cannot be blank', type=int)

        @jwt_required
        def post(self):

 # validate input

            args =  PostProducts.parser.parse_args()
            name = args.get('name').strip()
            price = args.get('price')
            user_id = args.get('user_id')
            quantity = args.get('quantity')


# error response
            if not name:
                return make_response(jsonify({'message': 'product name can not be empty'}),400)
            if not price:
                return make_response(jsonify({'message': 'price of product cannot be empty'}),400)
            if not quantity:
                return make_response(jsonify({'message': 'quantity of product cannot be empty'}),400)
            if not user_id:
                return make_response(jsonify({'message': 'quantity of product cannot be empty'}),400)

            this_product = Product.find_product_by_name(name)
            if this_product:
                return {'message': 'product already exist'},400 

            new_product = Product(
                name=name ,
                price=price,
                quantity = quantity,
                user_id = user_id
     
            )


            try:

                products = new_product.create_new_product()

                return {
                'message': 'product created successfully','status':'ok'

                 },201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500



# fetch all product
class GetProducts(Resource):
        @jwt_required
        def get(self):
            if Product.get_products() :
                rows=  Product.get_products()
                return jsonify({'message': 'product retrieved succesfully','status':'ok','products': rows})
            return jsonify({'message':'no products yet'})



# fetch a specific product
class EachProduct(Resource):
        @jwt_required
        def get(self,product_id):
            rows=  Product.get_each_product(product_id)
            if rows:
   
                return jsonify({'message': 'product retrieved succesfully','status':'ok','products': rows},200)
            else:
                return jsonify({'message':'not found' }),404

# delete  specific product
class DeleteProduct(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, help='title cannot be blank', type=int)
 

    @jwt_required
    def delete(self,product_id):

        args =  DeleteProduct.parser.parse_args()
        user_id = args.get('user_id')


        # attempt delete product
        try:
            Product.delete_product(product_id,user_id)

            return {
                'message': 'Product  was successfuly deleted'

                },200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


# modify an  entry
class ModifyProduct(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, help='title cannot be blank', type=int)
    parser.add_argument('name', required=True, help='body cannot be blank', type=str)


    @jwt_required
    def put(self,product_id):

        args =  ModifyProduct.parser.parse_args()
        user_id = args.get('user_id')
        name = args.get('name').strip()

   
        

        # attempt modify product
        try:
            Product.edit_product(product_id,name,user_id)

            return {
                'message': 'Product  was successfuly edited'

                }

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500



# handles posting of a sale by store attendant

class PostSale(Resource):
        
        # validate sale input

        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True, help='Sale description  cannot be blank', type=str)
        parser.add_argument('items', required=True, help=' items cannot be blank')
        parser.add_argument('user_id', required=True, help='User_id cannot be blank', type=int)

        @jwt_required
        def post(self):

            args =  PostSale.parser.parse_args()
            description = args.get('description').strip()
            items = args.get('items')
            user_id= args.get('user_id')
            total = 400
 
 # error response
            if not description:
                return make_response(jsonify({'message': 'Sale description  can not be empty'}),400)
            if not items:
                return make_response(jsonify({'message': 'Sale items  can not be empty'}),400)
            if not user_id:
                return make_response(jsonify({'message': 'user_id  can not be empty'}),400)


            new_sale = Sale(
                description=description ,
                items=items,
                total=total,
                user_id = user_id
     
            )


            try:

                sales = new_sale.create_new_sale()

                return {
                'message': 'sale created successfully','status':'ok'

                 },201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500



# fetch all product
class GetSales(Resource):

        @jwt_required
        def get(self):
 
            if Sale.get_sales() :
                rows=  Sale.get_sales()
                return jsonify({'message': 'sales retrieved succesfully','status':'ok','sale':rows})
            return jsonify({'message':'no sales yet'})
                




# fetch each sale
class EachSale(Resource):

        @jwt_required
        def get(self,sale_id):
            rows=  Sale.get_each_sale(sale_id)
            if rows:
                return jsonify({'message': 'sale retrieved succesfully','status':'ok','products': rows},200)
            else:
                return jsonify({'message':'not found' }),404


#  admin create  category
class PostCategory(Resource):

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
        parser.add_argument('user_id', required=True, help='User_id quantity cannot be blank', type=int)

        @jwt_required
        def post(self):

 # validate input

            args =  PostCategory.parser.parse_args()
            name = args.get('name').strip()
            user_id = args.get('user_id')



# error response
            if not name:
                return make_response(jsonify({'message': 'category name can not be empty'}),400)

            if not user_id:
                return make_response(jsonify({'message': 'user id  cannot be empty'}),400)

            this_category = Category.find_category_by_name(name)
            if this_category:
                return {'message': 'product already exist'},400 

            new_category = Category(
                name=name ,
                user_id = user_id
     
            )


            try:

                category = new_category.create_new_category()

                return {
                'message': 'category created successfully','status':'ok'

                 },201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500


#  adminpost category
class GetCategory(Resource):
    @jwt_required
    def get(self):
 
        if Category.get_categories() :
            rows=  Category.get_categories()
            return jsonify({'message': 'categories retrieved succesfully','status':'ok','sale':rows})
        return jsonify({'message':'no categories added yet'})


#  admin modify category
class ModifyCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, help='title cannot be blank', type=int)
    parser.add_argument('name', required=True, help='body cannot be blank', type=str)


    @jwt_required
    def put(self,category_id):

        args =  ModifyCategory.parser.parse_args()
        user_id = args.get('user_id')
        name = args.get('name').strip()

# error response
        if not name:
            return make_response(jsonify({'message': 'category name can not be empty'}),400)

        if not user_id:
            return make_response(jsonify({'message': 'user id  cannot be empty'}),400)

        # attempt modify category
        try:
            Category.edit_category(category_id,name,user_id)

            return {
                'message': 'Category  was successfuly edited'

                }

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

#  admin delete category
class DeleteCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, help='title cannot be blank', type=int)
 

    @jwt_required
    def delete(self,category_id):

        args =  DeleteProduct.parser.parse_args()
        user_id = args.get('user_id')

        if not user_id:
            return make_response(jsonify({'message': 'user id  cannot be empty'}),400)

        # attempt delete category
        try:
            Category.delete_category(category_id,user_id)

            return {
                'message': 'category  was successfuly deleted',
                'status':'ok'

                },200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

# make store attendant admin
class MakeAdmin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('admin_id', required=True, help='admin id cannot be blank', type=int)

    @jwt_required
    def post(self,user_id):
        args =  MakeAdmin.parser.parse_args()
        admin_id = args.get('admin_id')

        if not admin_id:
            return make_response(jsonify({'message': 'admin id  cannot be empty'}),400)   

 # attempt to make store attendant admin
        try:
            User.make_admin(user_id)

            return {
                'message': 'attendant successfuly made admin',
                'status':'ok'

                },200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

# add category to product
class AddCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('admin_id', required=True, help='admin id cannot be blank', type=int)
    parser.add_argument('category_id', required=True, help='category id cannot be blank', type=int)

    @jwt_required
    def post(self,product_id):
        args =  AddCategory.parser.parse_args()
        admin_id = args.get('admin_id')
        category_id = args.get('category_id')

        if not admin_id:
            return make_response(jsonify({'message': 'admin id  cannot be empty'}),400)   
        if not category_id:
            return make_response(jsonify({'message': 'category id  cannot be empty'}),400) 

        

#  attempt to add category to product
        try:
            Product.add_category_to_product(product_id,category_id,admin_id)

            return {
                'message': 'category added succesfully',
                'status':'ok'

                },200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500




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
api.add_resource(DeleteProduct, '/api/v1/products/<int:product_id>/')
api.add_resource(ModifyProduct, '/api/v1/products/<int:product_id>/')
api.add_resource(PostSale, '/api/v1/sales/')
api.add_resource(GetSales, '/api/v1/sales/')
api.add_resource(EachSale, '/api/v1/sale/<int:sale_id>/')
api.add_resource(PostCategory, '/api/v1/categories/')
api.add_resource(GetCategory, '/api/v1/categories/')
api.add_resource(ModifyCategory, '/api/v1/categories/<int:category_id>/')
api.add_resource(DeleteCategory, '/api/v1/categories/<int:category_id>/')
api.add_resource(MakeAdmin, '/api/v1/make/admin/<int:user_id>/')
api.add_resource(AddCategory, '/api/v1/products/add/category/<int:product_id>/')
