import json
import logging
import os
from copy import copy
from pathlib import Path
from typing import Any, Dict, List, Text

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from neuralspace.apis import get_async_http_session
from neuralspace.constants import (
    APP_IS_INSTALLED,
    AUTHORIZATION,
    BOLD_END,
    BOLD_START,
    BOOK,
    COMMON_HEADERS,
    CONFIDENCE,
    COUNT,
    CROSS,
    DARK_ORANGE_END,
    DARK_ORANGE_START,
    DATA,
    DESCRIPTION,
    DOOR,
    END_INDEX,
    ENTITIES,
    ENTITY,
    ENTITY_TYPE,
    FAST_FORWARD,
    FILTER,
    FROM,
    GREEN_TICK,
    INFO,
    INSTALL_APP_COMMAND,
    INSTALL_APP_URL,
    KEY,
    LANGUAGE,
    LIST_ENTITY_URL,
    LOGIN_URL,
    LOGO_HASH,
    ORANGE3_END,
    ORANGE3_START,
    PAGE_NUMBER,
    PAGE_SIZE,
    SEARCH,
    START_INDEX,
    TIME,
    TO,
    TYPE,
    VALUE,
    auth_path,
    neuralspace_url,
)

logger = logging.getLogger("rich")
console = Console()


def setup_logger(log_level: Text):
    global logger
    logging.basicConfig(level=log_level, handlers=[RichHandler(level=logging.INFO)])
    if log_level == "INFO":
        logger.level = logging.INFO
        logging.getLogger("asyncio").setLevel(logging.INFO)
    elif log_level == "DEBUG":
        logger.level = logging.DEBUG
        logging.getLogger("asyncio").setLevel(logging.DEBUG)
    elif log_level == "ERROR":
        logger.level = logging.ERROR
        logging.getLogger("asyncio").setLevel(logging.ERROR)


def get_logo():
    logo_path = (Path(os.path.realpath(__file__))).parent / "data" / "logo.txt"
    return f"{logo_path.read_text()}"


def print_logo():
    logo_path = (Path(os.path.realpath(__file__))).parent / "data" / "logo.txt"
    console.print(
        f"\n{BOLD_START}{logo_path.read_text()}{BOLD_END}", style=f"{LOGO_HASH}"
    )


def register_auth_token(login_response: Dict[Text, Text]):
    if "data" in login_response and "auth" in login_response["data"]:
        with open(str(auth_path()), "w") as f:
            json.dump(login_response, f)
    else:
        raise ValueError(f"Login response is malformed: {login_response}")


def get_auth_token() -> Text:
    if auth_path().exists():
        credentials = json.loads(auth_path().read_text())
        return credentials["data"]["auth"]
    else:
        raise FileNotFoundError(
            "Credentials file not found. Consider logging in using."
            " Seems like you have not logged in. "
            "`neuralspace login --email <your-neuralspace-email-id> "
            "--password <your-password>`"
        )


def is_success_status(status_code: int) -> bool:
    success = False
    if 200 <= status_code < 300:
        success = True
    return success


async def do_login(email: Text, password: Text):
    user_data = {"email": email, "password": password}
    logger.debug(f"Login{DOOR} attempt for: {user_data}")
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LOGIN_URL}",
        data=json.dumps(user_data),
        headers=COMMON_HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            register_auth_token(json_response)
            console.print(f"> {INFO} {GREEN_TICK}  Login successful!")
            console.print(f"> {INFO} {KEY} Credentials registered at {auth_path()}")
            console.print(
                f"{FAST_FORWARD}  Install an app: [dark_orange3]{INSTALL_APP_COMMAND}[/dark_orange3]"
            )
        else:
            console.print(
                f"> [red]ERROR[/red] {CROSS} Login failed! Please check your username and password"
            )


async def app_install(name: Text):
    user_data = {"appType": name}
    logger.debug(f"Installing app: {name}")
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{INSTALL_APP_URL}",
        data=json.dumps(user_data),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Install Successful!")
            console.print(
                f"{FAST_FORWARD} To use the {name} app: {DARK_ORANGE_START}neuralspace {name}{DARK_ORANGE_END} --help"
            )
        else:
            if json_response["message"] == APP_IS_INSTALLED:
                console.print(f"> {INFO} {GREEN_TICK}  {APP_IS_INSTALLED}")
                console.print(
                    f"{FAST_FORWARD} To use the {name} app: {DARK_ORANGE_START}"
                    f"neuralspace {name}{DARK_ORANGE_END} --help"
                )

            else:
                console.print(f"> [red]ERROR[/red] {CROSS} Install Failed!")
                console.print(
                    f"\n{json.dumps(json_response, indent=4, ensure_ascii=False)}"
                )


def get_list_chunks(items: List[Any], chunk_size: int):
    for chunk in range(0, len(items), chunk_size):
        yield items[chunk : chunk + chunk_size]  # noqa : E203


