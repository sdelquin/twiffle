from datetime import datetime
from pathlib import Path
from typing import List

import typer
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
def track(tracking_keywords: List[str], database: Path = config.DATABASE_NAME):
    db_handler = DBHandler(database)
    twiffle_handler = TwiffleHandler(db_handler)
    twiffle_handler.run_stream(*tracking_keywords)


@app.command()
def dump_users(
    output_filename: Path = typer.Option(None, '--output', '-o'),
    since: str = datetime.min.isoformat(' ', 'seconds'),
    until: str = datetime.now().isoformat(' ', 'seconds'),
    retweets: bool = typer.Option(True, help='Include retweets.'),
    database: Path = config.DATABASE_NAME,
    excluded_users: Path = typer.Option(None, help='File with usernames on each line.'),
):
    logger.disable('db_utils')
    db_handler = DBHandler(database)
    if excluded_users:
        excluded_users = excluded_users.read_text().strip().split('\n')
    else:
        excluded_users = []
    users = db_handler.extract_users(
        since=since, until=until, include_retweets=retweets, excluded_users=excluded_users
    )
    users = '\n'.join([f'@{u}' for u in users])
    if output_filename is not None:
        output_filename.write_text(users)
    else:
        print(users)


if __name__ == "__main__":
    app()
