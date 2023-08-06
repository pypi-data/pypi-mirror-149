import html
import json
import logging
from copy import copy
from typing import Any, Dict, Text

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
    SUGGESTIONS,
)
from neuralspace.transliteration.constants import (
    TRANSLIT_TEXT_COMMAND,
    TRANSLITERATION_APP_URL,
    TRANSLITERATION_LANGUAGE_CATALOG_URL,
)
from neuralspace.utils import (
    get_auth_token,
    is_success_status,
    neuralspace_url,
    print_transliteration_response,
)

console = Console()

logger = logging.getLogger("rich")


async def get_transliteration_response(
    text: Text, src_language: Text, tgt_language, suggestion_count: int
):
    console = Console()
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {
        "text": text,
        "sourceLanguage": src_language,
        "targetLanguage": tgt_language,
        "suggestionCount": suggestion_count,
    }
    console.print(
        f">[deep_sky_blue2] INFO [/deep_sky_blue2] Sending {ROCKET}Request to the server..."
    )
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{TRANSLITERATION_APP_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(
                f"> {INFO} [green]{GREEN_TICK} SUCCESS:[/green] Response received"
            )
            console.print(f"> {INFO} Parsing the information and creating a table")
            transliteration_suggestions = html.unescape(
                json_response[DATA][SUGGESTIONS]
            )
            print_transliteration_response(
                text=html.unescape(text),
                src_language=src_language,
                tgt_language=tgt_language,
                suggestions=transliteration_suggestions,
            )
        else:
            logger.error(f"{CROSS} Failed to get Transliteration response")
            logger.error(
                f"Platform response: {RED_START}{json_response['message']}{RED_END}"
            )


async def get_languages() -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {DOWN_ARROW}️ Fetching all supported languages for Transliteration"
    )
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().get(
        url=f"{neuralspace_url()}/{TRANSLITERATION_LANGUAGE_CATALOG_URL}",
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully Fetched Languages")
            table = Table(show_header=True, header_style="orange3")
            table.add_column("Language Pair", style="sandy_brown")
            table.add_column("Code", style="green")
            for row in json_response["data"]:
                table.add_row(row["languagePair"], row["code"])
            console.print(table)
            console.print(
                f"{FAST_FORWARD} To transliterate text: {DARK_ORANGE_START}{TRANSLIT_TEXT_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to fetch languages")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response['message']}{RED_END} "'''
            )
    return json_response
