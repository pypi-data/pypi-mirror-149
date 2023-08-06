import html
import json
import logging
from copy import copy
from typing import Any, Dict, Text

import requests
from rich.console import Console
from rich.table import Table

from neuralspace.apis import get_async_http_session
from neuralspace.constants import (
    AUTHORIZATION,
    COMMON_HEADERS,
    CROSS,
    DARK_ORANGE_END,
    DARK_ORANGE_START,
    DATA,
    DOWN_ARROW,
    ERROR,
    FAST_FORWARD,
    GREEN_TICK,
    INFO,
    RED_END,
    RED_START,
    ROCKET,
    SAD_SMILEY,
    TRANSLATED_TEXT,
)
from neuralspace.translation.constants import (
    TRANSLATE_TEXT_COMMAND,
    TRANSLATION_APP_URL,
    TRANSLATION_LANGUAGE_CATALOG_URL,
)
from neuralspace.utils import (
    get_auth_token,
    is_success_status,
    neuralspace_url,
    print_translation_response,
)

console = Console()

logger = logging.getLogger("rich")


class NSTranslationFailed(Exception):
    pass


async def get_translation_response(text: Text, src_language: Text, tgt_language):
    console = Console()
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {
        "text": text,
        "sourceLanguage": src_language,
        "targetLanguage": tgt_language,
    }
    console.print(
        f">[deep_sky_blue2] INFO [/deep_sky_blue2] Sending {ROCKET}Request to the server..."
    )
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{TRANSLATION_APP_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(
                f"> {INFO} [green]{GREEN_TICK} SUCCESS:[/green] Response received"
            )
            console.print(f"> {INFO} Parsing the information and creating a table")
            translated_text = html.unescape(json_response[DATA][TRANSLATED_TEXT])
            print_translation_response(
                text=html.unescape(text),
                src_language=src_language,
                tgt_language=tgt_language,
                translated_text=translated_text,
            )
        else:
            logger.error(f"{CROSS} Failed to get Translation response")
            logger.error(
                f"Platform response: {RED_START}{json_response['message']}{RED_END}"
            )


def get_translation_response_sync(text: Text, src_language: Text, tgt_language) -> Text:
    console = Console()
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {
        "text": text,
        "sourceLanguage": src_language,
        "targetLanguage": tgt_language,
    }
    console.print(
        f">[deep_sky_blue2] INFO [/deep_sky_blue2] Sending {ROCKET}Request to the server..."
    )
    response = requests.post(
        url=f"{neuralspace_url()}/{TRANSLATION_APP_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        console.print(
            f"> {INFO} [green]{GREEN_TICK} SUCCESS:[/green] Response received"
        )
        console.print(f"> {INFO} Parsing the information and creating a table")
        translated_text = html.unescape(json_response[DATA][TRANSLATED_TEXT])
        return translated_text
    else:
        NSTranslationFailed(f"Platform response: {json_response['message']}")


async def get_languages() -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {DOWN_ARROW}️ Fetching all supported languages for Translation"
    )
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().get(
        url=f"{neuralspace_url()}/{TRANSLATION_LANGUAGE_CATALOG_URL}",
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully Fetched Languages")
            table = Table()
            table.add_column("Language")
            table.add_column("Code")
            for row in json_response["data"]:
                table.add_row(row["language"], row["code"])
            console.print(table)
            console.print(
                f"{FAST_FORWARD} To translate text: {DARK_ORANGE_START}{TRANSLATE_TEXT_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to fetch languages")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response['message']}{RED_END} "'''
            )
    return json_response