def add_apps_to_table(table: Table) -> Table:
    table.add_row(
        f"{BOLD_START}NeuraLingo{BOLD_END}",
        f"{BOLD_START}nlu{BOLD_END}",
        "neuralspace [bold red]nlu[/bold red]",
        "Whether you are using chatbots, voicebots, or process automation engines, they are all powered by Natural "
        "Language Understanding (NLU). It's main purpose is to "
        "understand the intent of the user, and extract relevant "
        "information (entities) from what they said (speech) or wrote (text) to perform a relevant action. "
        "Entities can be anything from names, addresses, account numbers to very domain specific terms like names of "
        "chemicals, medicines, etc. Sometimes it also predicts the sentiment of the user which helps the bot respond "
        "to the user in a more empathetic tone.",
    )
    table.add_row(
        f"{BOLD_START}Entity Recognition{BOLD_END}",
        f"{BOLD_START}ner{BOLD_END}",
        "neuralspace [bold red]ner[/bold red]",
        "Entities play a major role in language understanding. To perform an action on a certain user query you not "
        "only need to understand the intent behind it but also the entities present in it. "
        "E.g., if someone says 'flights from Berlin to London', the intent here is flight-search and entities are "
        "Berlin and London, which are of type city. In a given piece of text, entities can be anything from names, "
        "addresses, account numbers to very domain specific terms like names of chemicals, medicines, etc. "
        "Essentially any valuable information that can be extracted from text.",
    )
    table.add_row(
        f"{BOLD_START}Machine Translation{BOLD_END}",
        f"{BOLD_START}translation{BOLD_END}",
        "neuralspace [bold red]translation[/bold red]",
        "Whether we are talking about subtitles, government documents or question papers for exams, all of them "
        "need to be translated into multiple languages. Manually translating documents at such a scale is not "
        "only expensive but also an extremely time consuming process. With the help of Neural Machine "
        "Translation (NMT) you can drastically reduce the amount of time it takes for manual translation "
        "of documents. Our translation models are all state-of-the-art Artificial Neural Networks which can "
        "translate text in over 100 languages. ",
    )
    table.add_row(
        f"{BOLD_START}Transliteration{BOLD_END}",
        f"{BOLD_START}transliteration{BOLD_END}",
        "neuralspace [bold red]transliteration[/bold red]",
        "For languages that don't use the latin script, e.g., Arabic, Hindi, Punjabi, Sinhala and many "
        "other spoken around the world, typing can be challenging as keyboards/keypads mostly default to "
        "latin characters. That makes creating content in vernacular languages difficult. With "
        "transliteration you can create content in these languages using your latin keypad. "
        "For instance, you type a word on the latin keypad the way you would pronounce it in Punjabi, "
        "and using transliteration you can convert that into Punjabi. It transforms a word from one "
        "alphabet to the other phonetically. ",
    )
    table.add_row(
        f"{BOLD_START}NeuralAug{BOLD_END}",
        f"{BOLD_START}augmentation{BOLD_END}",
        "neuralspace [bold red]augmentation[/bold red]",
        "Any language processing task requires data, and we all wish we could generate data "
        "magically. That was exactly the idea behind building NeuralAug. Given a sentence NeuralAug "
        "can generate up to ten sentences keeping the intent of the original sentence intact. It "
        "can help in creating datasets faster and make language processing models more robust. ",
    )
    table.add_row(
        f"{BOLD_START}Language Detection{BOLD_END}",
        f"{BOLD_START}language-detection{BOLD_END}",
        "neuralspace [bold red]language-detection[/bold red]",
        "Dealing with different languages poses a fundamental problem of first detecting what language "
        "you are looking at. Language-detection service will help you to detect the language based on "
        "your input text with given confidence score. Use it with other APIs like transliteration "
        "or translation and make your NLP application cater to any language you want.",
    )
    return table


def add_heading_to_description_table(table: Table) -> Table:
    table.add_column("App Name", style="#c47900")
    table.add_column("App Code", style="#c47900")
    table.add_column("Command", style="#c47900")
    table.add_column("Description")
    return table


def print_logo_and_description():
    console.print(f"[bold]{get_logo()}[/bold]", style="#c47900")
    console.print(
        "[bold magenta]Website: [/bold magenta][link]https://neuralspace.ai[/link]"
    )
    console.print(
        "[bold magenta]Docs: [/bold magenta][link]https://docs.neuralspace.ai[/link]"
    )
    console.print(
        "[bold magenta]Platform Login: [/bold magenta][link]https://platform.neuralspace.ai[/link]"
    )
    console.print("[bold magenta]Commands: [/bold magenta]")
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table = add_heading_to_description_table(table)
    table.add_row(
        "[bold]Login[/bold]",
        "neuralspace [bold red]login[/bold red]",
        "Login to the our platform and save credentials locally",
    )
    table.add_row(
        "[bold]List Apps[/bold]",
        "neuralspace [bold red]list-apps[/bold red]",
        "List all the available apps in our platform and their respective codes",
    )
    table.add_row(
        "[bold]Install App[/bold]",
        "neuralspace [bold red]install-app[/bold red]",
        "Installs the specific app on your account",
    )
    table = add_apps_to_table(table)
    console.print(table)


