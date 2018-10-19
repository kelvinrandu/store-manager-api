from flask_restful import Resource,reqparse,Api
from flask import Flask,jsonify,request, make_response,Blueprint
import re
from application.v1.resources.models import Sale
from application.v1.resources.models import Product




store_manager = Blueprint('api',__name__)

app = Flask(__name__)
api = Api(store_manager)


# handles posting of product by admin
class PostProducts(Resource):

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Product name cannot be blank', type=str)
        parser.add_argument('price', required=True, help=' Product price cannot be blank',type=int)
        parser.add_argument('quantity', required=True, help='Product quantity cannot be blank', type=int)


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

        def get(self):
            products = Product.get_products()
            
            return {'message': 'products retrieved succesfully','status':'ok','products': products}, 200



# fetch a specific product
class EachProduct(Resource):

        def get(self,product_id):

            products = Product.get_each_product(product_id)

            return {'message': 'product retrieved succesfully','status':'ok','products': products}, 200



# handles posting of a sale by store attendant

class PostSale(Resource):

        # validate sale input

        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True, help='Sale description  cannot be blank', type=str)
        parser.add_argument('items', required=True, help=' items cannot be blank')


        def post(self):

            args =  PostSale.parser.parse_args()
            description = args.get('description').strip()
            items = args.get('items')
            total = 400
 
 # error response
            if not description:
                return make_response(jsonify({'message': 'Sale description  can not be empty'}),400)


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

        def get(self):
                
            result = Sale.get_sales()
            return {'message': 'sales retrieved succesfully','status':'ok','sale':result}, 200


# routes
api.add_resource(PostProducts, '/api/v1/products')
api.add_resource(GetProducts, '/api/v1/products')
api.add_resource(EachProduct, '/api/v1/product/<int:product_id>')
api.add_resource(PostSale, '/api/v1/sales')
api.add_resource(GetSales, '/api/v1/sales')
