import sqlite3
from datetime import datetime


class DBHandler:
    def __init__(self, database_filename='twiffle.db'):
        self.conn = sqlite3.connect(
            database_filename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.conn.row_factory = sqlite3.Row
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

    def extract_users(self, since: str = None, until: str = None):
        """Extract unique usernames with tweets created after "since" and before "until"
        Parameters
        ----------
            since: str with isoformat "YYYY-MM-DD HH:MM:SS"
            until: str with isoformat "YYYY-MM-DD HH:MM:SS"
        """
        since = since or datetime.min.isoformat(' ', 'seconds')
        until = until or datetime.now().isoformat(' ', 'seconds')
        query = '''SELECT DISTINCT(username)
                   FROM status
                   WHERE created_at >= ? and created_at <= ?'''
        self.cursor.execute(query, (since, until))
        rows = self.cursor.fetchall()
        return [row['username'] for row in rows]
