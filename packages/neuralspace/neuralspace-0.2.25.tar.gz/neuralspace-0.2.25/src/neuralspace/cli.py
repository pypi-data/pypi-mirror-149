import asyncio
from typing import Text

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from neuralspace import VERSION
from neuralspace.apis import get_async_http_session
from neuralspace.augmentation.commands import augmentation
from neuralspace.language_detection.commands import language_detection
from neuralspace.ner.commands import ner
from neuralspace.nlu.commands import nlu
from neuralspace.translation.commands import translation
from neuralspace.transliteration.commands import transliteration
from neuralspace.utils import (
    add_apps_to_table,
    add_heading_to_description_table,
    app_install,
    do_login,
    print_logo,
    print_logo_and_description,
    setup_logger,
)

console = Console()


def close_connection():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_async_http_session().close())


# atexit.register(close_connection)


class RichGroup(click.Group):
    def format_help(self, ctx, formatter):
        print_logo_and_description()


@click.group(cls=RichGroup)
@click.version_option(VERSION)
def entrypoint():
    pass


@entrypoint.command(name="list-apps")
def list_apps():
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table = add_heading_to_description_table(table)
    table = add_apps_to_table(table)
    console.print(table)


@entrypoint.command(name="install-app")
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    required=True,
    help="Code of the app you want to install. To get App codes try: neuralspace list-apps",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def install_app(name: Text, log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(app_install(name))
    loop.run_until_complete(get_async_http_session().close())


@entrypoint.command(name="login", short_help="To login to the neuralSpace platform")
@click.option(
    "-e",
    "--email",
    type=click.STRING,
    required=False,
    help="Your NeuralSpace email id",
)
@click.option(
    "-p",
    "--password",
    type=click.STRING,
    required=False,
    help="Your NeuralSpace account password",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def login(email: Text, password: Text, log_level: Text):
    if not email:
        email = Prompt.ask("Enter your email")
    if not password:
        password = Prompt.ask("Enter your password", password=True)
    setup_logger(log_level=log_level)
    print_logo()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(do_login(email, password))
    loop.run_until_complete(get_async_http_session().close())


entrypoint.add_command(nlu)
entrypoint.add_command(ner)
entrypoint.add_command(translation)
entrypoint.add_command(transliteration)
entrypoint.add_command(augmentation)
entrypoint.add_command(language_detection)

if __name__ == "__main__":
    entrypoint()
