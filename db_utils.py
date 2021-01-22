import sqlite3
from datetime import datetime

from loguru import logger


class DBHandler:
    def __init__(self, database_filename):
        logger.debug(f'Opening database connection to {database_filename}')
        is_new_db = not database_filename.exists()
        self.conn = sqlite3.connect(
            database_filename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        if is_new_db:
            self.create_table()

    def create_table(self):
        logger.debug('Creating status table')
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
            logger.debug('Table already exists! Not created')

    def insert(self, id, username, text, created_at, url, is_retweet, /):
        logger.debug('Inserting new row on database')
        query = 'INSERT INTO status VALUES (?, ?, ?, ?, ?, ?)'
        self.cursor.execute(query, (id, username, text, created_at, url, is_retweet))
        self.conn.commit()

    def extract_users(self, since: str = None, until: str = None, include_retweets=True):
        """Extract unique usernames with tweets created after "since" and before "until"
        Parameters
        ----------
            since: str with isoformat "YYYY-MM-DD HH:MM:SS"
            until: str with isoformat "YYYY-MM-DD HH:MM:SS"
        """
        since = since or datetime.min.isoformat(' ', 'seconds')
        until = until or datetime.now().isoformat(' ', 'seconds')
        logger.info(f'Extracting unique usernames from {since} to {until}')
        query = '''SELECT DISTINCT(username)
                   FROM status
                   WHERE created_at >= ? and created_at <= ? and is_retweet=?'''
        self.cursor.execute(query, (since, until, int(include_retweets)))
        rows = self.cursor.fetchall()
        return [row['username'] for row in rows]
