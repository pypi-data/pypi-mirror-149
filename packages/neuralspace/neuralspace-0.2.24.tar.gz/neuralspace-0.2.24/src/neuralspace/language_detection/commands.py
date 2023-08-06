import asyncio
from typing import Text

import click

from neuralspace.apis import get_async_http_session
from neuralspace.language_detection.apis import (
    get_language_detection_response,
    get_languages,
)
from neuralspace.utils import setup_logger


@click.group(name="language-detection")
def language_detection():
    pass


@language_detection.command(
    name="parse",
)
@click.option(
    "-t",
    "--text",
    type=click.STRING,
    required=True,
    help="text to be processed",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def detect_language(text: Text, log_level: Text):
    setup_logger(log_level=log_level)
    if not text:
        ValueError("Please enter the text for which you wish to detect language")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_language_detection_response(text))
    loop.run_until_complete(get_async_http_session().close())


@language_detection.command(name="get-languages")
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def language_detection_get_languages(log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_languages())
    loop.run_until_complete(get_async_http_session().close())
