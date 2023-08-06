import hashlib
import json
import logging
import time
from asyncio import sleep
from copy import copy
from datetime import datetime
from typing import Any, Dict, List, Text, Tuple

import randomname
import requests
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from neuralspace.apis import get_async_http_session
from neuralspace.constants import (
    ARROW_UP,
    AUTHORIZATION,
    BIN,
    BOLD_END,
    BOLD_START,
    BOOK,
    CODE,
    COMMON_HEADERS,
    COMPLETED,
    CONFIDENCE,
    COUNT,
    CREATE_PROJECT_COMMAND,
    CROSS,
    DARK_ORANGE_END,
    DARK_ORANGE_START,
    DATA,
    DEAD,
    DEPLOY_MODEL_COMMAND,
    DEPLOYED,
    DEPLOYED_STATUS,
    DOWN_ARROW,
    END,
    END_INDEX,
    ENTITIES,
    ENTITIES_FILE,
    ENTITY,
    ENTITY_ID,
    ENTITY_PARTIAL_F1,
    ENTITY_TYPE,
    ERROR,
    EXAMPLE,
    EXAMPLE_ID,
    EXAMPLES,
    EXAMPLES_FILE,
    FAILED,
    FAST_FORWARD,
    FILTER,
    FINGER_RIGHT,
    GREEN_TICK,
    HASH,
    INFO,
    INITIATED,
    INTENT,
    INTENT_ACCURACY,
    INTENT_CLASSIFIER_METRICS,
    INTENT_RANKING,
    KEY,
    KEY_DATA,
    KEY_RASA,
    KEY_REPLICAS,
    LANGUAGE,
    LANGUAGES,
    LAST_STATUS_UPDATED,
    LIST_ENTITY_URL,
    LIST_MODELS_COMMAND,
    MESSAGE,
    METRICS,
    MODEL_ID,
    MODEL_NAME,
    MODELS,
    N_REPLICAS,
    NAME,
    NAME_GENERATOR_CONFIG,
    NER_METRICS,
    NO_OF_TRAINING_JOBS,
    NUMBER_OF_EXAMPLES,
    NUMBER_OF_INTENTS,
    NUMBER_OF_MODELS,
    NUMBERS_IN_SQUARE,
    OM,
    ORANGE_END,
    ORANGE_START,
    PAGE_NUMBER,
    PAGE_SIZE,
    PARSE_MODEL_COMMAND,
    PEN_AND_PAPER,
    PERSON_DUMBELL,
    PERSON_HERE,
    PERSON_STANDING,
    PERSON_TAKING,
    PIN,
    PREPARED,
    PROJECT_ID,
    PROJECT_NAME,
    PROJECTS,
    QUEUED,
    RED_END,
    RED_START,
    REPLICAS,
    SAD_SMILEY,
    SAND_CLOCK,
    SAVED,
    SEARCH,
    SOUP,
    START,
    START_INDEX,
    STATUS_MODEL_COMMAND,
    SYNONYMS,
    TEXT,
    TIMED_OUT,
    TRAIN_MODEL_COMMAND,
    TRAINING,
    TRAINING_STATUS,
    TRAINING_TIME,
    TYPE,
    UPLOAD_DATASET_COMMAND,
    USER_DEFINED_ENTITY_TYPES,
    WRITING,
    neuralspace_home,
    neuralspace_url,
    progress_bar,
)
from neuralspace.nlu.constants import (
    ADD_ENTITY_EXAMPLES_URL,
    ADD_SYNONYMS_TO_THE_PROJECT_URL,
    C_COMPLETED,
    C_DEAD,
    C_FAILED,
    C_INITIATED,
    C_QUEUED,
    C_TIMED_OUT,
    C_TRAINING,
    CREATE_ENTITY_URL,
    CREATE_EXAMPLE_URL,
    CREATE_PROJECT_URL,
    DEFAULT_RASA_TRAINING_JOBS,
    DELETE_ENTITY_EXAMPLES_URL,
    DELETE_ENTITY_URL,
    DELETE_EXAMPLE_URL,
    DELETE_MODELS_URL,
    DELETE_MULTIPLE_PROJECT_URL,
    DELETE_PROJECT_URL,
    DEPLOY_MODEL_URL,
    LANGUAGE_CATALOG_URL,
    LIST_EXAMPLES_URL,
    LIST_MODELS_URL,
    LIST_PROJECTS_URL,
    LIST_SYNONYMS_IN_THE_PROJECT_URL,
    PARSE_URL,
    SINGLE_MODEL_DETAILS_URL,
    TRAIN_MODEL_URL,
)
from neuralspace.nlu.utils import print_model_ids
from neuralspace.utils import get_auth_token, is_success_status, print_ner_response

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)


def create_project_sync(project_name: Text, languages: List[Text]) -> Dict[Text, Any]:
    logger.info(
        f"Creating a project called {project_name} in languages: {', '.join(languages)}"
    )
    payload = {PROJECT_NAME: project_name, LANGUAGE: languages}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    url = f"{neuralspace_url()}/{CREATE_PROJECT_URL}"
    response = requests.post(url, data=json.dumps(payload), headers=HEADERS)
    json_response = response.json()
    if is_success_status(response.status_code):
        logger.info("Successfully created project")
        logger.info(f"Project details: \n {json.dumps(json_response, indent=4)}")
    else:
        logger.error("Failed to create project")
        logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


