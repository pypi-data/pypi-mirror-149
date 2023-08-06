import json
import time as t
from copy import copy
from pathlib import Path
from typing import Any, Dict, List, Text, Tuple

import requests
from rich.console import Console
from rich.table import Table

from neuralspace.constants import (
    AUTHORIZATION,
    BAG,
    COMMON_HEADERS,
    COUNT,
    CROSS,
    DATA,
    ENTITIES,
    ENTITY,
    ENTITY_TYPE,
    EXAMPLES,
    FILTER,
    GREEN_TICK,
    INFO,
    LANGUAGE,
    LIST_ENTITY_URL,
    LOOKUP,
    PAGE_NUMBER,
    PAGE_SIZE,
    PRE_TRAINED,
    REGEX,
    SEARCH,
    neuralspace_url,
)
from neuralspace.utils import get_auth_token, is_success_status

console = Console()


def convert_files(convert, rasa_data):
    lookup_data = convert.lookup_converter(rasa_data.lookup_tables)
    regex_data = convert.regex_converter(rasa_data.regex_features)
    synonym_data = convert.synonym_converter(rasa_data.entity_synonyms)
    training_data = convert.training_data_converter(rasa_data)
    return lookup_data, regex_data, synonym_data, training_data


def __replace_entities_with_mapping(
    entities: List[Dict[Text, Any]], entity_mapping: Dict[Text, Text]
):
    for entity_value in entities:
        if entity_value[ENTITY] in entity_mapping:
            entity_value[ENTITY] = entity_mapping[entity_value[ENTITY]]


def map_entities(nlu_data: List[Dict[Text, Any]], entity_mapping: Dict[Text, Text]):
    for example in nlu_data:
        entities = example.get(ENTITIES, [])
        if entities:
            __replace_entities_with_mapping(entities, entity_mapping)
    return nlu_data


def get_entity_list_from_remote(
    entity_type: Text,
    language: Text,
    keyword_search: Text = "",
    page_size: int = 1,
    page_number: int = 10,
    authtoken: Text = None,
) -> Tuple[List[Dict[Text, Any]], int]:
    payload = {
        FILTER: {ENTITY_TYPE: entity_type, LANGUAGE: language},
        SEARCH: keyword_search,
        PAGE_NUMBER: page_number,
        PAGE_SIZE: page_size,
    }
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = authtoken if authtoken else get_auth_token()

    response = requests.request(
        "POST",
        f"{neuralspace_url()}/{LIST_ENTITY_URL}",
        headers=HEADERS,
        data=json.dumps(payload, ensure_ascii=False),
    )
    json_response = response.json(encoding="utf-8")

    if not is_success_status(response.status_code):
        raise Exception(
            f"Error while fetching entities. "
            f"Error message: {json.dumps(json_response, indent=4)}"
        )
    return json_response[DATA][ENTITIES], json_response[DATA][COUNT]


def auto_tag_pretrained_entities(
    data: List[Dict[Text, Any]], language: Text, authtoken: Text = None
):
    sample_pretrained_entities, count = get_entity_list_from_remote(
        entity_type=PRE_TRAINED, language=language, authtoken=authtoken
    )
    if count:
        all_pretrained_entities, _ = get_entity_list_from_remote(
            entity_type=PRE_TRAINED,
            language=language,
            page_number=1,
            page_size=count,
            authtoken=authtoken,
        )
        all_pretrained_entity_names = {
            entity[ENTITY]: entity[ENTITY] for entity in all_pretrained_entities
        }
        for example in data:
            entities = example.get(ENTITIES, [])
            for entity_value in entities:
                if entity_value[ENTITY] in all_pretrained_entity_names:
                    entity_value[ENTITY] = all_pretrained_entity_names[
                        entity_value[ENTITY]
                    ]
                    entity_value[ENTITY_TYPE] = PRE_TRAINED
    return data


def auto_tag_lookup(
    data: List[Dict[Text, Any]], lookup_entities: List[Dict[Text, Any]]
):
    all_lookup_entity_names = {
        entity[ENTITY]: entity[ENTITY] for entity in lookup_entities
    }
    for example in data:
        entities = example.get(ENTITIES, [])
        for entity_value in entities:
            if (
                entity_value[ENTITY] in all_lookup_entity_names
                and ENTITY_TYPE not in entity_value
            ):
                entity_value[ENTITY] = all_lookup_entity_names[entity_value[ENTITY]]
                entity_value[ENTITY_TYPE] = LOOKUP
    return data


def auto_tag_regex(data: List[Dict[Text, Any]], regex_entities: List[Dict[Text, Any]]):
    all_regex_entity_names = {
        entity[ENTITY]: entity[ENTITY] for entity in regex_entities
    }
    for example in data:
        entities = example.get(ENTITIES, [])
        for entity_value in entities:
            if (
                entity_value[ENTITY] in all_regex_entity_names
                and ENTITY_TYPE not in entity_value
            ):
                entity_value[ENTITY] = all_regex_entity_names[entity_value[ENTITY]]
                entity_value[ENTITY_TYPE] = REGEX
    return data


def remove_nlu_duplicates(
    data_to_clear_duplicates: List[Dict[Text, Any]]
) -> List[Dict[Text, Any]]:
    # removing the duplicate entry
    unique_dict = [
        k
        for j, k in enumerate(data_to_clear_duplicates)
        if k not in data_to_clear_duplicates[j + 1 :]  # noqa : E203
    ]
    return unique_dict


def remove_entity_duplicates(
    entities: List[Dict[Text, Any]],
) -> List[Dict[Text, Any]]:
    for entity in entities:
        entity[EXAMPLES] = sorted(list(set(entity[EXAMPLES])), key=str.casefold)
    return entities


def print_converted_data_inference(from_platform: Text, output_path: Path, converter):
    console.print(
        f"> {GREEN_TICK} SUCCESS Your {from_platform} dataset is now converted to Neuralspace-platform data"
    )
    console.print(f"> {INFO} Converted dataset is {BAG} stored in: {output_path}")
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Contents")
    table.add_column("Total")
    table.add_row(
        "Number of examples before removing duplicates",
        str(converter.number_of_nlu_examples_before_duplicate_check),
    )
    table.add_row(
        "Number of examples after removing the duplicates",
        str(converter.number_of_nlu_examples_after_duplicate_check),
    )
    table.add_row("Number of intent present", str(converter.number_of_unique_intent()))
    console.print(table)
    console.print(
        "Number of duplicates found: ",
        str(
            converter.number_of_nlu_examples_before_duplicate_check
            - converter.number_of_nlu_examples_after_duplicate_check
        ),
    )
    console.print("\nChecking Files... \n")
    console.print("> Lookups", end=" ")
    t.sleep(1)
    console.print(f"{GREEN_TICK} ") if converter.lookup_data else console.print(
        f"{CROSS} "
    )
    console.print("> Synonyms", end=" ")
    t.sleep(1)
    console.print(f"{GREEN_TICK} ") if converter.synonym_data else console.print(
        f"{CROSS} "
    )
    console.print("> Regex", end=" ")
    t.sleep(1)
    console.print(f"{GREEN_TICK} ") if converter.regex_data else console.print(
        f"{CROSS} "
    )


def print_model_ids(model_ids: List[Text]):
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Index")
    table.add_column("Model Id")
    for index, single_model_id in enumerate(model_ids):
        table.add_row(str(index), single_model_id)
    console.print(table)
