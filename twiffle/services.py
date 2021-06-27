from datetime import datetime
from pathlib import Path

from loguru import logger

from twiffle import config
from twiffle.db_utils import DBHandler
from twiffle.tweepy_helpers import TwiffleHandler


def track(settings: dict):
    db_path = config.DATA_DIR / (settings['label'] + '.db')
    keywords = settings['track']['keywords']
    db_handler = DBHandler(db_path)
    twiffle_handler = TwiffleHandler(db_handler)
    twiffle_handler.run_stream(*keywords)


def dump_users(settings: dict, dump_block: str = 'all'):
    logger.disable('twiffle.db_utils')

    db_path = config.DATA_DIR / (settings['label'] + '.db')
    dump = settings.get('dump_users', {})
    dump_blocks = dump.keys() if dump_block == 'all' else [dump_block]
    for dump_name, dump_config in dump.items():
        if dump_name not in dump_blocks:
            continue
        excluded_users = [
            u.removeprefix('@') for u in dump_config.get('excluded_users', [])
        ]
        since = dump_config.get('since', datetime.min.isoformat(' ', 'seconds'))
        until = dump_config.get('until', datetime.now().isoformat(' ', 'seconds'))
        include_retweets = dump_config.get('retweets', True)
        must_include = dump_config.get('must_include', [])

        db_handler = DBHandler(db_path)
        users = db_handler.extract_users(
            since=since,
            until=until,
            include_retweets=include_retweets,
            excluded_users=excluded_users,
            must_include=must_include,
        )
        users = '\n'.join([f'@{u}' for u in users])
        dump_file = config.DATA_DIR / (dump_name + '.dump')
        Path(dump_file).write_text(users)