async def get_languages() -> Dict[Text, Any]:
    console.print(f"> {INFO} {DOWN_ARROW}️ Fetching all supported languages for NLU")
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().get(
        url=f"{neuralspace_url()}/{LANGUAGE_CATALOG_URL}",
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully Fetched Languages")
            table = Table()
            table.add_column("Language")
            table.add_column(CODE)
            for row in json_response[DATA]:
                table.add_row(row[LANGUAGE], row[CODE])
            console.print(table)
            console.print(
                f"{FAST_FORWARD} To create the project: {DARK_ORANGE_START}{CREATE_PROJECT_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to create project")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )
    return json_response


async def create_project(project_name: Text, languages: List[Text]) -> Dict[Text, Any]:
    console.print(
        f"> {INFO} Creating a project called "
        f"{project_name} in languages: {', '.join(languages)}!"
    )
    payload = {PROJECT_NAME: project_name, LANGUAGE: languages}
    HEADERS = copy(COMMON_HEADERS)
    table = Table()
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{CREATE_PROJECT_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO}" f" {KEY} Retrieving credentials from config...")
            console.print(f"> {INFO} " f"{GREEN_TICK} Successfully created project!")
            console.print(
                f"> {INFO} " f"{PERSON_HERE} Here is your project information..."
            )
            table.add_column("Name")
            table.add_column(LANGUAGE)
            table.add_column("App Type")
            table.add_column("Project Id", style="green")
            language_to_write = ""
            for i, language in enumerate(json_response[DATA][LANGUAGE]):
                if i == len(json_response[DATA][LANGUAGE]) - 1:
                    language_to_write += language
                else:
                    language_to_write += language + ", "
            table.add_row(
                json_response[DATA][PROJECT_NAME],
                language_to_write,
                json_response[DATA]["appType"],
                json_response[DATA][PROJECT_ID],
            )
            console.print(table)
            console.print(
                f"{FAST_FORWARD} Upload data to your project using this command:"
                f" {DARK_ORANGE_START}{UPLOAD_DATASET_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to create   project")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}:- " {RED_START}{json_response[DATA]['error']}{RED_END} "'''
            )
    return json_response


async def delete_project(project_id: Text) -> Dict[Text, Any]:
    console.print(f"> {INFO} {BIN} Deleting project with id: {project_id}")
    payload = {PROJECT_ID: project_id}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().delete(
        url=f"{neuralspace_url()}/{DELETE_PROJECT_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully deleted project")
            console.print(
                f"{FAST_FORWARD} To create the project:  {DARK_ORANGE_START}{CREATE_PROJECT_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to delete projects")
            console.print(
                f"> Reason for failure {SAD_SMILEY}:- {RED_START}{json_response[MESSAGE]}{RED_END}"
            )
    return json_response


def print_projects_table(projects: Dict[Text, Any], verbose: bool):
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Project Name")
    table.add_column("Project ID")
    if verbose:
        table.add_column("Languages")
        table.add_column("Number of Examples")
        table.add_column("Number of Intents")
        table.add_column("Number of Models")
    for data in projects[DATA][PROJECTS]:
        args = [data[PROJECT_NAME], data[PROJECT_ID]]
        if verbose:
            args += [
                ", ".join(data[LANGUAGE]),
                str(data[NUMBER_OF_EXAMPLES]),
                str(data[NUMBER_OF_INTENTS]),
                str(data[NUMBER_OF_MODELS]),
            ]
        table.add_row(*args)
    console.print(table)


async def list_projects(
    search: Text, page_size: int, page_number: int, languages: List[Text], verbose: bool
) -> Dict[Text, Any]:
    payload = {
        SEARCH: search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
        LANGUAGES: languages,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_PROJECTS_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(
                f"> {INFO} {BOOK} Your projects for Page {page_number} "
                f"with Page Size: {page_size}"
            )
            print_projects_table(json_response, verbose)
            console.print(
                f"{FAST_FORWARD} To upload your dataset: {DARK_ORANGE_START}{UPLOAD_DATASET_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to list projects")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )
    return json_response


def print_examples_table(examples: Dict[Text, Any], verbose: bool = False):
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Example ID")
    table.add_column("Text")
    if verbose:
        table.add_column("Intent")
        table.add_column("N Entities", style="#c47900")

    console.print(
        f"> {INFO} {NUMBERS_IN_SQUARE} Total Examples Count: {examples[DATA][COUNT]}"
    )
    for data in examples[DATA][EXAMPLES]:
        marked_sentence = ""
        start_index = []
        end_index = []
        for i, entities in enumerate(data[ENTITIES]):
            start_index.append(entities[START])
            end_index.append(entities[END])
        for idx, character in enumerate(data[TEXT]):
            if idx in start_index:
                marked_sentence += "[bold green]"
            elif idx in end_index:
                marked_sentence += "[/bold green]"
            marked_sentence += character
        args = [data[EXAMPLE_ID], marked_sentence]
        if verbose:
            args += [data[INTENT], str(len(data[ENTITIES]))]
        table.add_row(*args)

    console.print(table)


async def list_examples(
    project_id: Text,
    language: Text,
    prepared: bool,
    type: Text,
    intent: Text,
    page_number: int,
    page_size: int,
    verbose: bool = False,
) -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {DOWN_ARROW}️ Fetching Examples with filter: \n"
        f"> {INFO} {HASH} {BOLD_START}Project ID:{BOLD_END} {ORANGE_START}{project_id}{ORANGE_END}\n"
        f"> {INFO} {OM} Language: {language}\n"
        f"> {INFO} {SOUP} Prepared: {prepared}\n"
        f"> {INFO} {PIN} type: {type}"
    )
    payload = {
        FILTER: {
            PROJECT_ID: project_id,
            LANGUAGE: language,
            PREPARED: prepared,
            TYPE: type,
        },
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    if intent:
        payload[FILTER][INTENT] = intent

    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_EXAMPLES_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            print_examples_table(json_response, verbose)
            console.print(
                f"{FAST_FORWARD} To train the model: {DARK_ORANGE_START}{TRAIN_MODEL_COMMAND}{DARK_ORANGE_END}"
            )
            console.print(
                f"{RED_START}{PEN_AND_PAPER}NOTE: To train a model in a project, the project must have minimum"
                f" [orange4]2[/orange4] intent and every intent must atleast have{RED_END} "
                f"[orange4]10[/orange4] {RED_START}training examples{RED_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to list examples")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )

    return json_response


def get_training_status_colour(status: Text) -> Text:
    if status == COMPLETED:
        return C_COMPLETED
    if status == TRAINING:
        return C_TRAINING
    elif status == FAILED:
        return C_FAILED
    elif status == TIMED_OUT:
        return C_TIMED_OUT
    elif status == DEAD:
        return C_DEAD
    elif status == INITIATED:
        return C_INITIATED
    elif status == QUEUED:
        return C_QUEUED
    elif status == SAVED:
        return C_COMPLETED
    elif status == DEPLOYED:
        return C_COMPLETED
    else:
        return C_INITIATED


def print_models_table(models: Dict[Text, Any], verbose: bool):
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Model ID")
    table.add_column("Model Name")
    if verbose:
        table.add_column("Training Status")
        table.add_column("Replicas")
        table.add_column("Intent Acc")
        table.add_column("Entity Partial F1")
        table.add_column("Training Time (sec)")
        table.add_column("Last Updated")
        table.add_column("Message")

    console.print(
        f"> {INFO} {NUMBERS_IN_SQUARE} Total Models Count: {models[DATA][COUNT]}"
    )
    for data in models[DATA][MODELS]:
        args = [data[MODEL_ID], data[MODEL_NAME]]
        if verbose:
            args += [
                f"{get_training_status_colour(data[TRAINING_STATUS])} {data[TRAINING_STATUS]}",
                str(data[REPLICAS]),
                "{:.3f}".format(
                    data[METRICS][INTENT_CLASSIFIER_METRICS][INTENT_ACCURACY]
                )
                if data[TRAINING_STATUS] == COMPLETED
                else "0.0",
                "{:.3f}".format(data[METRICS][NER_METRICS][ENTITY_PARTIAL_F1])
                if data[TRAINING_STATUS] == COMPLETED
                else "0.0",
                str(data[TRAINING_TIME])
                if data[TRAINING_STATUS] == COMPLETED
                else "0.0",
                str(data[LAST_STATUS_UPDATED]),
                data.get(MESSAGE, ""),
            ]
        table.add_row(*args)
    console.print(table)


async def list_models(
    project_id: Text,
    language: Text,
    training_status: List[Text],
    page_number: int,
    page_size: int,
    verbose: bool,
) -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {DOWN_ARROW}️ Fetching models with filter: \n"
        f"> {INFO} {FINGER_RIGHT} Project ID: {project_id}\n"
        f"> {INFO} {PERSON_TAKING} Language: {language}\n"
        f"> {INFO} {PERSON_DUMBELL}️ Training Statuses: {training_status}"
    )
    payload = {
        FILTER: {PROJECT_ID: project_id, LANGUAGE: language},
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    if training_status:
        payload[FILTER][TRAINING_STATUS] = training_status

    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{LIST_MODELS_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            print_models_table(json_response, verbose)
            console.print(
                f"{FAST_FORWARD} To deploy the model: {DARK_ORANGE_START}{DEPLOY_MODEL_COMMAND}{DARK_ORANGE_START}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to list models")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )
    return json_response


async def delete_examples(example_ids: List[Text]) -> Dict[Text, Any]:
    console.print(f"> {INFO} {BIN} Deleting Example with id: {example_ids}")
    for examples_id in example_ids:
        payload = {EXAMPLE_ID: examples_id}
        HEADERS = copy(COMMON_HEADERS)
        HEADERS[AUTHORIZATION] = get_auth_token()
        async with get_async_http_session().delete(
            url=f"{neuralspace_url()}/{DELETE_EXAMPLE_URL}",
            data=json.dumps(payload, ensure_ascii=False),
            headers=HEADERS,
        ) as response:
            json_response = await response.json(encoding="utf-8")
            if is_success_status(response.status):
                console.print(
                    f"> {INFO} {GREEN_TICK} Successfully deleted example_id: {examples_id}"
                )
            else:
                console.print(f"> {ERROR} {CROSS} Failed to delete examples")
                console.print(
                    f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
                )
    return json_response


async def upload_dataset(
    nlu_data: List[Dict[Text, Text]],
    project_id: Text,
    language: Text,
    skip_first: int = 0,
    ignore_errors: bool = False,
) -> List[Dict[Text, Any]]:
    responses = []
    error_examples = []
    console.print(
        f"> {INFO} Uploading {len(nlu_data) - skip_first} "
        f"examples for project {project_id} and language {language}"
    )
    console.print(f"> {INFO} Skipping first {skip_first} examples")
    Total_number_examples = len(nlu_data[skip_first:])
    current_example_number = 0

    task = progress_bar.add_task(description="", total=Total_number_examples)
    progress_bar.update(task)
    animation_tracker = 1
    for chunk_id, example in enumerate(nlu_data[skip_first:]):
        progress_bar.start()
        current_example_number += 1
        batch = {PROJECT_ID: project_id, LANGUAGE: language, EXAMPLE: example}
        HEADERS = copy(COMMON_HEADERS)
        HEADERS[AUTHORIZATION] = get_auth_token()
        async with get_async_http_session().post(
            url=f"{neuralspace_url()}/{CREATE_EXAMPLE_URL}",
            data=json.dumps(batch, ensure_ascii=False),
            headers=HEADERS,
        ) as response:
            if is_success_status(response.status):
                json_response = await response.json(encoding="utf-8")
                if current_example_number % 3 == 0:
                    if animation_tracker == 1:
                        progress_bar.update(task_id=task, description="🏃")
                        animation_tracker = 2
                    elif animation_tracker == 2:
                        progress_bar.update(task_id=task, description="🚶")
                        animation_tracker = 3
                    elif animation_tracker == 3:
                        progress_bar.update(task_id=task, description="🏃")
                        animation_tracker = 1
                responses.append(json_response)
                progress_bar.update(task_id=task, completed=current_example_number)
            else:
                if "text/html" in response.content_type:
                    message = response.text()
                else:
                    json_response = await response.json(encoding="utf-8")
                    message = json_response[MESSAGE]
                json_response = await response.json(encoding="utf-8")
                console.print(
                    f"> {ERROR} {CROSS} Failed to upload example with text "
                    f"{DARK_ORANGE_START}{example['text']}{DARK_ORANGE_END}"
                )

                console.print(
                    f"> Failed on example: \n{json.dumps(example, indent=4, ensure_ascii=False)}"
                )
                console.print(
                    f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{message}{RED_END} "'''
                )
                error_examples.append(example)
                if ignore_errors:
                    continue
                else:
                    break
    console.print(f"\n> {INFO} {GREEN_TICK} Uploaded {len(responses)} examples")
    console.print(f"> {INFO} {CROSS} Failed on {len(error_examples)} examples")
    with open("failed_examples.json", "w") as f:
        json.dump(error_examples, f, ensure_ascii=False)
        console.print(
            f"> {INFO} {WRITING} Writing failed examples into failed_examples.json"
        )
    console.print(
        f"To train your model: {DARK_ORANGE_START}{TRAIN_MODEL_COMMAND}{DARK_ORANGE_END}"
    )
    return responses


