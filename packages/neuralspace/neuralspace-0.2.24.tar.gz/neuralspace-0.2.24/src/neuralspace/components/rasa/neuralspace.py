import json
import logging
import os
import typing
from copy import copy
from typing import Any, Dict, List, Optional, Text

import rasa.shared.utils.io
import rasa.utils.train_utils
from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import track

from neuralspace.components.rasa.utils import (
    get_metadata,
    get_project_id_if_exists,
    get_recent_model_id,
    print_table_description_for_examples,
    update_metadata,
)
from neuralspace.constants import (
    COMPONENT_CLASS,
    CROSS,
    DATA,
    ENTITIES,
    ENTITY,
    ENTITY_ID,
    ENTITY_KEY_DELEMETER,
    ENTITY_TYPE,
    ERROR,
    EXAMPLE_ID,
    EXAMPLES,
    FAILED,
    GREEN_END,
    GREEN_START,
    INFO,
    INTENT,
    INTENT_RANKING,
    KEY_AUTH,
    KEY_DATA,
    KEY_ID,
    KEY_KEY,
    KEY_MODEL_ID,
    KEY_MODEL_IDS,
    KEY_PATH_TO_PROJECT_ID,
    KEY_PROJECT_DETAILS,
    KEY_PROJECT_ID,
    KEY_PROJECT_IDS,
    LANGUAGE,
    NEURALSPACE_HOME,
    PIPELINE,
    PLATFORM_URL,
    RED_END,
    RED_START,
    SAD_SMILEY,
    SUCCESS,
    SYNONYM,
    TEXT,
    TRAINING_STATUS,
    auth_path,
    neuralspace_home,
)
from neuralspace.datamodels import DatasetTypes
from neuralspace.language_detection.apis import get_language_detection_response_sync
from neuralspace.nlu.apis import (
    add_entity_examples_sync,
    add_synonym_to_project_sync,
    delete_entity_examples_sync,
    delete_entity_sync,
    delete_examples_sync,
    deploy_sync,
    get_uploaded_entities,
    get_uploaded_examples,
    list_all_entity_sync,
    parse_sync,
    start_training,
    update_entities,
    update_examples,
    upload_entity_sync,
    upload_example_sync,
    wait_till_deploy_completes_sync,
    wait_till_training_completes_sync,
)
from neuralspace.nlu.converters.rasaconverter import RasaConverter
from neuralspace.translation.apis import get_translation_response_sync
from neuralspace.utils import is_success_status

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)
console = Console()

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class NsModelTrainingError(Exception):
    pass


class NsEntityUploadException(Exception):
    pass


