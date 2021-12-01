#!/usr/bin/env python

from pathlib import Path

import typer
import yaml
from loguru import logger

from twiffle import config, services

logger.add(
    config.LOGFILE_PATH,
    rotation=config.LOGFILE_ROTATION,
    retention=config.LOGFILE_RETENTION,
)

app = typer.Typer(add_completion=False)

settings_path_option = typer.Option(
    config.SETTINGS_PATH, '--settings', '-c', help='Path to the settings file'
)


@app.command()
def track(settings_path: str = settings_path_option):
    '''Track the given twitter terms.'''
    settings = yaml.load(Path(settings_path).read_text(), Loader=yaml.FullLoader)
    services.track(settings)


@app.command()
def dump_users(
    dump_block: str = typer.Argument('all', help='Block to be dumped'),
    settings_path: str = settings_path_option,
    dump_to_file: bool = typer.Option(False, '--file', '-f', help='Dump users to file'),
):
    '''Dump users who matches tracking rules.'''
    settings = yaml.load(Path(settings_path).read_text(), Loader=yaml.FullLoader)
    services.dump_users(settings, dump_block, dump_to_file)


@app.command()
def dump_db(
    settings_path: str = settings_path_option,
    slice: int = typer.Option(
        0,
        '--slice',
        '-s',
        help='''Slice results.
Positive values slice from the beginning.
Negative values slice from the end''',
    ),
):
    '''Dump database contents to stdout.'''
    settings = yaml.load(Path(settings_path).read_text(), Loader=yaml.FullLoader)
    services.dump_db(settings, slice)


if __name__ == "__main__":
    app()
