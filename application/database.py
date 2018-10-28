from psycopg2 import connect, extras
import os

class DatabaseConnect():
    """Initializes connection to the database"""
    def __init__(self):
        self.conn = connect(os.getenv('DATABASE_URL'))
        self.cursor2 = self.conn.cursor
        self.cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        self.conn.autocommit = True

    def CloseConnection(self):
        
        self.conn.close()
 

class TestDatabaseConnect():
    """Initializes connection to the database"""
    def __init__(self):
        self.conn = connect(os.getenv('DATABASE_TEST_URL'))
        self.cursor2 = self.conn.cursor
        self.cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        self.conn.autocommit = True

    def CloseConnection(self):
        
        self.conn.close()

    def create_tables(self):
        
        try:
         # delete tables if they exist
            self.cursor.execute("DROP TABLE IF EXISTS products,sales,categories,users;")
            self.cursor.execute("DROP TABLE IF EXISTS tokens;")

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

            self.cursor.execute(users)
            self.cursor.execute(create_admin)
            self.cursor.execute(categories)
            self.cursor.execute(products)
            self.cursor.execute(sales)
            self.cursor.execute(tokens)

         
        except Exception as ex:
            print('error in migration', ex)


    def delete_tables(self):

        self.cursor.execute("DELETE from users;")
        self.cursor.execute("DELETE from categories;")
        self.cursor.execute("DELETE from products;")
        self.cursor.execute("DELETE from sales;")
        self.cursor.execute("DELETE from tokens;")
        