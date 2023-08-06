import os
from pathlib import Path
from typing import Text

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    Task,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.text import Text as Text_render

__NEURALSPACE_URL = "https://platform.neuralspace.ai"
NEURALSPACE_URL_ENV_VAR = "NEURALSPACE_URL"
LOGIN_URL = "api/auth/login"
INSTALL_APP_URL = "api/app/install"

COMMON_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
}

NAME_GENERATOR_CONFIG = {
    "adj": ("emotions", "age", "character"),
}

# Literals to be used globally
NEURALSPACE_PATH_ENV_VAR = "NEURALSPACE_PATH"

# Panini default data directory
__NEURALSPACE_HOME = Path.home() / ".neuralspace"


def neuralspace_home() -> Path:
    global __NEURALSPACE_HOME

    if NEURALSPACE_PATH_ENV_VAR in os.environ:
        __NEURALSPACE_HOME = Path(os.environ[NEURALSPACE_PATH_ENV_VAR])

    # Create directory if doesn't exist
    __NEURALSPACE_HOME.mkdir(parents=True, exist_ok=True)
    return __NEURALSPACE_HOME


def neuralspace_url() -> Text:
    global __NEURALSPACE_URL

    if NEURALSPACE_URL_ENV_VAR in os.environ:
        __NEURALSPACE_URL = os.environ[NEURALSPACE_URL_ENV_VAR]

    return __NEURALSPACE_URL


def auth_path() -> Path:
    return neuralspace_home() / "auth.json"


# FILE KEYS IN csv
NLU_FILE = "nlu.csv"
SYNONYMS_FILE = "synonym.csv"
REGEX_FILE = "regex.csv"
LOOKUP_FILE = "lookup.csv"

# KEYS
METADATA = "metadata"
SUCCESS = "success"
NEURALSPACE_HOME = "neuralspaceHome"
DESCRIPTION = "description"
PROJECT_ID = "projectId"
LANGUAGE = "language"
LANGUAGES = "languages"
TYPE = "type"
EXAMPLE = "example"
VALUE = "value"
START_INDEX = "start_idx"
END_INDEX = "end_idx"
TIME = "time"
FROM = "from"
TO = "to"
AUTHORIZATION = "Authorization"
PROJECT_NAME = "projectName"
SEARCH = "search"
PAGE_NUMBER = "pageNumber"
PAGE_SIZE = "pageSize"
DATA = "data"
DELETED = "deleted"
NOT_FOUND = "notFound"
PROJECTS = "projects"
NUMBER_OF_EXAMPLES = "noOfExamples"
NUMBER_OF_INTENTS = "noOfIntents"
NUMBER_OF_MODELS = "noOfModels"
FILTER = "filter"
PREPARED = "prepared"
COUNT = "count"
CREATED_AT = "createdAt"
ENTITIES = "entities"
INTENT = "intent"
EXAMPLE_ID = "exampleId"
ENTITY_ID = "entityId"
TEXT = "text"
EXAMPLES = "examples"
MODEL_NAME = "modelName"
MODEL_ID_key = "model_id"
MODEL_ID = "modelId"
MODEL_IDS = "modelIDs"
TRAINING_STATUS = "trainingStatus"
DEPLOYED_STATUS = "deploymentStatus"
COMPLETED = "Completed"
DEPLOYED = "Deployed"
TRAINING = "Training"
FAILED = "Failed"
TIMED_OUT = "Timed Out"
DEAD = "Dead"
INITIATED = "Initiated"
QUEUED = "Queued"
SAVED = "Saved"
REPLICAS = "replicas"
METRICS = "metrics"
INTENT_CLASSIFIER_METRICS = "intentClassifierPerformance"
INTENT_ACCURACY = "i_acc"
NER_METRICS = "nerPerformance"
ENTITY_PARTIAL_F1 = "e_f1_partial"
TRAINING_TIME = "trainingTime"
ENTITY = "entity"
MESSAGE = "message"
MODELS = "models"
N_REPLICAS = "nReplicas"
LAST_STATUS_UPDATED = "lastStatusUpdateAt"
PARSED_RESPONSE = "parsedResponse"
OUTPUT = "output"
START_INDEX = "start_idx"
END_INDEX = "end_idx"
TIME = "time"
FROM = "from"
TO = "to"
VALUE = "value"
KEY_ID = "id"
KEY_KEY = "key"
YES = "Yes"
NO = "No"
ENTITY_TYPE = "entityType"
PRE_TRAINED = "pre-trained"
LOOKUP = "lookup"
SYNONYM = "synonym"
REGEX = "regex"
NAME = "name"
PATTERN = "pattern"
ELEMENTS = "elements"
ENTITY_SYNONYMS = "entity_synonyms"
LOOKUP_TABLES = "lookup_tables"
REGEX_FEATURES = "regex_features"
COMMON_EXAMPLES = "common_examples"
SYNONYMS = "synonyms"
TRANSLATED_TEXT = "translated_text"
TRANSLITERATED_TEXT = "transliterated_text"
SUGGESTIONS = "suggestions"
DETECTED_LANGUAGES = "detected_languages"
AUGMENTATION_SUGGESTIONS = "augmentation_suggestions"
APP_TYPE = "appType"
CODE = "code"
END = "end"
START = "start"
CONFIDENCE = "confidence"
INTENT_RANKING = "intent_ranking"
NO_OF_TRAINING_JOBS = "noOfTrainingJob"
# supported entity types
NER_TYPES = [PRE_TRAINED, LOOKUP, SYNONYM, REGEX]
USER_DEFINED_ENTITY_TYPES = [LOOKUP, SYNONYM, REGEX]
TRAIN = "train"
TEST = "test"


