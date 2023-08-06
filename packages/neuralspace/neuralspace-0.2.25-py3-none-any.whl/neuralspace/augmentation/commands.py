import asyncio
from typing import Text

import click

from neuralspace.apis import get_async_http_session
from neuralspace.augmentation.apis import get_augmentation_response, get_languages
from neuralspace.utils import setup_logger


@click.group(name="augmentation")
def augmentation():
    pass


@augmentation.command(
    name="parse",
)
@click.option(
    "-t",
    "--text",
    type=click.STRING,
    required=True,
    help="text to be augmented",
)
@click.option(
    "-n",
    "--num-augments",
    type=click.INT,
    required=True,
    help="Number of sentences to generate",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def augment(text: Text, num_augments: int, log_level: Text):
    setup_logger(log_level=log_level)
    if not text:
        ValueError("Please enter the text for which you wish to generate Augmentations")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        get_augmentation_response(text=text, example_count=num_augments)
    )
    loop.run_until_complete(get_async_http_session().close())


@augmentation.command(name="get-languages")
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def language_detection_get_languages(log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_languages())
    loop.run_until_complete(get_async_http_session().close())
