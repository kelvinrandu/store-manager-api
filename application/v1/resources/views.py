import re
import datetime
from flask_restful import Resource,reqparse,Api
from flask import Flask,jsonify,request, make_response,Blueprint
from application.v1.resources.models import Product,Sale,User,Category 
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from functools import wraps

store_manager = Blueprint('api', __name__)

app = Flask(__name__)
api = Api(store_manager)

def admin_only(f):
    ''' Deny access if the user is not admin '''
    @wraps(f)
    def decorator_func(*args,**kwargs):
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        if  user['role'] == 0 :
            return {'message': 'unauthorized access'}, 401
        return f(*args, **kwargs)
    return decorator_func
def attendant_only(f):
    ''' Deny access if the user is not admin '''
    @wraps(f)
    def decorator_func(*args,**kwargs):
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        if  user['role'] == 1 :
            return {'message': 'unauthorized '}, 401
        return f(*args, **kwargs)
    return decorator_func


class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='Username cannot be blank')
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank', type=str)
    
    @jwt_required
    @admin_only
    def post(self):

        args = UserRegistration.parser.parse_args()
        raw_password = args.get('password')
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        user_id = user['id']
        username = args.get('username').strip()
        email = args.get('email')
        
        email_format = re.compile(
        r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)")
        username_format = re.compile(r"(^[a-zA-Z]+$)")
        if not email :
            return make_response(jsonify({'message': 'email can not be empty'}),400)
        if not user_id:
            return make_response(jsonify({'message': 'user id can not be empty'}),400)
        if not raw_password:
            return make_response(jsonify({'message': 'password cannot be empty'}),400)
        if not username:
            return make_response(jsonify({'message': 'username is empty'}),400)
        if len(raw_password) < 6:
            return make_response(jsonify({'message': 'Password should be atleast 6 characters'}), 400)
        if not (re.match(email_format, email)):
            return make_response(jsonify({'message': 'Invalid email'}), 400)
        if not (re.match(username_format, username)):
            return make_response(jsonify({'message': 'Please input only characters '}), 400)

        current_username = User.find_by_username(username)
        if current_username:
            return {'message': 'username already exist'}, 400

        this_user = User.find_by_email(email)
        if this_user:
            return {'message': 'email already exist'}, 400 
  
        new_user = User(
            username=username.lower(),
            email=email.lower(),
            password=User.generate_hash(raw_password)
     
        )

        try:
            result = new_user.create_store_attendant()

            return {
                'message': 'Store attendant has been created succesfully',
                'status': 'ok',
                'username ': username
                }, 201

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='Email cannot be blank')
    parser.add_argument('password', required=True, help='Password cannot be blank')

    def post(self):

        args = UserLogin.parser.parse_args()
        password = args.get('password').strip()
        email = args.get('email').strip()
        if not email:
            return {'message': 'email can not be empty'},400
        if not password:
            return {'message': 'password cannot be empty'},400

        current_user = User.find_by_email(email.lower())
        if current_user is None:
            return {'message': 'email {} doesn\'t exist'.format(email)},400

        if User.verify_hash(password, current_user['password']):
            access_token = create_access_token(identity =  current_user['username'],expires_delta=datetime.timedelta(hours=1))

            return {
                'message': 'User has logged in succesfully',
                'status':'ok',
                'access_token': access_token,
                'username': current_user['username']

                },200
        else:
            return {'message': 'Wrong credentials'},400


