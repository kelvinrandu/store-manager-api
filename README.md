[![Build Status](https://travis-ci.org/kelvinrandu/store-manager-api.svg?branch=Challenge3)](https://travis-ci.org/kelvinrandu/store-manager-api)

[![Coverage Status](https://coveralls.io/repos/github/kelvinrandu/store-manager-api/badge.svg?branch=ch-add-coveralls-badge-161360364)](https://coveralls.io/github/kelvinrandu/store-manager-api?branch=ch-add-coveralls-badge-161360364)

# STORE-MANAGER-API
A restful  flask app intended to communicate using api endpoints

## DESCRIPTION
Store-manager is an api that helps store owners manage sales and product inventory records.
The store attendants have the priviledge to do the following:
- Login in into their account
- View all products
- Add sale record
- View my sale records

The admin has the priviledge to do the following:
- Login in into their account
- Create a new store attendant
- View all products
- Create a new product
- View all products
- View each product
- Edit product
- Delete product
- View all sales records
- View each sales records
- Create a new category 
- Edit  category
- delete  category
- Make store attendant admin

## DOCUMENTATION
- https://mystoremanager2.docs.apiary.io/#

## LINK TO PIVOTAL TRACKER STORIES
- https://www.pivotaltracker.com/n/projects/2202884



## LINK TO LIVE SITE
https://my-store-manager2.herokuapp.com/


## RUNNING THE APPLICATION
- clone [this](https://github.com/kelvinrandu/store-manager-api.git) repository
- navigate to the project directory
- install virtual environment
```virtualenv venv ```
- activate the virtual environment
```$ source venv/bin/activate```
- install dependencies needed for the project to run
``` $ pip install -r requirements.txt ```
- install flask
``` $ pip install flask```
- run the application
``` $ FLASK_APP=run.py flask run```

## API ROUTES

| Methods        | Url          | Description |
| ------------- |:-------------:| -----:|
| POST   | https://my-store-manager2.herokuapp.com/api/v1/login/      |  login user      | 
| POST   | https://my-store-manager2.herokuapp.com/api/v1/register/          | admin register store attendant|
| POST   | https://my-store-manager2.herokuapp.com/api/v1/products/        |  create product   |
| GET     | https://my-store-manager2.herokuapp.com/api/v1/products/       |  Fetch all product   | 
| GET     | https://my-store-manager2.herokuapp.com/api/v1/product/<int: product_id>/ |  Fetches a single product   |
| PUT  | https://my-store-manager2.herokuapp.com/api/v1/products/ <int: product_id>       |  modify product     | 
| DELETE  | https://my-store-manager2.herokuapp.com/api/v1/products/ <int: product_id>    |  delete a  product | 
| POST   | https://my-store-manager2.herokuapp.com/api/v1/sales/           |  create sale         |       
| GET     | https://my-store-manager2.herokuapp.com/api/v1/my/sales/         |  Fetch  sales my sales for store attendant     |  
| GET     | https://my-store-manager2.herokuapp.com/api/v1/sales/          |  Fetch all sales     |     
| GET     | https://my-store-manager2.herokuapp.com/api/v1/sale/<int: sale_id>/  |  Fetches a single sale   |
| POST    | https://my-store-manager2.herokuapp.com/api/v1/categories/  |  post category  |
|  GET  | https://my-store-manager2.herokuapp.com/api/v1/categories/  |  fetch all categories  |
|  PUT  | https://my-store-manager2.herokuapp.com/api/v1/categories/<int:category_id>/  |  modify a category  |
|  DELETE | https://my-store-manager2.herokuapp.com/api/v1/categories/<int:category_id>/  |  delete a category  |
|  POST | https://my-store-manager2.herokuapp.com/api/v1/make/admin/<int:attendant_id>/  |  make store attendant admin  |
|  POST | https://my-store-manager2.herokuapp.com/api/v1/products/add/category/<int:product_id>/|  add category to product|


## TESTING THE APP
 The endpoints above can be tested  using [postman](https://www.getpostman.com/)

## RUN TEST
To run unitests type the code below in your terminal in your root folder
- export yourtesting  app setting
``` export APP_SETTINGS="testing" ```
- export link to your test database
``` export DATABASE_URL="url to your test database" ```
- run your tests
 ``` $ pytest ```