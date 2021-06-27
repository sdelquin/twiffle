#!/usr/bin/env python

from pathlib import Path

import typer
import yaml
from loguru import logger

from twiffle import config, services

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
    services.track(settings)


@app.command()
def dump_users(
    settings: Path = typer.Argument(config.SETTINGS_FILE, help='Path to the settings file')
):
    settings = yaml.load(settings.read_text(), Loader=yaml.FullLoader)
    services.dump_users(settings)


if __name__ == "__main__":
    app()
