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
db_handler = DBHandler()


@app.command()
def track(tracking_keywords: List[str]):
    twiffle_handler = TwiffleHandler(db_handler)
    twiffle_handler.run_stream(*tracking_keywords)


@app.command()
def dump_users(since: str = None, until: str = None):
    users = db_handler.extract_users(since=since, until=until)
    print('\n'.join(users))


if __name__ == "__main__":
    app()
