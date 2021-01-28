#!/usr/bin/env python

from datetime import datetime
from pathlib import Path

import typer
import yaml
from loguru import logger

import config
from db_utils import DBHandler
from tweepy_helpers import TwiffleHandler

logger.add(
    config.LOGFILE_NAME,
    rotation=config.LOGFILE_ROTATION,
    retention=config.LOGFILE_RETENTION,
)

app = typer.Typer()


@app.command()
def track(
    settings: Path = typer.Argument(config.SETTINGS_FILE, help='Path to the settings file')
):
    settings = yaml.load(settings.read_text(), Loader=yaml.FullLoader)
    database = Path(settings['database'])
    keywords = settings['track']['keywords']
    db_handler = DBHandler(database)
    twiffle_handler = TwiffleHandler(db_handler)
    twiffle_handler.run_stream(*keywords)


@app.command()
def dump_users(
    settings: Path = typer.Argument(config.SETTINGS_FILE, help='Path to the settings file')
):
    logger.disable('db_utils')

    settings = yaml.load(settings.read_text(), Loader=yaml.FullLoader)
    database = Path(settings['database'])
    s = settings.get('dump_users', {})
    excluded_users = [u.removeprefix('@') for u in s.get('excluded_users', [])]
    since = s.get('since', datetime.min.isoformat(' ', 'seconds'))
    until = s.get('until', datetime.now().isoformat(' ', 'seconds'))
    include_retweets = s.get('retweets', True)
    output = s.get('output')
    must_include = s.get('must_include', [])

    db_handler = DBHandler(database)
    users = db_handler.extract_users(
        since=since,
        until=until,
        include_retweets=include_retweets,
        excluded_users=excluded_users,
        must_include=must_include,
    )
    users = '\n'.join([f'@{u}' for u in users])
    if output is not None:
        Path(output).write_text(users)
    else:
        print(users)


if __name__ == "__main__":
    app()
