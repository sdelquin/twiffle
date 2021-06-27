from datetime import datetime
from pathlib import Path

from loguru import logger

from twiffle.db_utils import DBHandler
from twiffle.tweepy_helpers import TwiffleHandler


def track(settings: dict):
    database = Path(settings['database'])
    keywords = settings['track']['keywords']
    db_handler = DBHandler(database)
    twiffle_handler = TwiffleHandler(db_handler)
    twiffle_handler.run_stream(*keywords)


def dump_users(settings: dict):
    logger.disable('twiffle.db_utils')

    database = Path(settings['database'])
    dump = settings.get('dump_users', {})
    for dump_name, dump_config in dump.items():
        print(dump_config)
        excluded_users = [
            u.removeprefix('@') for u in dump_config.get('excluded_users', [])
        ]
        since = dump_config.get('since', datetime.min.isoformat(' ', 'seconds'))
        until = dump_config.get('until', datetime.now().isoformat(' ', 'seconds'))
        include_retweets = dump_config.get('retweets', True)
        must_include = dump_config.get('must_include', [])

        db_handler = DBHandler(database)
        users = db_handler.extract_users(
            since=since,
            until=until,
            include_retweets=include_retweets,
            excluded_users=excluded_users,
            must_include=must_include,
        )
        users = '\n'.join([f'@{u}' for u in users])
        Path(dump_name + '.txt').write_text(users)
