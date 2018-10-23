from psycopg2 import connect, extras
import os

class DatabaseConnect():
    """Initializes connection to the database"""
    def __init__(self):
        # self.conn = connect(os.getenv('DATABASE_URL'))
        self.conn = connect("dbname=me user=postgres password=1234 host=localhost")
        self.cursor2 = self.conn.cursor
        self.cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        self.conn.autocommit = True

    def CloseConnection(self):
        
        self.conn.close()

def create_tables():
    cur = conn.cursor()
    try:
        # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS  users;")
        cur.execute("DROP TABLE IF EXISTS tokens;")

        # create table users
        users = "CREATE TABLE users(id VARCHAR(256) PRIMARY KEY, username VARCHAR(64) UNIQUE , email VARCHAR(64) UNIQUE," \
                "password VARCHAR(256),role VARCHAR(64),time_created TIMESTAMP );"


        # create table tokens
        tokens = "CREATE TABLE tokens(id VARCHAR(256) PRIMARY KEY, expired_tokens VARCHAR(256));"

        cur.execute(users)

        cur.execute(tokens)

        conn.commit()
    except Exception as ex:
        print('error in migration', ex)


def delete_tables():
    cur = conn.cursor()
    cur.execute("DELETE from users;")
    cur.execute("DELETE from tokens;")
    conn.commit()