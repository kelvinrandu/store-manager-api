import os
from psycopg2 import connect, extras

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



def create_tables():
        
    try:
     # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS products,sales,categories,users;")
        cur.execute("DROP TABLE IF EXISTS tokens;")

        users = "CREATE TABLE users(id INT PRIMARY KEY, username VARCHAR(64) UNIQUE , email VARCHAR(64) UNIQUE," \
                    "password VARCHAR(256),role   INT  default 0,created_by INT default 0,time_created TIMESTAMP );"
        create_admin ="INSERT INTO users(id,username, email, password,role)VALUES(1,'admin','admin@gmail.com', '$pbkdf2-sha256$29000$tBZizDmHkLIWAsA4J4Rwrg$2K6y68IgBSKwnpAplRupNrKZJF9ZhV6w2Jj5eRRTqMw','1');" 
        products = "CREATE TABLE products(id VARCHAR(256) PRIMARY KEY, title VARCHAR(256), body TEXT," \
                    "user_id VARCHAR(256), time_created TIMESTAMP, preferred_answer VARCHAR(256));"

        sales = "CREATE TABLE sales(id VARCHAR(256) PRIMARY KEY, body TEXT," \
                    "user_id VARCHAR(256), question_id VARCHAR(256), preferred BOOLEAN DEFAULT FALSE, time_created TIMESTAMP);"

        categories = "CREATE TABLE categories(id VARCHAR(256) PRIMARY KEY, body TEXT," \
                    "user_id VARCHAR(256), question_id VARCHAR(256), preferred BOOLEAN DEFAULT FALSE, time_created TIMESTAMP);"

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
    
        