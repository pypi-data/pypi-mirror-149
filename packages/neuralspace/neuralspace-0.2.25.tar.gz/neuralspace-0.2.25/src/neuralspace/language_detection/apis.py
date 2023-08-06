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
    DETECTED_LANGUAGES,
    DOWN_ARROW,
    ERROR,
    FAST_FORWARD,
    GREEN_TICK,
    INFO,
    LANGUAGE,
    RED_END,
    RED_START,
    ROCKET,
    SAD_SMILEY,
)
from neuralspace.language_detection.constants import (
    LANG_DETECTION_TEXT_COMMAND,
    LANGUAGE_DETECTION_APP_URL,
    LANGUAGE_DETECTION_LANGUAGE_CATALOG_URL,
)
from neuralspace.utils import (
    get_auth_token,
    is_success_status,
    neuralspace_url,
    print_language_detection_response,
)

console = Console()

logger = logging.getLogger("rich")


class NSLanguageDetectionFailed(Exception):
    pass


async def get_language_detection_response(text: Text):
    console = Console()
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {"text": text}
    console.print(
        f">[deep_sky_blue2] INFO [/deep_sky_blue2] Sending {ROCKET}Request to the server..."
    )
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LANGUAGE_DETECTION_APP_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(
                f"> {INFO} [green]{GREEN_TICK} SUCCESS:[/green] Response received"
            )
            console.print(f"> {INFO} Parsing the information and creating a table")
            detected_languages = html.unescape(json_response[DATA][DETECTED_LANGUAGES])
            print_language_detection_response(
                text=html.unescape(text),
                detected_languages=detected_languages,
            )
        else:
            logger.error(f"{CROSS} Failed to get Language Detection response")
            logger.error(
                f"Platform response: {RED_START}{json_response['message']}{RED_END}"
            )


def get_language_detection_response_sync(text: Text) -> Text:
    console = Console()
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {"text": text}
    console.print(
        f">[deep_sky_blue2] INFO [/deep_sky_blue2] Sending {ROCKET}Request to the server..."
    )
    response = requests.post(
        url=f"{neuralspace_url()}/{LANGUAGE_DETECTION_APP_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        console.print(
            f"> {INFO} [green]{GREEN_TICK} SUCCESS:[/green] Response received"
        )
        console.print(f"> {INFO} Parsing the information and creating a table")
        detected_languages = html.unescape(json_response[DATA][DETECTED_LANGUAGES])
        print_language_detection_response(
            text=html.unescape(text),
            detected_languages=detected_languages,
        )
        return detected_languages[0][LANGUAGE]
    else:
        NSLanguageDetectionFailed(f"Platform response: {json_response['message']}")


async def get_languages() -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {DOWN_ARROW}️ Fetching all supported languages for Language Detection"
    )
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().get(
        url=f"{neuralspace_url()}/{LANGUAGE_DETECTION_LANGUAGE_CATALOG_URL}",
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully Fetched Languages")
            table = Table()
            table.add_column("Languages", style="sandy_brown")
            for row in json_response["data"]:
                table.add_row(row)
            console.print(table)
            console.print(
                f"{FAST_FORWARD} To detect language: {DARK_ORANGE_START}{LANG_DETECTION_TEXT_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to fetch languages")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response['message']}{RED_END} "'''
            )
    return json_response