class PostProducts(Resource):
       
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Product name cannot be blank')
        parser.add_argument('price', required=True, help=' Product price cannot be blank')
        parser.add_argument('quantity', required=True, help='Product quantity cannot be blank')
        parser.add_argument('min_stock', required=True, help='Minimum stock quantity cannot be blank')
        parser.add_argument('category_id', required=True, help='category id cannot be blank')

        @jwt_required
        @admin_only
        def post(self):

            args = PostProducts.parser.parse_args()
            name = args.get('name').strip()
            price = args.get('price')
            category_id = args.get('category_id')
            user_name = get_jwt_identity()
            user = User.find_by_username(user_name)
            user_id = user['id']
            quantity = args.get('quantity')
            min_stock = args.get('min_stock')
            number_format = re.compile(r"(^[0-9])")


            if not name:
                return make_response(jsonify({'message': 'product name can not be empty'}),400)
            if not price:
                return make_response(jsonify({'message': 'price of product cannot be empty'}),400)
            if not quantity:
                return make_response(jsonify({'message': 'quantity of product cannot be empty'}),400)
            if not user_id:
                return make_response(jsonify({'message': 'user id  cannot be empty'}),400)
            if not min_stock:
                return make_response(jsonify({'message': 'minimum stock  cannot be empty'}),400)
            if not (re.match(number_format, price)):
                return make_response(jsonify({'message': 'Please input only integers '}), 400)
            if not (re.match(number_format, quantity)):
                return make_response(jsonify({'message': 'Please input only integers '}), 400)
            if not (re.match(number_format, min_stock)):
                return make_response(jsonify({'message': 'Please input only integers '}), 400) 
            if not (re.match(number_format, category_id)):
                return make_response(jsonify({'message': 'Please input only intergers '}), 400)  
            if quantity < min_stock:
                return make_response(jsonify({'message': 'quantity cannot be  less than minimum stock '}),400)           

            this_product = Product.find_product_by_name(name)
            if this_product:
                return {'message': 'product  by this name already exist'}, 400 

            this_category = Category.get_category_by_id(category_id)
            if this_category == False:
                return {'message': 'category with this id does not exist'}, 400 

            new_product = Product(
                name=name,
                price=price,
                quantity=quantity,
                min_stock=min_stock,
                user_id=user_id,
                category_id=category_id
     
            )

            try:
                products = new_product.create_new_product()

                return {
                    'message': 'product created successfully', 'status': 'ok'

                 }, 201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500

class GetProducts(Resource):
        @jwt_required
        def get(self):
            if Product.get_products() :
                rows= Product.get_products()
                return jsonify({'message': 'product retrieved succesfully','status':'ok','products': rows})
            return jsonify({'message':'no products yet'})

class EachProduct(Resource):
        @jwt_required
        def get(self, product_id):
            this_product = Product.find_by_id(product_id)
            if this_product != True:
                return make_response(jsonify({'message': 'no product by the provided id exists'}), 400)
            rows = Product.get_each_product(product_id)
            return jsonify({'message': 'product retrieved succesfully', 'status':'ok','products': rows[0]},200)

class DeleteProduct(Resource):

    @jwt_required
    @admin_only
    def delete(self, product_id):

        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        user_id = user['id']

        try:
            Product.delete_product(product_id, user_id)

            return {
                'message': 'Product  was successfuly deleted'

                }, 200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

