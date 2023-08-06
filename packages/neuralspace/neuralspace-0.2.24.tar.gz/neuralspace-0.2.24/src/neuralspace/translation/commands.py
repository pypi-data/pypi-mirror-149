import asyncio
from typing import Text

import click

from neuralspace.apis import get_async_http_session
from neuralspace.translation.apis import get_languages, get_translation_response
from neuralspace.translation.constants import SUPPORTED_LANGUAGES
from neuralspace.utils import setup_logger


@click.group(name="translation")
def translation():
    pass


@translation.command(
    name="parse",
)
@click.option(
    "-t",
    "--text",
    type=click.STRING,
    required=True,
    help="text to be translated",
)
@click.option(
    "-src",
    "--src-language",
    type=click.STRING,
    required=True,
    help="language that the text is in",
)
@click.option(
    "-tgt",
    "--tgt-language",
    type=click.STRING,
    required=True,
    help="language you wish to translate to",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def translate(text: Text, src_language: Text, tgt_language: Text, log_level: Text):
    setup_logger(log_level=log_level)
    if not src_language:
        ValueError(
            f"Source Language is mandatory. You can select from {SUPPORTED_LANGUAGES}"
        )
    if not tgt_language:
        ValueError(
            f"Target Language is mandatory. You can select from {SUPPORTED_LANGUAGES}"
        )
    if not text:
        ValueError("Please enter the text to translate")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_translation_response(text, src_language, tgt_language))
    loop.run_until_complete(get_async_http_session().close())


@translation.command(name="get-languages")
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def translation_get_languages(log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_languages())
    loop.run_until_complete(get_async_http_session().close())
