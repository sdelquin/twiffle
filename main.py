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

app = typer.Typer()


@app.command()
def track(
    settings_path: str = typer.Option(
        config.SETTINGS_PATH, '--settings', '-s', help='Path to the settings file'
    )
):
    settings = yaml.load(Path(settings_path).read_text(), Loader=yaml.FullLoader)
    services.track(settings)


@app.command()
def dump_users(
    settings_path: str = typer.Option(
        config.SETTINGS_PATH, '--settings', '-s', help='Path to the settings file'
    ),
    dump_block: str = typer.Argument('all', help='Block to be dumped'),
):
    settings = yaml.load(Path(settings_path).read_text(), Loader=yaml.FullLoader)
    services.dump_users(settings, dump_block)


if __name__ == "__main__":
    app()
