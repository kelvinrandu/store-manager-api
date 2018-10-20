[![Build Status](https://travis-ci.org/kelvinrandu/store-manager-api.svg?branch=develop)](https://travis-ci.org/kelvinrandu/store-manager-api)

[![Coverage Status](https://coveralls.io/repos/github/kelvinrandu/store-manager-api/badge.svg?branch=develop)](https://coveralls.io/github/kelvinrandu/store-manager-api?branch=develop)

# store-manager-api
A restful  flask app intended to communicate using api endpoints
## DESCRIPTION
Store-manager is an api that helps store owners manage sales and product inventory records.
The store attendants have the priviledge to do the following:
- Login in into their account
- Add product
- View all products
- View each product
- Add sale record
- View  sale records
- View each sale records



## LINK TO PIVOTAL TRACKER STORIES
- https://www.pivotaltracker.com/n/projects/2202884

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
| POST   | http://127.0.0.1:5000/api/v1/login       |  login user      | 
| POST   | http://127.0.0.1:5000/api/v1/register          |  register user         |
| POST   | http://127.0.0.1:5000/api/v1/products        |  create product      | 
| POST   | http://127.0.0.1:5000/api/v1/sales           |  create sale         | 
| GET     | http://127.0.0.1:5000/api/v1/products       |  Fetch all product   |       
| GET     | http://127.0.0.1:5000/api/v1/sales          |  Fetch all sales     |      
| GET     | http://127.0.0.1:5000/api/v1/product/<int: product_id>  |  Fetches a single product   |
| GET     | http://127.0.0.1:5000/api/v1/sale/<int: sale_id>  |  Fetches a single sale   |


## TESTING THE APP
 The endpoints above can be tested  using [postman](https://www.getpostman.com/)

## RUN TEST
To run unitests type the code below in your terminal in your root folder
``` $ pytest ```