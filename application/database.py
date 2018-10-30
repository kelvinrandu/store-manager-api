import os
from psycopg2 import connect, extras
# from instance.config import APP_CONFIG


environment = os.environ['APP_SETTINGS']
if environment == 'testing':
    conn = connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    print('connect to test database')
    
if environment == 'development':
    conn = connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    print('connect to develop database')

if environment == 'production':
    conn = connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    print('connect to develop database')    
# DATABASE_URL = APP_CONFIG[environment].DATABASE_URL
# conn = connect(DATABASE_URL)


# config_name = os.getenv('FLASK_ENV')
# development_url = os.getenv('Dev_URL')
# testing_url = os.getenv('Test_URL')
# production_url = os.getenv('DATABASE_URL')
# print(config_name)

    # conn = connect(os.getenv('DATABASE_URL'))
    # cur = conn.cursor()
    # print("Database is  connected.")

# if config_name == 'development':
#     conn = connect(os.getenv('DATABASE_URL'))
#     print("Database is connected as .")

# if config_name == 'production':
#     conn = connect(os.getenv('DATABASE_URL'))
#     print("Database is  connected as.")
# if config_name == 'testing':
#     conn = connect(os.getenv('DATABASE_URL'))
#     print("Database is  connected as.")






def create_tables():
        
    try:
     # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS products,sales,categories,users;")
        cur.execute("DROP TABLE IF EXISTS tokens;")

        # create table users
        users = "CREATE TABLE users(id VARCHAR(256) PRIMARY KEY, username VARCHAR(64) UNIQUE , email VARCHAR(64) UNIQUE," \
                    "password VARCHAR(256),role   INT  default 0,time_created TIMESTAMP );"
        create_admin ="INSERT INTO users(id,username, email, password,role)VALUES(1,'admin','admin@gmail.com', '$pbkdf2-sha256$29000$tBZizDmHkLIWAsA4J4Rwrg$2K6y68IgBSKwnpAplRupNrKZJF9ZhV6w2Jj5eRRTqMw','1');" 
        # create table products
        products = "CREATE TABLE products(id VARCHAR(256) PRIMARY KEY, title VARCHAR(256), body TEXT," \
                    "user_id VARCHAR(256), time_created TIMESTAMP, preferred_answer VARCHAR(256));"

        # create table sales
        sales = "CREATE TABLE sales(id VARCHAR(256) PRIMARY KEY, body TEXT," \
                    "user_id VARCHAR(256), question_id VARCHAR(256), preferred BOOLEAN DEFAULT FALSE, time_created TIMESTAMP);"

        # create table category
        categories = "CREATE TABLE categories(id VARCHAR(256) PRIMARY KEY, body TEXT," \
                    "user_id VARCHAR(256), question_id VARCHAR(256), preferred BOOLEAN DEFAULT FALSE, time_created TIMESTAMP);"

        # create table tokens
        tokens = "CREATE TABLE tokens(id VARCHAR(256) PRIMARY KEY, expired_tokens VARCHAR(256));"

        cur.execute(users)
        cur.execute(create_admin)
        cur.execute(categories)
        cur.execute(products)
        cur.execute(sales)
        cur.execute(tokens)

         
    except Exception as ex:
        print('error in migration', ex)


def delete_tables():

    cur.execute("DELETE from users;")
    cur.execute("DELETE from categories;")
    cur.execute("DELETE from products;")
    cur.execute("DELETE from sales;")
    cur.execute("DELETE from tokens;")
    
        