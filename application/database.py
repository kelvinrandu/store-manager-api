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