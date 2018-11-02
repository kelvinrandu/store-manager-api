[![Build Status](https://travis-ci.org/kelvinrandu/store-manager-api.svg?branch=Challenge3)](https://travis-ci.org/kelvinrandu/store-manager-api)

[![Coverage Status](https://coveralls.io/repos/github/kelvinrandu/store-manager-api/badge.svg?branch=ch-add-coveralls-badge-161360364)](https://coveralls.io/github/kelvinrandu/store-manager-api?branch=ch-add-coveralls-badge-161360364)

# STORE-MANAGER-API
A restful  flask app intended to communicate using api endpoints

## DESCRIPTION
Store-manager is an api that helps store owners manage sales and product inventory records.
The store attendants have the priviledge to do the following:
- Create an  account
- Login in into their account
- Add product
- View all products
- View each product
- Add sale record
- View  sale records
- View each sale records

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
| POST   | https://my-store-manager2.herokuapp.com/api/v1/register/          |  register user   |
| POST   | https://my-store-manager2.herokuapp.com/api/v1/products/        |  create product   
| PUT  | https://my-store-manager2.herokuapp.com/api/v1/products/ <int: product_id>       |  modify product     | 

| POST   | https://my-store-manager2.herokuapp.com/api/v1/sales/           |  create sale         | 
| GET     | https://my-store-manager2.herokuapp.com/api/v1/products/       |  Fetch all product   |       
| GET     | https://my-store-manager2.herokuapp.com/api/v1/sales/          |  Fetch all sales     |      
| GET     | https://my-store-manager2.herokuapp.com/api/v1/product/<int: product_id>/ |  Fetches a single product   |
| GET     | https://my-store-manager2.herokuapp.com/api/v1/sale/<int: sale_id>/  |  Fetches a single sale   |


## TESTING THE APP
 The endpoints above can be tested  using [postman](https://www.getpostman.com/)

## RUN TEST
To run unitests type the code below in your terminal in your root folder
``` $ pytest ```