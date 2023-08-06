import asyncio
from typing import Text

import click

from neuralspace.apis import get_async_http_session
from neuralspace.transliteration.apis import get_languages, get_transliteration_response
from neuralspace.utils import setup_logger


@click.group(name="transliteration")
def transliteration():
    pass


@transliteration.command(
    name="parse",
)
@click.option(
    "-t",
    "--text",
    type=click.STRING,
    required=True,
    help="text to be transliterated",
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
    help="language you wish to transliterate the text into",
)
@click.option(
    "-n",
    "--num-suggestions",
    type=click.STRING,
    required=True,
    help="number of suggestions required",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def transliterate(
    text: Text,
    src_language: Text,
    tgt_language: Text,
    num_suggestions: int,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    if not text:
        ValueError("Please enter the text to transliterate")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        get_transliteration_response(text, src_language, tgt_language, num_suggestions)
    )
    loop.run_until_complete(get_async_http_session().close())


@transliteration.command(name="get-languages")
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def transliteration_get_languages(log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_languages())
    loop.run_until_complete(get_async_http_session().close())
