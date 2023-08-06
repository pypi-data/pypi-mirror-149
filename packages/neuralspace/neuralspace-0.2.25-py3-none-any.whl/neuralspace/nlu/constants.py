LANGUAGE_CATALOG_URL = "api/nlu/v1/supported-languages"
CREATE_EXAMPLE_URL = "api/nlu/v1/single/example"
CREATE_PROJECT_URL = "api/nlu/v1/project"
LIST_PROJECTS_URL = "api/nlu/v1/list/projects"
LIST_EXAMPLES_URL = "api/nlu/v1/list/example"
DELETE_EXAMPLE_URL = "api/nlu/v1/single/example"
DELETE_PROJECT_URL = "api/nlu/v1/single/project"
TRAIN_MODEL_URL = "api/nlu/v1/model/train/queue"
SINGLE_MODEL_DETAILS_URL = "api/nlu/v1/model"
LIST_MODELS_URL = "api/nlu/v1/list/model"
DEPLOY_MODEL_URL = "api/nlu/v1/model/deploy"
DELETE_MODELS_URL = "api/nlu/v1/model"
PARSE_URL = "api/nlu/v1/model/parse"
CREATE_ENTITY_URL = "api/nlu/v1/entity"
DELETE_ENTITY_URL = "api/nlu/v1/entity"
ADD_ENTITY_EXAMPLES_URL = "api/nlu/v1/add/examples/entity"
DELETE_ENTITY_EXAMPLES_URL = "api/nlu/v1/remove/examples/entity"
DELETE_MULTIPLE_PROJECT_URL = "api/nlu/v1/project"
ADD_SYNONYMS_TO_THE_PROJECT_URL = "api/nlu/v1/project/add/synonym"
LIST_SYNONYMS_IN_THE_PROJECT_URL = "api/nlu/v1/project/list/synonym"


TRAINING_PROGRESS = [
    "Initiated",
    "Queued",
    "Preparing Data",
    "Data Prepared",
    "Pipeline Building",
    "Pipeline Built",
    "Training",
    "Trained",
    "Saved",
    "Completed",
]

SUPPORTED_LANGUAGES = [
    "eu",
    "be",
    "ca",
    "hr",
    "cs",
    "et",
    "gl",
    "hu",
    "ga",
    "la",
    "lv",
    "sr",
    "sk",
    "sl",
    "bg",
    "hy",
    "tr",
    "uk",
    "he",
    "kk",
    "mt",
    "ug",
    "fi",
    "sv",
    "id",
    "ko",
    "vi",
    "af",
    "hi",
    "bn",
    "te",
    "ta",
    "mr",
    "ur",
    "gu",
    "kn",
    "ml",
    "as",
    "pa",
    "fa",
    "ar",
    "acm",
    "afb",
    "akw",
    "ama",
    "apc",
    "apd",
    "arz",
    "el",
    "da",
    "en",
    "nb",
    "zh",
    "nl",
    "fr",
    "de",
    "it",
    "ja",
    "lt",
    "pl",
    "pt",
    "ro",
    "ru",
    "es",
    "sq",
    "an",
    "az",
    "ba",
    "bs",
    "br",
    "my",
    "ce",
    "cv",
    "ka",
    "ht",
    "is",
    "io",
    "jv",
    "ky",
    "lb",
    "mk",
    "mg",
    "ms",
    "ne",
    "oc",
    "su",
    "sw",
    "tl",
    "tg",
    "tt",
    "uz",
    "vo",
    "cy",
    "yo",
    "multilingual",
]

# Training status colour codes
C_INITIATED = "⚪"
C_QUEUED = "🔵"
C_COMPLETED = "🟢"
C_TRAINING = "🟠"
C_FAILED = "🔴"
C_TIMED_OUT = "🟤"
C_DEAD = "⚫"

# DEFAULT VALUES
DEFAULT_RASA_TRAINING_JOBS = 1
