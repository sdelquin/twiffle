import sqlite3


class DBHandler:
    def __init__(self, database_filename='twiffle.db'):
        self.conn = sqlite3.connect(database_filename)
        self.cursor = self.conn.cursor()

    def init(self):
        query = '''CREATE TABLE status (
                id TEXT PRIMARY KEY,
                username TEXT,
                text TEXT,
                created_at TIMESTAMP,
                url TEXT,
                is_retweet INTEGER);'''
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError:
            print('Database already exists!')

    def insert(self, id, username, text, created_at, url, is_retweet, /):
        query = 'INSERT INTO status VALUES (?, ?, ?, ?, ?, ?)'
        self.cursor.execute(query, (id, username, text, created_at, url, is_retweet))
        self.conn.commit()