class ModifyProduct(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='name cannot be blank', type=str)
    parser.add_argument('quantity', required=True, help='quantity cannot be blank', type=int)
    parser.add_argument('min_stock', required=True, help='minimum stock cannot be blank', type=int)
    parser.add_argument('category_id', required=True, help='category id cannot be blank', type=int)
    
    @jwt_required
    @admin_only
    def put(self, product_id):

        args = ModifyProduct.parser.parse_args()
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        user_id = user['id']
        name = args.get('name').strip()
        quantity = args.get('quantity')
        min_stock = args.get('min_stock')
        category_id = args.get('category_id')

        this_product = Product.find_product_by_name(name)
        if this_product:
            return {'message': 'product  by this name already exist'}, 400 
        
        try:
            Product.edit_product(product_id, name, quantity, min_stock, category_id, user_id)
            product = Product.find_product_by_name(name)
            if product == False:
                return {'message': 'could not fetch product'}, 400 


            return jsonify({
                'message': 'Product  was successfuly edited',
                'product': product

                })

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class PostSale(Resource):
        
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', required=True, help='product id cannot be blank', type=int)
        parser.add_argument('quantity', required=True, help='quantity cannot be blank', type=int)

        @jwt_required
        @attendant_only
        def post(self):

            args = PostSale.parser.parse_args()
            product_id = args.get('product_id')
            user_name = get_jwt_identity()
            user = User.find_by_username(user_name)
            user_id = user['id']
            quantity= args.get('quantity')
            total = 0

             
            if not product_id:
                return make_response(jsonify({'message': 'product id  can not be empty'}), 400)
            if not user_id:
                return make_response(jsonify({'message': 'user_id  can not be empty'}), 400)
            if not quantity:
                return make_response(jsonify({'message': 'quantity of product  can not be empty'}), 400)

            this_product = Product.find_by_id(product_id)
            if this_product != True:
                return make_response(jsonify({'message': 'no product by the provided id exists'}), 400)

            this_user = User.find_by_id(user_id)
            if this_user != True:
                return make_response(jsonify({'message': 'no user by the provided id exists'}), 400)

            stock = Product.find_stock(product_id)
           
            min_stock = stock['min_stock']
            stock_quantity = stock['quantity']
            gap = stock_quantity - min_stock
                    
            if quantity > gap :
                 return {'message': 'only a maximum of  {}  is allowed '.format(gap)},400

            total = stock['price'] * quantity
            remaining_quantity = stock_quantity - quantity
           
            new_sale = Sale(
                product_id=product_id,
                quantity=quantity,
                total=total,
                user_id = user_id
     
            )

            try:
                sales = new_sale.create_new_sale()
                Product.updated_product(product_id,remaining_quantity)

                return {
                'message': 'sale created successfully','status':'ok'

                 }, 201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500

class GetSales(Resource):
        
        @jwt_required
        @admin_only
        def get(self):
 
            if Sale.get_sales() :
                rows=  Sale.get_sales()
                return jsonify({'message': 'sales retrieved succesfully','status':'ok','sale':rows})
            return jsonify({'message':'no sales yet'})


class GetMySales(Resource):

        @jwt_required
        @attendant_only
        def get(self):
            user_name = get_jwt_identity()
            user = User.find_by_username(user_name)
            user_id = user['id']
 
            if Sale.get_my_sales(user_id) :
                rows=  Sale.get_my_sales(user_id)
                return jsonify({'message': 'my sales retrieved succesfully','status':'ok','sale':rows[0]})
            return jsonify({'message':'not made sales yet'})              

class EachSale(Resource):
        
        @jwt_required
        @admin_only
        def get(self,sale_id):
            rows=  Sale.get_each_sale(sale_id)
            if rows:
                return jsonify({'message': 'sale retrieved succesfully','status':'ok','products': rows},200)
            else:
                return jsonify({'message':'not found' }),404


class PostCategory(Resource):

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
        @jwt_required
        @admin_only
        def post(self):

            args =  PostCategory.parser.parse_args()
            name = args.get('name').strip()
            user_name = get_jwt_identity()
            user = User.find_by_username(user_name)
            user_id = user['id']
            


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

                new_category.create_new_category()

                return {
                'message': 'category created successfully','status':'ok'

                 },201

            except Exception as e:
                print(e)
                return {'message': 'Something went wrong'}, 500


class GetCategory(Resource):
    @jwt_required
    def get(self):
 
        if Category.get_categories() :
            rows=  Category.get_categories()
            return jsonify({'message': 'categories retrieved succesfully','status':'ok','categories':rows})
        return jsonify({'message':'no categories added yet'})


class ModifyCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='body cannot be blank', type=str)
   
    @jwt_required
    @admin_only
    def put(self,category_id):

        args =  ModifyCategory.parser.parse_args()
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        user_id = user['id']
        name = args.get('name').strip()

        if not name:
            return make_response(jsonify({'message': 'category name can not be empty'}),400)

        if not user_id:
            return make_response(jsonify({'message': 'user id  cannot be empty'}),400)

        this_category= Category.get_category_by_id(category_id)
        if this_category == False:
            return make_response(jsonify({'message': 'category you are trying to edit does not exist'}),400)

        this_name= Category.find_category_by_name(name)
        if this_name :
            return make_response(jsonify({'message': 'category name already exists'}),400)

        try:
            Category.edit_category(category_id,name,user_id)
            category= Category.find_category_by_name(name)

            return jsonify({
                'message': 'Category  was successfuly edited',
                'category':category

                })

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class DeleteCategory(Resource):

  
    @jwt_required
    @admin_only
    def delete(self,category_id):

        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        user_id = user['id']

        if not user_id:
            return make_response(jsonify({'message': 'user id  cannot be empty'}),400)

        this_category= Category.get_category_by_id(category_id)
        if this_category == False:
            return make_response(jsonify({'message': 'category you are trying to delete does not exist'}),400)

        try:
            Category.delete_category(category_id,user_id)

            return {
                'message': 'category  was successfuly deleted',
                'status':'ok'

                },200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

class MakeAdmin(Resource):

    @jwt_required
    @admin_only
    def post(self,attendant_id):
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        user_id = user['id']
           

        if not user_id:
            return make_response(jsonify({'message': 'admin id  cannot be empty'}),400)

        attendant = User.find_by_id(attendant_id)  
        if attendant != True:
            return make_response(jsonify({'message': 'attendant  cannot be found'}),400)

        try:
            User.make_admin(attendant_id)

            return {
                'message': 'attendant successfuly made admin',
                'status':'ok'

                },200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500

class AddCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category_id', required=True, help='category id cannot be blank', type=int)

    @jwt_required
    @admin_only
    def post(self,product_id):
        args =  AddCategory.parser.parse_args()      
        category_id = args.get('category_id')
        user_name = get_jwt_identity()
        user = User.find_by_username(user_name)
        admin_id = user['id']

        if not admin_id:
            return make_response(jsonify({'message': 'admin id  cannot be empty'}),400)   
        if not category_id:
            return make_response(jsonify({'message': 'category id  cannot be empty'}),400) 

        
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


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        # jti = get_raw_jwt()['jti']
        # try:
        #     revoked_token = RevokedTokenModel(jti = jti)
        #     revoked_token.add()
        #     return {'message': 'Access token has been revoked'}
        # except:
        #     return {'message': 'Something went wrong'}, 500
        pass





api.add_resource(UserRegistration, '/api/v1/auth/signup/')
api.add_resource(UserLogin, '/api/v1/auth/login/')
api.add_resource(UserLogoutAccess, '/api/v1/logout/access/')
api.add_resource(PostProducts, '/api/v1/products/')
api.add_resource(GetProducts, '/api/v1/products/')
api.add_resource(EachProduct, '/api/v1/product/<int:product_id>/')
api.add_resource(DeleteProduct, '/api/v1/products/<int:product_id>/')
api.add_resource(ModifyProduct, '/api/v1/products/<int:product_id>/')
api.add_resource(PostSale, '/api/v1/sales/')
api.add_resource(GetSales, '/api/v1/sales/')
api.add_resource(GetMySales, '/api/v1/my/sales/')
api.add_resource(EachSale, '/api/v1/sale/<int:sale_id>/')
api.add_resource(PostCategory, '/api/v1/categories/')
api.add_resource(GetCategory, '/api/v1/categories/')
api.add_resource(ModifyCategory, '/api/v1/categories/<int:category_id>/')
api.add_resource(DeleteCategory, '/api/v1/categories/<int:category_id>/')
api.add_resource(MakeAdmin, '/api/v1/make/admin/<int:attendant_id>/')
api.add_resource(AddCategory, '/api/v1/products/add/category/<int:product_id>/')