async def wait_till_training_completes(
    model_id: Text, wait: bool, wait_interval: int
) -> Dict[Text, Any]:
    json_response = None
    if wait:
        payload = {
            MODEL_ID: model_id,
        }
        HEADERS = copy(COMMON_HEADERS)
        HEADERS[AUTHORIZATION] = get_auth_token()
        console.print(
            f"> {INFO} {SAND_CLOCK} Waiting for model to "
            f"get trained; model id: {model_id}"
        )
        current_status = ""
        with console.status("...") as status:
            while True:
                async with get_async_http_session().get(
                    url=f"{neuralspace_url()}/{SINGLE_MODEL_DETAILS_URL}",
                    params=payload,
                    headers=HEADERS,
                ) as response:
                    json_response = await response.json(encoding="utf-8")
                    if is_success_status(response.status):
                        current_status = json_response[DATA][TRAINING_STATUS]
                        if (
                            json_response[DATA][TRAINING_STATUS] == COMPLETED
                            or json_response[DATA][TRAINING_STATUS] == FAILED
                            or json_response[DATA][TRAINING_STATUS] == TIMED_OUT
                            or json_response[DATA][TRAINING_STATUS] == DEAD
                        ):
                            if json_response[DATA][TRAINING_STATUS] == COMPLETED:
                                console.print(
                                    f"{FAST_FORWARD} To deploy your model on Neuralspace platform: "
                                    f"{DARK_ORANGE_START}{DEPLOY_MODEL_COMMAND}{DARK_ORANGE_END}"
                                )
                            if json_response[DATA][TRAINING_STATUS] == FAILED:
                                console.print(
                                    f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[DATA][MESSAGE]}{RED_END}\
                                     "'''
                                )
                            break
                    else:
                        console.print(f"> {ERROR} Failed to fetch model details")
                        console.print(
                            f'''> Reason for failure {SAD_SMILEY}:
                            " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
                        )
                        break
                    status.update(f"Model is {current_status} {PERSON_STANDING}")
                    await sleep(wait_interval)
                    status.update(f"Model is {current_status} {PERSON_DUMBELL}")
            console.print(
                f"> {INFO} "
                f"{get_training_status_colour(json_response[DATA][TRAINING_STATUS])} "
                f"Training status: {json_response[DATA][TRAINING_STATUS]}"
            )
    return json_response


async def train_model(
    project_id: Text, language: Text, model_name: Text, training_jobs: int
) -> Tuple[Dict[Text, Any], Dict[Text, Any]]:
    console.print(
        f"> {INFO} Queuing training job for: \n"
        f"> {INFO} Project ID: {project_id}\n"
        f"> {INFO} Language: {language}\n"
        f"> {INFO} Model Name: {model_name}"
    )
    payload = {
        PROJECT_ID: project_id,
        LANGUAGE: language,
        MODEL_NAME: model_name,
        NO_OF_TRAINING_JOBS: training_jobs,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{TRAIN_MODEL_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            model_ids = json_response[DATA]
            console.print(
                f"> {INFO}  Successfully queued {len(model_ids)} training jobs."
            )
            console.print(
                f"To checkout the training status use: {STATUS_MODEL_COMMAND}"
            )
            print_model_ids(model_ids)
            last_model_status = QUEUED
        else:
            console.print(f"> {ERROR} Failed to queue training job")
            console.print(f"> {ERROR} {json_response[MESSAGE]}")
            last_model_status = None
    return json_response, last_model_status


async def delete_models(model_id: Text) -> Dict[Text, Any]:
    console.print(f"> {INFO} {BIN} Deleting model with id: {model_id}")
    payload = {MODEL_ID: model_id}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    async with get_async_http_session().delete(
        url=f"{neuralspace_url()}/{DELETE_MODELS_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully deleted model")
            console.print(
                f"{FAST_FORWARD} To upload the dataset: {DARK_ORANGE_START}{UPLOAD_DATASET_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to delete models")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )
    return json_response


async def deploy(model_id: Text, n_replicas: int) -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {ARROW_UP}️ Deploying: Model ID: {model_id}; Replicas: {n_replicas};"
    )
    payload = {MODEL_ID: model_id, N_REPLICAS: n_replicas}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{DEPLOY_MODEL_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Model added to deployment queue.")
            console.print(
                f"{FAST_FORWARD} Check for replicas in model status to know that the model got deployed "
                f"(use the --verbose flag): "
                f"{DARK_ORANGE_START}{LIST_MODELS_COMMAND}{DARK_ORANGE_END}"
            )
            console.print(
                f"{FAST_FORWARD}Once the model is deployed parse text using: "
                f"{DARK_ORANGE_START}{PARSE_MODEL_COMMAND}{DARK_ORANGE_END}"
            )
        else:
            console.print(f"> {ERROR} {CROSS} Failed to deploy model")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )
    return json_response


def print_nlu_response(nlu_response: Dict[Text, Any], response_time: float):
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Text")
    table.add_column("Intent")
    table.add_column("Intent Confidence")
    table.add_column("Response Time (m-sec)")
    table.add_row(
        nlu_response[DATA][TEXT],
        nlu_response[DATA][INTENT][NAME],
        str(nlu_response[DATA][INTENT][CONFIDENCE]),
        str(response_time / 1000),
    )
    console.print(table)
    intent_ranking_table = Table(
        show_header=True, header_style="bold #c47900", show_lines=True
    )
    intent_ranking_table.add_column("Intent")
    intent_ranking_table.add_column("Confidence")

    for row in nlu_response[DATA][INTENT_RANKING]:
        intent_ranking_table.add_row(
            row["name"],
            str(row["confidence"]),
        )
    console.print(f"> {INFO} Intent Ranking")
    console.print(intent_ranking_table)
    formatted_entities = []
    for e in nlu_response[DATA][ENTITIES]:
        e[START_INDEX] = e[START]
        e[END_INDEX] = e[END]
        e[TYPE] = e[ENTITY]
        formatted_entities.append(e)
    print_ner_response(formatted_entities, nlu_response[DATA][TEXT])


async def parse(model_id: Text, input_text: Text) -> Dict[Text, Any]:
    console.print(
        f"> {INFO} {PEN_AND_PAPER} Parsing text: {input_text}, using Model ID: {model_id}"
    )
    payload = {MODEL_ID: model_id, TEXT: input_text}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    start = datetime.now()
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{PARSE_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    ) as response:
        end = datetime.now()
        response_time = (end - start).microseconds
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(f"> {INFO} {GREEN_TICK} Successfully parsed text")
            print_nlu_response(json_response, response_time)
        else:
            console.print(f"> {ERROR} {CROSS} Failed to parse model")
            console.print(
                f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
            )
    return json_response


def calculate_hash(example: Dict):
    hash = (
        int(
            hashlib.sha256(
                json.dumps(example, ensure_ascii=False).encode("utf-8")
            ).hexdigest(),
            16,
        )
        % 10**8
    )
    return str(hash)


def get_uploaded_examples(project_id) -> Dict[Text, Any]:
    examples_file = neuralspace_home() / KEY_RASA / project_id / EXAMPLES_FILE
    uploaded_examples = {}
    if examples_file.exists():
        with open(examples_file, "r") as exf:
            uploaded_examples = json.load(exf)
    return uploaded_examples


def get_uploaded_entities(project_id) -> Dict[Text, Any]:
    entities_file = neuralspace_home() / KEY_RASA / project_id / ENTITIES_FILE
    uploaded_entities = {}
    if entities_file.exists():
        with open(entities_file) as exf:
            uploaded_entities = json.load(exf)
    return uploaded_entities


def update_examples(uploaded_examples: Dict[Text, Any], project_id: Text):
    examples_file = neuralspace_home() / KEY_RASA / project_id / EXAMPLES_FILE
    if not examples_file.parent.exists():
        examples_file.parent.mkdir(exist_ok=True)
    with open(examples_file, "w") as exf:
        json.dump(uploaded_examples, exf, ensure_ascii=False, indent=4)


def update_entities(uploaded_entities: Dict[Text, Any], project_id: Text):
    examples_file = neuralspace_home() / KEY_RASA / project_id / ENTITIES_FILE
    if not examples_file.parent.exists():
        examples_file.parent.mkdir(exist_ok=True)
    with open(examples_file, "w") as exf:
        json.dump(uploaded_entities, exf, indent=4)


def upload_example_sync(
    example: Dict[Text, Any], project_id: Text, language: Text
) -> requests.Response:
    logger.debug(f"Uploading example: {example}")
    batch = {PROJECT_ID: project_id, LANGUAGE: language, EXAMPLE: example}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()

    url = f"{neuralspace_url()}/{CREATE_EXAMPLE_URL}"
    response = requests.post(
        url, data=json.dumps(batch, ensure_ascii=False), headers=HEADERS
    )
    return response


def upload_entity_sync(example: Dict[Text, Any]) -> requests.Response:
    console.print(f"Uploading entity: {example}")
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    url = f"{neuralspace_url()}/{CREATE_ENTITY_URL}"
    response = requests.post(
        url, data=json.dumps(example, ensure_ascii=False), headers=HEADERS
    )
    return response


def start_training(project_id: Text, language: Text) -> Dict[Text, Any]:
    data = {
        PROJECT_ID: project_id,
        LANGUAGE: language,
        NO_OF_TRAINING_JOBS: DEFAULT_RASA_TRAINING_JOBS,
    }
    url = f"{neuralspace_url()}/{TRAIN_MODEL_URL}"
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.post(url=url, json=data, headers=HEADERS)
    json_response: Dict = response.json(encoding="utf-8")
    if not is_success_status(response.status_code):
        raise Exception(json_response.get(MESSAGE))
    return json_response


def wait_till_training_completes_sync(
    model_id: Text,
    wait_interval: int,
) -> Dict[Text, Any]:
    payload = {
        MODEL_ID: model_id,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    console.print(
        f"> {INFO} {SAND_CLOCK} Waiting for model to "
        f"get trained; model id: {model_id}"
    )
    with console.status("...") as status:
        while True:
            response = requests.get(
                url=f"{neuralspace_url()}/{SINGLE_MODEL_DETAILS_URL}",
                params=payload,
                headers=HEADERS,
            )
            json_response: Dict[Text, Any] = response.json(encoding="utf-8")
            if is_success_status(response.status_code):
                current_status = json_response[DATA][TRAINING_STATUS]
                if (
                    json_response[DATA][TRAINING_STATUS] == COMPLETED
                    or json_response[DATA][TRAINING_STATUS] == FAILED
                    or json_response[DATA][TRAINING_STATUS] == TIMED_OUT
                    or json_response[DATA][TRAINING_STATUS] == DEAD
                ):
                    if json_response[DATA][TRAINING_STATUS] == COMPLETED:
                        pass
                    if json_response[DATA][TRAINING_STATUS] == FAILED:
                        console.print(
                            f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[DATA]['message']}{RED_END}\
                                                 "'''
                        )
                        raise Exception("Model training failed")
                    break
            else:
                console.print(f"> {ERROR} Failed to fetch model details")
                console.print(
                    f'''> Reason for failure {SAD_SMILEY}:
                                        " {RED_START}{json_response['message']}{RED_END} "'''
                )
                raise Exception("Model training failed")
            status.update(f"Model is {current_status} {PERSON_STANDING}")
            time.sleep(wait_interval)
            status.update(f"Model is {current_status} {PERSON_DUMBELL}")
        console.print(
            f"> {INFO} "
            f"{get_training_status_colour(json_response[DATA][TRAINING_STATUS])} "
            f"Training status: {json_response[DATA][TRAINING_STATUS]}"
        )
    return json_response


