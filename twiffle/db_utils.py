import sqlite3

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

    def extract_users(
        self,
        since: str,
        until: str,
        include_retweets=True,
        excluded_users=[],
        must_include=[],
    ):
        """Extract unique usernames with tweets created after "since" and before "until"
        Parameters
        ----------
            since: str with isoformat "YYYY-MM-DD HH:MM:SS"
            until: str with isoformat "YYYY-MM-DD HH:MM:SS"
        """
        logger.info(f'Extracting unique usernames from {since} to {until}')
        query = '''SELECT *
                   FROM status
                   WHERE created_at >= ? and created_at <= ?'''
        if not include_retweets:
            query += ' and is_retweet=0'
        self.cursor.execute(query, (since, until))
        rows = self.cursor.fetchall()
        return sorted(
            {
                row['username']
                for row in rows
                if row['username'] not in excluded_users
                and self._tweet_contains_terms(row['text'], must_include)
            },
            key=str.casefold,
        )

    @staticmethod
    def _tweet_contains_terms(tweet_text: str, terms: list):
        tweet_tokens = set(tweet_text.lower().split())
        terms = set([t.lower() for t in terms])
        return terms <= tweet_tokens