class NeuralSpaceNLP(Component):
    """The core component that links spaCy to related components in the pipeline."""

    WAIT_INTERVAL = "wait_interval"
    CASE_SENSITIVE = "case_sensitive"
    AUTO_TAG_ENTITIES = "auto_tag_entities"
    ENTITY_MAPPING = "entity_mapping"
    TIMEOUT_IN_MINS = "timeout_in_mins"
    FORCE_TRAIN = "force_train"
    MULTILINGUAL = "multilingual"
    MODEL_ID = "model_id"
    USE_EXISTING_ENTITIES = "use_existing_entities"

    defaults = {
        # when retrieving word vectors, this will decide if the casing
        # of the word is relevant. E.g. `hello` and `Hello` will
        # retrieve the same vector, if set to `False`. For some
        # applications and models it makes sense to differentiate
        # between these two words, therefore setting this to `True`.
        CASE_SENSITIVE: False,
        WAIT_INTERVAL: 2,
        AUTO_TAG_ENTITIES: False,
        ENTITY_MAPPING: {},
        TIMEOUT_IN_MINS: 5,
        FORCE_TRAIN: False,
        MULTILINGUAL: False,
        MODEL_ID: None,
        USE_EXISTING_ENTITIES: True,
    }

    def __init__(
        self,
        project_id: Text = None,
        language: Text = None,
        component_config: Dict[Text, Any] = None,
        model_id=None,
    ):
        self.project_id = project_id
        self.language = language
        self.component_config = component_config if component_config is not None else {}
        self.component_config[LANGUAGE] = self.language
        self.model_id = model_id
        self.check_neuralspace_login()
        self.is_deployed = False
        self.is_trained = False
        self.existing_examples = {}
        self.existing_entities = {}
        self.total_uploaded_examples = 0
        self.total_uploaded_entities = 0
        self.total_removed_examples = 0
        self.total_removed_entities = 0
        self.total_removed_entities_example = 0
        self.total_uploaded_entities_example = 0
        self.multilingual = self.component_config.get(self.MULTILINGUAL)
        self.existing_entities_in_platform = list_all_entity_sync(self.language)
        super().__init__(component_config)

    @classmethod
    def load_model(cls):
        console.print("loading model")

    def check_neuralspace_login(self):
        ns_auth_json = auth_path()
        self.component_config[NEURALSPACE_HOME] = str(neuralspace_home())
        if not os.path.exists(ns_auth_json):
            raise Exception(
                "Please log into neuralspace cli by installing it with"
                "`pip install neuralspace` and `neuralspace login -e <email> -p <password>"
            )
        with open(ns_auth_json) as f:
            auth_params = json.load(f)
        if KEY_DATA not in auth_params:
            raise Exception("Please login in neuralspace cli")
        if KEY_AUTH not in auth_params.get("data"):
            raise Exception(
                "Corrupt auth.json file. Please reinstall and login into neuralspace cli"
            )

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["neuralspace"]

    @classmethod
    def create(
        cls, component_config: Dict[Text, Any], config: RasaNLUModelConfig
    ) -> "NeuralSpaceNLP":
        working_directory = os.getcwd()
        component_config[KEY_PROJECT_ID] = component_config.get(
            KEY_PROJECT_ID,
            get_project_id_if_exists(
                working_directory=working_directory,
                create_if_doesnt_exist=True,
                language=config[LANGUAGE],
            ),
        )
        console.print(f"Using project ID: {component_config[KEY_PROJECT_ID]}")

        component_config = rasa.utils.train_utils.override_defaults(
            cls.defaults, component_config
        )
        language = config[LANGUAGE]
        metadata = get_metadata()
        metadata[KEY_PROJECT_IDS].append(component_config[KEY_PROJECT_ID])
        if component_config[KEY_PROJECT_ID] not in metadata[KEY_PROJECT_DETAILS].keys():
            metadata[KEY_PROJECT_DETAILS][component_config[KEY_PROJECT_ID]] = {
                KEY_MODEL_IDS: [],
                LANGUAGE: language,
            }
        metadata[KEY_PATH_TO_PROJECT_ID][working_directory] = component_config[
            KEY_PROJECT_ID
        ]
        update_metadata(metadata)
        return cls(
            component_config[KEY_PROJECT_ID],
            language,
            component_config,
            model_id=component_config[KEY_MODEL_ID],
        )

    @property
    def get_existing_examples(self) -> Dict[Text, Dict[Text, Any]]:
        return get_uploaded_examples(self.project_id)

    @property
    def get_existing_entities(
        self,
    ) -> Dict[Text, Dict[Text, Any]]:
        return get_uploaded_entities(self.project_id)

    def __get_unique_entity_key(self, entity: Dict[Text, Any]) -> Text:
        return f"{entity[ENTITY]}{ENTITY_KEY_DELEMETER}{entity[ENTITY_TYPE]}{ENTITY_KEY_DELEMETER}{entity[LANGUAGE]}"

    def manage_adding_existing_entities(
        self,
        existing_entity: Dict[Text, Any],
        new_entity: Dict[Text, Any],
        entity_id: Text,
    ):
        examples_to_delete = list(
            set(existing_entity[EXAMPLES]) - set(new_entity[EXAMPLES])
        )
        examples_to_add = list(
            set(existing_entity[EXAMPLES]) - set(new_entity[EXAMPLES])
        )

        logger.debug(f"new entity: {new_entity}")
        logger.debug(f"Entity examples to delete: {examples_to_delete}")
        logger.debug(f"Entity examples to add: {examples_to_add}")

        if examples_to_delete:
            response = delete_entity_examples_sync(entity_id, examples_to_delete)
            self.total_removed_entities_example += 1
            if not response[SUCCESS]:
                raise Exception(
                    f"Could not delete entity examples {examples_to_delete} with id: {entity_id}"
                )
        if examples_to_add:
            response = add_entity_examples_sync(entity_id, examples_to_add)
            self.total_uploaded_entities_example += 1
            if not response[SUCCESS]:
                raise Exception(
                    f"Could not add entity examples {examples_to_delete} with id: {entity_id}"
                )

    def sync_entities(self, entity_data: List[Dict[Text, Any]]):  # noqa : C901
        self.existing_entities_in_platform = list_all_entity_sync(self.language)
        existing_entities = self.get_existing_entities
        unique_entity_keys = [
            f"{self.__get_unique_entity_key(entity)}" for entity in entity_data
        ]
        unique_existing_entity_keys = [
            {"id": id, "key": f"{self.__get_unique_entity_key(entity)}"}
            for id, entity in existing_entities.items()
        ]
        logger.debug(f"existing_entities: {existing_entities}")
        logger.debug(f"entity_data: {entity_data}")
        logger.debug(f"unique_entity_keys: {unique_entity_keys}")
        # Delete examples that were removed or updated from the dataset
        for entity in unique_existing_entity_keys:
            entity_id, entity_key = entity[KEY_ID], entity[KEY_KEY]
            if entity_key not in unique_entity_keys:
                self.total_removed_entities += 1
                delete_entity_sync(entity_id)
                existing_entities.pop(entity_id)
                update_entities(existing_entities.copy(), self.project_id)

        for entity_id, existing_entity in existing_entities.items():
            new_entity = entity_data[
                unique_entity_keys.index(self.__get_unique_entity_key(existing_entity))
            ]
            self.manage_adding_existing_entities(
                existing_entity=existing_entity,
                new_entity=new_entity,
                entity_id=entity_id,
            )
            existing_entities[entity_id] = new_entity
            update_entities(existing_entities.copy(), self.project_id)
        for entity in entity_data:

            logger.debug(f"Ready to upload: {entity}")
            if entity not in existing_entities.values():
                if (
                    self.component_config[self.USE_EXISTING_ENTITIES]
                    and entity[ENTITY]
                    in self.existing_entities_in_platform[entity[ENTITY_TYPE]]
                ):
                    self.manage_adding_existing_entities(
                        existing_entity=self.existing_entities_in_platform[
                            entity[ENTITY_TYPE]
                        ][entity[ENTITY]],
                        new_entity=entity,
                        entity_id=self.existing_entities_in_platform[
                            entity[ENTITY_TYPE]
                        ][entity[ENTITY]][ENTITY_ID],
                    )

                    logger.debug(f"Found Existing entity: {entity}")
                    if entity[ENTITY_TYPE] == SYNONYM:
                        add_synonym_to_project_sync(
                            project_id=self.project_id,
                            language=self.language,
                            entity_id=self.existing_entities_in_platform[
                                entity[ENTITY_TYPE]
                            ][entity[ENTITY]][ENTITY_ID],
                        )
                    existing_entities[
                        self.existing_entities_in_platform[entity[ENTITY_TYPE]][
                            entity[ENTITY]
                        ][ENTITY_ID]
                    ] = entity
                    self.total_uploaded_entities += 1
                    update_entities(existing_entities, self.project_id)
                else:
                    result = upload_entity_sync(entity)
                    self.total_uploaded_entities += 1
                    if is_success_status(result.status_code):
                        logger.debug(f"uploaded entity: {entity}")
                        result = result.json()
                        if entity[ENTITY_TYPE] == SYNONYM:
                            add_synonym_to_project_sync(
                                project_id=self.project_id,
                                language=self.language,
                                entity_id=result[DATA][ENTITY_ID],
                            )
                        existing_entities[result[DATA].get(ENTITY_ID)] = entity
                        update_entities(existing_entities, self.project_id)
                    else:
                        json_response = result.json()
                        raise NsEntityUploadException(
                            f"> {CROSS} Failed to add entity {SAD_SMILEY}: "
                            f" {json_response['message']}"
                        )
        update_entities(existing_entities, self.project_id)
        self.existing_entities = existing_entities

    def sync_examples(self, nlu_examples: List[Dict[Text, Any]]):
        existing_examples = self.get_existing_examples

        # Delete examples that were removed or updated from the dataset
        for example_id, example in copy(existing_examples).items():
            if example not in nlu_examples:
                self.total_removed_examples += 1
                delete_examples_sync(example_id)
                existing_examples.pop(example_id)
                update_examples(existing_examples, self.project_id)

        console.print(f"> {INFO} Uploading Examples to project ID: {self.project_id}")
        for example in track(nlu_examples, description="Uploading..."):
            if example not in existing_examples.values():
                self.total_uploaded_examples += 1
                result = upload_example_sync(example, self.project_id, self.language)
                json_response = result.json()
                if json_response[SUCCESS]:
                    existing_examples[json_response[DATA].get(EXAMPLE_ID)] = example
                    update_examples(existing_examples, self.project_id)
                else:
                    raise Exception(
                        f"> {ERROR} {CROSS} Failed to add entity examples {SAD_SMILEY}: "
                        f"{RED_START}{json_response['message']}{RED_END} "
                    )
        update_examples(existing_examples, self.project_id)
        self.existing_examples = existing_examples

    def convert(
        self,
        config: Optional[RasaNLUModelConfig],
        training_data: TrainingData,
    ) -> RasaConverter:
        converter = RasaConverter(
            language=config.get(LANGUAGE),
            entity_mapping=self.component_config[self.ENTITY_MAPPING],
            auto_tag_entities=self.component_config[self.AUTO_TAG_ENTITIES],
        )
        converter.component_convert(
            training_data=training_data, dataset_type=DatasetTypes.TRAIN.value
        )
        return converter

    def upload_examples(self, converter: RasaConverter) -> None:
        self.sync_examples(converter.nlu_data)
        self.sync_entities(
            converter.synonym_data + converter.lookup_data + converter.regex_data
        )

    @property
    def can_train_new_model(self):
        return (
            self.total_removed_examples
            + self.total_uploaded_examples
            + self.total_uploaded_entities
            + self.total_uploaded_entities_example
            + self.total_removed_entities_example
            + self.total_removed_entities
        ) > 0 or self.component_config[self.FORCE_TRAIN]

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        ns_rasa_metadata = get_metadata()

        # convert dataset from rasa format to NS format.
        converter = self.convert(config, training_data)
        # upload the example that has not been uploaded yet.
        self.upload_examples(converter)
        # start the training process
        if not self.model_id and self.can_train_new_model:
            training_response = start_training(self.project_id, self.language)

            self.model_id = training_response[KEY_DATA][0]
            self.component_config[KEY_MODEL_ID] = self.model_id

            # Will wait till the training process ends
            wait_interval = self.component_config.get(self.WAIT_INTERVAL)

            final_training_response = wait_till_training_completes_sync(
                self.model_id, wait_interval=int(wait_interval)
            )
            status = final_training_response[KEY_DATA].get(TRAINING_STATUS)
            if status != FAILED:
                self.is_trained = True
                # un-deploy the previous model
                if (
                    self.project_id in ns_rasa_metadata[KEY_PROJECT_DETAILS]
                    and ns_rasa_metadata[KEY_PROJECT_DETAILS][self.project_id][
                        KEY_MODEL_IDS
                    ]
                ):
                    if ns_rasa_metadata[KEY_PROJECT_DETAILS][self.project_id][
                        KEY_MODEL_IDS
                    ]:
                        json_response = deploy_sync(
                            ns_rasa_metadata[KEY_PROJECT_DETAILS][self.project_id][
                                KEY_MODEL_IDS
                            ][-1],
                            n_replicas=0,
                        )
                        if json_response[DATA]:
                            wait_till_deploy_completes_sync(
                                ns_rasa_metadata[KEY_PROJECT_DETAILS][self.project_id][
                                    KEY_MODEL_IDS
                                ][-1],
                                wait_interval=wait_interval,
                                timeout_in_mins=self.component_config.get(
                                    self.TIMEOUT_IN_MINS
                                ),
                                check_n_replicas=0,
                            )
                # deploy the current model
                deploy_sync(self.model_id, n_replicas=1)
                deploy_response = wait_till_deploy_completes_sync(
                    self.model_id,
                    wait_interval=wait_interval,
                    timeout_in_mins=self.component_config.get(self.TIMEOUT_IN_MINS),
                )
                if deploy_response[SUCCESS]:
                    self.is_deployed = True
                else:
                    console.print(
                        f"> {ERROR} Model deployment is failed. You can always manually deploy models from "
                        f"{PLATFORM_URL}{self.project_id}/{self.language}/details"
                    )
            else:
                console.print(f"> {ERROR} Failed to fetch model details")
                console.print(
                    f'''> Reason for failure {SAD_SMILEY}: {RED_START}
                    {final_training_response['message']}{RED_END} "'''
                )
                raise NsModelTrainingError(
                    f"Model training failed: {final_training_response['message']}"
                )
        else:
            if not self.model_id:
                self.model_id = get_recent_model_id(self.project_id)
            console.print(
                f"{GREEN_START}Don't need to retrain the model. Because, There is no change in your data{GREEN_END}"
            )

    def process(self, message: Message, **kwargs: Any) -> Message:
        text = message.data.get(TEXT)
        if text:
            if self.multilingual:
                text_language = get_language_detection_response_sync(text=text)
                if not text_language == "en":
                    if text_language is None:
                        text_language = "en"
                    text = get_translation_response_sync(
                        text=text, src_language=text_language, tgt_language="en"
                    )
            response = parse_sync(self.model_id, text)
            if response[DATA]:
                print(response)
                message.set(INTENT, response[DATA][INTENT], add_to_output=True)
                message.set(
                    INTENT_RANKING,
                    response[DATA][INTENT_RANKING],
                    add_to_output=True,
                )
                message.set(ENTITIES, response[DATA][ENTITIES], add_to_output=True)
        return message

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["NeuralSpaceNLP"] = None,
        **kwargs: Any,
    ) -> "NeuralSpaceNLP":
        """Loads trained component (see parent class for full docstring)."""
        if cached_component:
            return cached_component

        component_index = model_metadata.component_classes.index(COMPONENT_CLASS)

        console.print(
            f"Loading Neuralspace model: {model_metadata.metadata[PIPELINE][int(component_index)][KEY_MODEL_ID]}"
        )
        return cls(
            project_id=model_metadata.get(KEY_PROJECT_ID),
            language=model_metadata.get(LANGUAGE),
            component_config=model_metadata.metadata[PIPELINE][int(component_index)],
            model_id=model_metadata.metadata[PIPELINE][int(component_index)][
                KEY_MODEL_ID
            ],
        )

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        metadata = get_metadata()
        metadata[KEY_PROJECT_DETAILS][self.project_id][KEY_MODEL_IDS].append(
            self.model_id
        )
        update_metadata(metadata)
        model_metadata = {
            "project_id": self.project_id,
            "language": self.language,
            "component_config": dict(self.component_config),
            "model_id": self.model_id,
        }
        table = print_table_description_for_examples(
            total_uploaded_examples=self.total_uploaded_examples,
            total_removed_examples=self.total_removed_examples,
            total_removed_entities_examples=self.total_removed_entities_example,
            total_uploaded_entities_examples=self.total_uploaded_entities_example,
            total_removed_entities=self.total_removed_entities,
            total_uploaded_entities=self.total_uploaded_entities,
        )
        console.print(table)
        return model_metadata
