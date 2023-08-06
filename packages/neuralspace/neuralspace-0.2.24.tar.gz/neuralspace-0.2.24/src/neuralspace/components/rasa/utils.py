import json
from pathlib import Path
from typing import Any, Dict, Text

from rich.table import Table

from neuralspace.constants import (
    KEY_MODEL_IDS,
    KEY_PATH_TO_PROJECT_ID,
    KEY_PROJECT_DETAILS,
    KEY_PROJECT_IDS,
    KEY_RASA,
    NS_RASA_METADATA_FILE,
    ORANGE3_END,
    ORANGE3_START,
    neuralspace_home,
)
from neuralspace.nlu.apis import create_project_id


def metadata_file_path() -> Path:
    metadata_path = neuralspace_home() / KEY_RASA / NS_RASA_METADATA_FILE
    metadata_path.parent.mkdir(exist_ok=True)
    if not metadata_path.exists():
        initial_meta_file = {
            KEY_PROJECT_IDS: [],
            KEY_PROJECT_DETAILS: {},
            KEY_PATH_TO_PROJECT_ID: {},
        }
        with open(metadata_path, "w") as meta_file_pointer:
            json.dump(initial_meta_file, meta_file_pointer, indent=4)
    return metadata_path


def get_metadata() -> Dict[Text, Any]:
    with open(metadata_file_path(), "r") as file_pointer:
        metadata = json.load(file_pointer)
    return metadata


def update_metadata(metadata: Dict[Text, Any]):
    with open(metadata_file_path(), "w") as file_pointer:
        json.dump(metadata, file_pointer, ensure_ascii=False, indent=4)


def get_project_id_if_exists(
    working_directory: Text, create_if_doesnt_exist: bool = False, language: Text = None
) -> Text:
    metadata = get_metadata()
    project_id = None
    if working_directory in metadata[KEY_PATH_TO_PROJECT_ID]:
        project_id = metadata[KEY_PATH_TO_PROJECT_ID][working_directory]
    elif create_if_doesnt_exist:
        project_id = create_project_id(language=language)
    return project_id


def get_recent_model_id(project_id: Text):
    meta_data = get_metadata()
    return meta_data[KEY_PROJECT_DETAILS][project_id][KEY_MODEL_IDS][-1]


def print_table_description_for_examples(
    total_uploaded_examples,
    total_removed_examples,
    total_uploaded_entities,
    total_removed_entities,
    total_removed_entities_examples,
    total_uploaded_entities_examples,
) -> Table:
    table = Table(show_header=True, header_style="bold #c47900", show_lines=True)
    table.add_column("Contents")
    table.add_column("Total")
    table.add_row(
        f"{ORANGE3_START}Uploaded NLU Examples{ORANGE3_END}",
        str(total_uploaded_examples),
    )
    table.add_row(
        f"{ORANGE3_START}Uploaded Entities{ORANGE3_END}", str(total_uploaded_entities)
    )
    table.add_row(
        f"{ORANGE3_START}Uploaded Entities Example{ORANGE3_END}",
        str(total_uploaded_entities_examples),
    )
    table.add_row(
        f"{ORANGE3_START}Removed NLU Examples{ORANGE3_END}", str(total_removed_examples)
    )
    table.add_row(
        f"{ORANGE3_START}Removed Entities{ORANGE3_END}", str(total_removed_entities)
    )
    table.add_row(
        f"{ORANGE3_START}Removed Entities Example{ORANGE3_END}",
        str(total_removed_entities_examples),
    )
    return table