def print_ner_response(list_of_entities: List[Dict[Text, Text]], original_text: Text):
    if not list_of_entities:
        console.print(
            f"There is no entities in your text: [bold red]{original_text}[/bold red]"
        )
    else:
        table = Table(show_header=True, header_style="orange3")
        table.add_column("idx", style="sandy_brown")
        table.add_column("Type", style="green")
        table.add_column("Value", style="green")
        table.add_column("Entities marked in original text")
        for i, entities in enumerate(list_of_entities):
            start_index = entities[START_INDEX]
            end_index = entities[END_INDEX]
            marked_sentence = ""
            for idx, character in enumerate(original_text):
                if idx == start_index:
                    marked_sentence += "[bold green]"
                elif idx == end_index:
                    marked_sentence += "[/bold green]"
                marked_sentence += character
            if entities[TYPE] == TIME and isinstance(entities[VALUE], dict):
                type_time_format = (
                    f"From: {str(entities[VALUE][FROM])} To: {str(entities[VALUE][TO])}"
                )
                table.add_row(str(i), entities[TYPE], type_time_format, marked_sentence)
            else:
                table.add_row(str(i), entities[TYPE], entities[VALUE], marked_sentence)
        console.print(table)


def print_translation_response(
    text: Text, src_language: Text, tgt_language: Text, translated_text: Text
):
    table = Table(show_header=True, header_style="orange3")
    table.add_column("Text", style="sandy_brown")
    table.add_column("Src Language", style="green")
    table.add_column("Tgt Language", style="green")
    table.add_column("Translated Text", style="green")

    table.add_row(text, src_language, tgt_language, translated_text)
    console.print(table)


def print_transliteration_response(
    text: Text, src_language: Text, tgt_language: Text, suggestions: Text
):
    table = Table(show_header=True, header_style="orange3")
    table.add_column("Text", style="sandy_brown")
    table.add_column("Src Language", style="green")
    table.add_column("Tgt Language", style="green")
    table.add_column("Transliterated Suggestions", style="green")

    original_text_shown = False

    for suggestion in suggestions:
        if original_text_shown is False:
            table.add_row(text, src_language, tgt_language, suggestion)
            original_text_shown = True
        else:
            table.add_row("", "", "", suggestion)
    console.print(table)


def print_language_detection_response(text: Text, detected_languages: List[Dict]):
    table = Table(show_header=True, header_style="orange3")
    table.add_column("Text", style="sandy_brown")
    table.add_column("Detected Language", style="green")
    table.add_column("Confidence Score", style="green")
    original_text_shown = False

    for language in detected_languages:
        if original_text_shown is False:
            table.add_row(
                text, language[LANGUAGE], str(round(float(language[CONFIDENCE]), 2))
            )
            original_text_shown = True
        else:
            table.add_row(
                "", language[LANGUAGE], str(round(float(language[CONFIDENCE]), 2))
            )
    console.print(table)


def print_augmentation_response(text: Text, augmentation_suggestions: List):
    table = Table(show_header=True, header_style="orange3")
    table.add_column("Text", style="sandy_brown")
    table.add_column("Suggestions", style="green")
    original_text_shown = False

    for augmentation in augmentation_suggestions:
        if original_text_shown is False:
            table.add_row(text, augmentation)
            original_text_shown = True
        else:
            table.add_row("", augmentation)
    console.print(table)


def print_get_entity(response_to_print):
    table = Table(show_header=True, header_style="orange3")
    table.add_column("idx", style="sandy_brown")
    table.add_column("Entity Name", style="green")
    table.add_column("Description", style="green")
    for index, entity in enumerate(response_to_print[DATA][ENTITIES]):
        table.add_row(str(index), entity[ENTITY], entity[DESCRIPTION])
    console.print(table)


async def get_entity_list(
    language: Text, search: Text, page_number: int, page_size: int, entity_type: Text
):
    payload = {
        FILTER: {ENTITY_TYPE: entity_type, LANGUAGE: language},
        SEARCH: search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_ENTITY_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(
                f"> {INFO} {BOOK} Entities available for Page "
                f"{ORANGE3_START}{page_number}{ORANGE3_END} of {json_response[DATA][COUNT]} "
                f"with Page Size: {ORANGE3_START}{page_size}{ORANGE3_END}"
            )
            print_get_entity(json_response)
        else:
            console.print("Please check your parameter and give the right parameter")