def wait_till_deploy_completes_sync(
    model_id: Text,
    wait_interval: int,
    timeout_in_mins: int = 5,
    check_n_replicas: int = 1,
) -> Dict[Text, Any]:
    payload = {
        MODEL_ID: model_id,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    start_time = datetime.now()
    with console.status("...") as status:
        while True:
            response = requests.get(
                url=f"{neuralspace_url()}/{SINGLE_MODEL_DETAILS_URL}",
                params=payload,
                headers=HEADERS,
            )
            json_response: Dict[Text, Any] = response.json(encoding="utf-8")
            current_status = json_response[DATA][DEPLOYED_STATUS]
            if is_success_status(response.status_code):
                if (
                    json_response[DATA][KEY_REPLICAS] == check_n_replicas
                    and current_status == DEPLOYED
                ):

                    break
                elif json_response[DATA][DEPLOYED_STATUS] == FAILED:
                    console.print(
                        f'''> Reason for failure {SAD_SMILEY}: " {RED_START}{json_response[DATA]['message']}{RED_END}\
                                             "'''
                    )
                    raise Exception(
                        f"Model deployment failed because: {json.dumps(response.json(), indent=4)}"
                    )
            else:
                console.print(f"> {ERROR} Failed to fetch model details")
                console.print(
                    f'''> Reason for failure {SAD_SMILEY}:
                                        " {RED_START}{json_response[MESSAGE]}{RED_END} "'''
                )
                raise Exception("Model training failed")
            status.update(
                f"Model is {current_status} with currently "
                f"{json_response[DATA][KEY_REPLICAS]} replicas {PERSON_STANDING}"
            )
            time.sleep(wait_interval)
            status.update(
                f"Model is {current_status} with currently "
                f"{json_response[DATA][KEY_REPLICAS]} replicas {PERSON_DUMBELL}"
            )
            end_time = datetime.now()
            time_diff_in_mins = (end_time - start_time).seconds / 60
            if time_diff_in_mins >= timeout_in_mins:
                raise Exception(
                    f"Timeout while waiting for model to get deployed. Timeout set to {timeout_in_mins}"
                )
        if check_n_replicas != 0:
            console.print(
                f"> {INFO} "
                f"{get_training_status_colour(current_status)} "
                f"Deployment status: {current_status}"
            )
    return json_response


def parse_sync(model_id: Text, input_text: Text) -> Dict[Text, Any]:
    logger.info(f"Parsing text: {input_text}, using Model ID: {model_id}")
    payload = {MODEL_ID: model_id, TEXT: input_text}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    print(json.dumps(payload))
    start = datetime.now()
    response = requests.post(
        url=f"{neuralspace_url()}/{PARSE_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    print(f"Response is :: {response.text}")
    end = datetime.now()
    response_time = (end - start).microseconds
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        logger.debug(
            f"Platform Response: \n{json.dumps(json_response, indent=4, ensure_ascii=False)}"
        )
        print_nlu_response(json_response, response_time)
    else:
        logger.error("Failed to deploy model")
        logger.error(f"Platform response: \n {json.dumps(json_response, indent=4)}")
    return json_response


def deploy_sync(model_id: Text, n_replicas: int) -> Dict[Text, Any]:
    if n_replicas == 0:
        console.print(f"> {INFO} Un-deploying the Previous model: {model_id}")
    else:
        console.print(f"> {INFO} Deploying the current model: {model_id}")
    payload = {MODEL_ID: model_id, N_REPLICAS: n_replicas}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.post(
        url=f"{neuralspace_url()}/{DEPLOY_MODEL_URL}", json=payload, headers=HEADERS
    )
    json_response = response.json(encoding="utf-8")
    return json_response


def delete_examples_sync(example_id: Text) -> Dict[Text, Any]:
    console.print(f"> {INFO} {BIN} Deleting Example with id: {example_id}")
    payload = {EXAMPLE_ID: example_id}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.delete(
        url=f"{neuralspace_url()}/{DELETE_EXAMPLE_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        logger.debug(
            f"> {INFO} {GREEN_TICK} Successfully deleted example: {example_id}!"
        )
    else:
        raise Exception(
            f"> {ERROR} {CROSS} Failed to add entity examples {SAD_SMILEY}: "
            f"{RED_START}{json_response['message']}{RED_END}"
        )
    return json_response


def delete_entity_sync(entity_id: Text) -> Dict[Text, Any]:
    console.print(f"> {INFO} {BIN} Deleting entity with id: {entity_id}")
    payload = {ENTITY_ID: entity_id}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.delete(
        url=f"{neuralspace_url()}/{DELETE_ENTITY_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        logger.debug(f"> {INFO} {GREEN_TICK} Successfully deleted entity!")
    else:
        raise Exception(
            f'''> Failed to delete entity {SAD_SMILEY}: " {json_response['message']}"'''
        )
    return json_response


def delete_entity_examples_sync(
    entity_id: Text, examples: List[Text]
) -> Dict[Text, Any]:
    logger.debug(f"> {INFO} {BIN} Deleting entity with id: {entity_id}")
    payload = {ENTITY_ID: entity_id, EXAMPLES: examples}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.post(
        url=f"{neuralspace_url()}/{DELETE_ENTITY_EXAMPLES_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        logger.debug(f"> {INFO} {GREEN_TICK} Successfully deleted entity examples!")
    else:
        raise Exception(
            f"{ERROR} {CROSS} Failed to delete entity examples {SAD_SMILEY}: "
            f"{RED_START}{json_response['message']}{RED_END} "
        )

    return json_response


def add_entity_examples_sync(entity_id: Text, examples: List[Text]) -> Dict[Text, Any]:
    logger.debug(
        f"> {INFO} {BIN} Adding examples {examples} to entity with id: {entity_id}"
    )
    payload = {ENTITY_ID: entity_id, EXAMPLES: examples}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.post(
        url=f"{neuralspace_url()}/{ADD_ENTITY_EXAMPLES_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    if is_success_status(response.status_code):
        logger.debug(f"> {INFO} {GREEN_TICK} Successfully added entity examples!")
    else:
        raise Exception(
            f"> {ERROR} {CROSS} Failed to add entity examples {SAD_SMILEY}:  "
            f"{RED_START}{json_response['message']}{RED_END}"
        )
    return json_response


def create_project_id(language: Text):
    console.print(f"Creating a new project with language {language}")
    result = create_project_sync(
        project_name=f"rasa-{randomname.get_name(**NAME_GENERATOR_CONFIG)}-{language}-{datetime.now()}",
        languages=[language],
    )
    return result[KEY_DATA][PROJECT_ID]


def list_projects_sync(
    search: Text, page_size: int, page_number: int, languages: List[Text], verbose: bool
) -> Dict[Text, Any]:
    payload = {
        SEARCH: search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
        LANGUAGES: languages,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.post(
        url=f"{neuralspace_url()}/{LIST_PROJECTS_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    return json_response


def delete_multiple_project_sync(project_ids: List[Text]):
    payload = {PROJECT_ID: project_ids}
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    response = requests.delete(
        url=f"{neuralspace_url()}/{DELETE_MULTIPLE_PROJECT_URL}",
        data=json.dumps(payload, ensure_ascii=False),
        headers=HEADERS,
    )
    json_response = response.json(encoding="utf-8")
    return json_response


def delete_all_project(total_projects: int):
    project_ids = []
    if not total_projects == 0:
        all_projects = list_projects_sync(
            "", page_size=total_projects, page_number=1, languages=[], verbose=False
        )
        all_projects = all_projects[DATA][PROJECTS]
        for project in all_projects:
            project_ids.append(project[PROJECT_ID])
        delete_multiple_project_sync(project_ids)


def list_entity_sync(
    entity_type: Text, page_size: int, page_number: int, search: Text, language: Text
) -> Dict[Text, Any]:
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {
        FILTER: {ENTITY_TYPE: entity_type, LANGUAGE: language},
        SEARCH: search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    response = requests.post(
        url=f"{neuralspace_url()}/{LIST_ENTITY_URL}",
        headers=HEADERS,
        data=json.dumps(payload),
    )
    if not is_success_status(response.status_code):
        raise Exception(
            "Error while Getting the entities from the platform please try again"
            "after some time or raise a query in the slack channel"
        )

    json_response = response.json()
    return json_response


def list_all_entity_sync(language: Text) -> Dict[Text, Dict[Text, Any]]:
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    entities_names = {}
    for entity_type in USER_DEFINED_ENTITY_TYPES:
        json_response = list_entity_sync(
            entity_type, page_size=1, page_number=1, search="", language=language
        )
        logger.debug(json_response)
        count = json_response[DATA][COUNT]
        if not count == 0:
            json_response = list_entity_sync(
                entity_type,
                page_size=count,
                page_number=1,
                search="",
                language=language,
            )
            entities_names[entity_type] = {
                entity[ENTITY]: {
                    ENTITY_ID: entity[ENTITY_ID],
                    EXAMPLES: entity[EXAMPLES],
                }
                for entity in json_response[DATA][ENTITIES]
            }
        else:
            entities_names[entity_type] = {}
    return entities_names


def add_synonym_to_project_sync(project_id: Text, language: Text, entity_id: Text):
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {
        PROJECT_ID: project_id,
        LANGUAGE: language,
        ENTITY_ID: entity_id,
    }
    response = requests.post(
        url=f"{neuralspace_url()}/{ADD_SYNONYMS_TO_THE_PROJECT_URL}",
        headers=HEADERS,
        data=json.dumps(payload),
    )
    if not is_success_status(response.status_code):
        raise Exception(
            "Error while Adding the synonym from the platform please try again"
            "after some time or raise a query in the slack channel"
        )

    json_response = response.json()
    return json_response


def list_project_synonym_sync(
    project_id: Text, language: Text, search: Text, page_number: int, page_size: int
):
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {
        PROJECT_ID: project_id,
        LANGUAGE: language,
        SEARCH: search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    response = requests.post(
        url=f"{neuralspace_url()}/{LIST_SYNONYMS_IN_THE_PROJECT_URL}",
        headers=HEADERS,
        data=json.dumps(payload),
    )
    if not is_success_status(response.status_code):
        raise Exception(
            "Error while Getting the project synonyms from the platform please try again"
            "after some time or raise a query in the slack channel"
        )

    json_response = response.json()
    return json_response


def list_all_project_synonym_sync(project_id: Text, language: Text):
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    synonym_list = {}
    json_response = list_project_synonym_sync(
        project_id, page_size=1, page_number=1, search="", language=language
    )
    logger.debug(json_response)
    count = json_response[DATA][COUNT]
    if not count == 0:
        json_response = list_project_synonym_sync(
            project_id,
            page_size=count,
            page_number=1,
            search="",
            language=language,
        )
        synonym_list = {
            synonym[ENTITY]: synonym[ENTITY_ID]
            for synonym in json_response[DATA][SYNONYMS]
        }
    return synonym_list
