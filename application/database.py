import os
from psycopg2 import connect, extras

environment = os.environ['APP_SETTINGS']
if environment == 'testing':
    conn = connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    
if environment == 'development':
    conn = connect(os.getenv('DATABASE_URL'))
    conn.autocommit = False
    cur = conn.cursor()
    


if environment == 'production':
    conn = connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()


def create_tables():
        
    try:
        cur.execute("DROP TABLE IF EXISTS products,sales,categories,users;")
        cur.execute("DROP TABLE IF EXISTS tokens;")
        users = """
                CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY,
                username varchar,
                role int,
                email varchar,
                password varchar,
                created_at timestamp default now());
                """

        categories = """
                CREATE TABLE IF NOT EXISTS categories(id serial PRIMARY KEY,
                name varchar,
                created_by int,
                created_at timestamp default now());
                """
        products = """
                CREATE TABLE IF NOT EXISTS products(id serial PRIMARY KEY,
                name varchar,
                price int,
                quantity int, 
                min_stock int,               
                category_id int,                              
                created_by int,
                created_at timestamp default now());
                """

        sales = """
                CREATE TABLE IF NOT EXISTS sales(id serial PRIMARY KEY,
                product_id int,
                quantity int,
                total int,
                created_by int,
                created_at timestamp default now());
                """

        create_admin = """ 
                    INSERT INTO users(username, email, password,role)VALUES('admin','admin@gmail.com', '$pbkdf2-sha256$29000$tBZizDmHkLIWAsA4J4Rwrg$2K6y68IgBSKwnpAplRupNrKZJF9ZhV6w2Jj5eRRTqMw',1);
                    """

        tokens = """
                 CREATE TABLE IF NOT EXISTS tokens(id VARCHAR(256) PRIMARY KEY,
                 expired_tokens VARCHAR(256));
                 """

        cur.execute(users)   
        cur.execute(create_admin)
        cur.execute(categories)
        cur.execute(products)
        cur.execute(sales)
        cur.execute(tokens)
        conn.commit()
        # conn.close()
        
        
    except Exception as ex:
        print('error in migration', ex)


def delete_tables():

    cur.execute("DELETE from users;")
    cur.execute("DELETE from categories;")
    cur.execute("DELETE from products;")
    cur.execute("DELETE from sales;")
    cur.execute("DELETE from tokens;")
    
        