# Follow up Commands
CREATE_PROJECT_COMMAND = "neuralspace nlu create-project --help"
UPLOAD_DATASET_COMMAND = "neuralspace nlu upload-dataset --help"
INSTALL_APP_COMMAND = "neuralspace install-app --help"
TRAIN_MODEL_COMMAND = "neuralspace nlu train --help"
DEPLOY_MODEL_COMMAND = "neuralspace nlu deploy --help"
PARSE_MODEL_COMMAND = "neuralspace nlu parse --help"
STATUS_MODEL_COMMAND = "neuralspace nlu model-status --help"
LIST_MODELS_COMMAND = "neuralspace nlu list-models --help"
# checking command

APP_IS_INSTALLED = "App is already installed"

# URLS
LIST_ENTITY_URL = "api/nlu/v1/list/entity"
PLATFORM_URL = "https://ns-platform-staging.uksouth.cloudapp.azure.com/#/platform/nlu/"

# emojis
BOOK = "📚"
FAST_FORWARD = "⏩"
CROSS = "❌"
SAD_SMILEY = "😔"
GREEN_TICK = "✅"
BIN = "🗑️"
NUMBERS_IN_SQUARE = "🔢"
DOWN_ARROW = "⬇️"
PEN_AND_PAPER = "📝"
ARROW_UP = "⤴"
PERSON_STANDING = "🧍"
PERSON_DUMBELL = "🏋"
SAND_CLOCK = "⏳"
WRITING = "✍️"
PIN = "📌"
SOUP = "🍲"
OM = "🕉️"
HASH = "#️⃣"
FINGER_RIGHT = "👉️"
PERSON_TAKING = "🗣️"
PERSON_HERE = "💁"
KEY = "🗝"
DOOR = "🚪"
ROCKET = "🚀"
BAG = "👜"

# COLORS
RED_START = "[red]"
RED_END = "[/red]"
ORANGE_START = "[orange]"
ORANGE_END = "[/orange]"
ORANGE3_START = "[orange3]"
ORANGE3_END = "[/orange3]"
DARK_ORANGE_START = "[dark_orange3]"
DARK_ORANGE_END = "[/dark_orange3]"
INFO = "[deep_sky_blue2]INFO[/deep_sky_blue2]"
BOLD_START = "[bold]"
BOLD_END = "[/bold]"
GREEN_START = "[green]"
GREEN_END = "[/green]"
LOGO_HASH = ""
ERROR = f"{RED_START}ERROR{RED_END}"

# Rasa
KEY_PROJECT_ID = "project_id"
KEY_PROJECT_IDS = "project_ids"
KEY_MODEL_IDS = "model_ids"
KEY_MODEL_ID = "model_id"
COMPONENT_CONFIG = "component_config"
KEY_PROJECT_DETAILS = "project_details"
KEY_PATH_TO_PROJECT_ID = "project_path"
KEY_RASA = "rasa"
NS_RASA_METADATA_FILE = "metadata.json"
KEY_DATA = "data"
KEY_AUTH = "auth"
KEY_REPLICAS = "replicas"
ENTITY_KEY_DELEMETER = "$$$###"
EXAMPLES_FILE = "examples.json"
ENTITIES_FILE = "entities.json"
PIPELINE = "pipeline"
COMPONENT_CLASS = "neuralspace.components.rasa.neuralspace.NeuralSpaceNLP"


# PROGRESS BAR
class CustomisedTransferSpeedColumn(TransferSpeedColumn):
    def render(self, task: Task) -> Text_render:
        """Show data transfer speed."""
        speed = task.finished_speed or task.speed
        if speed is None:
            return Text_render("?", style="progress.data.speed")
        return Text_render(f"{speed: .2f} examples/s", style="progress.data.speed")


progress_bar = Progress(
    SpinnerColumn(),
    TextColumn(
        "[orange3]Uploading...[/orange3]"
        " [dark_green]{task.completed}[/dark_green]/[dark_green]{task.total}[/dark_green]"
    ),
    BarColumn(bar_width=50),
    "[progress.percentage]{task.percentage:>3.0f}%",
    TimeRemainingColumn(),
    CustomisedTransferSpeedColumn(),
    "[orange3][progress.description]{task.description}[/orange3]",
)
