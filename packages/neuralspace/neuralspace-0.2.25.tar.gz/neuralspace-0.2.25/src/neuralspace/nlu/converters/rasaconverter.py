from pathlib import Path
from typing import Any, Dict, List, Optional, Text

from neuralspace.constants import (
    ELEMENTS,
    ENTITIES,
    ENTITY,
    ENTITY_TYPE,
    EXAMPLES,
    INTENT,
    LANGUAGE,
    LOOKUP,
    NAME,
    PATTERN,
    REGEX,
    SYNONYM,
)
from neuralspace.datamodels import DatasetType
from neuralspace.nlu.converters.base import DataConverter
from neuralspace.nlu.converters.rasa.training_data.training_data import TrainingData
from neuralspace.nlu.utils import (
    auto_tag_lookup,
    auto_tag_pretrained_entities,
    auto_tag_regex,
    map_entities,
    remove_entity_duplicates,
    remove_nlu_duplicates,
)


class RasaConverter(DataConverter):
    def __init__(
        self,
        language: Text,
        entity_mapping: Optional[Dict[Text, Text]],
        auto_tag_entities: bool,
    ):
        self.nlu_data = []
        self.lookup_data = []
        self.regex_data = []
        self.synonym_data = []
        self.language = language
        self.entity_mapping = entity_mapping
        self.auto_tag_entities = auto_tag_entities
        self.number_of_nlu_examples_before_duplicate_check = 0
        self.number_of_nlu_examples_after_duplicate_check = 0

    @property
    def all_entity_types(self) -> List[Text]:
        all_entities = []
        all_entities += [entity[ENTITY] for entity in self.lookup_data]
        all_entities += [entity[ENTITY] for entity in self.regex_data]
        all_entities += [entity[ENTITY] for entity in self.synonym_data]
        all_nlu_entities = []
        for example in self.nlu_data:
            if ENTITIES in example:
                for entity in example[ENTITIES]:
                    all_nlu_entities.append(entity[ENTITY])
        all_entities += list(set(all_nlu_entities))
        return list(set(all_nlu_entities))

    def __lookup_converter(
        self, entities: List[Dict[Text, Any]]
    ) -> List[Dict[Text, Any]]:
        formatted_lookup_entities = []
        for lookup_entity in entities:
            entity = {
                ENTITY: lookup_entity[NAME],
                EXAMPLES: lookup_entity[ELEMENTS],
                LANGUAGE: self.language,
                ENTITY_TYPE: LOOKUP,
            }
            formatted_lookup_entities.append(entity)
        return formatted_lookup_entities

    def __regex_converter(
        self, entities: List[Dict[Text, Any]]
    ) -> List[Dict[Text, Any]]:
        """
        Rasa's format -> [{‘name’: ‘help’, ‘pattern’: ‘\\bhelp\\b’}, {‘name’: ‘help’, ‘pattern’: ‘\\df’}]
        NeuralSpace format ->
        {
            "entity": "entity-name",
            "examples": [],
            "language": "language-code",
            "entityType": "regex"
        }
        """
        all_regexes = {}
        for regex_entity in entities:
            if regex_entity[NAME] not in all_regexes:
                all_regexes[regex_entity[NAME]] = {
                    ENTITY: regex_entity[NAME],
                    EXAMPLES: [regex_entity[PATTERN]],
                    LANGUAGE: self.language,
                    ENTITY_TYPE: REGEX,
                }
            else:
                all_regexes[regex_entity[NAME]][EXAMPLES].append(regex_entity[PATTERN])
        return list(all_regexes.values())

    def __synonym_converter(self, synonyms: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Rasa's format -> {'super': 'good', 'great': 'good', 'done good': 'good'}
        Note that in rasa's format the value in teh dictionary is the actual name of the synonym entity

        NeuralSpace format ->
        {
            "entity": "synonym-name",
            "examples": [],
            "language": "language-code",
            "entityType": "synonyms"
        }
        """
        formatted_synonyms = {}
        for synonym, entity_name in synonyms.items():
            if entity_name not in formatted_synonyms:
                formatted_synonyms[entity_name] = {
                    ENTITY: entity_name,
                    EXAMPLES: [synonym],
                    LANGUAGE: self.language,
                    ENTITY_TYPE: SYNONYM,
                }
            else:
                formatted_synonyms[entity_name][EXAMPLES].append(synonym)
        return list(formatted_synonyms.values())

    @staticmethod
    def __nlu_data_converter(
        dataset: TrainingData,
    ):
        formatted_nlu_data = []
        for example in dataset.nlu_examples:
            formatted_nlu_data.append(example.as_dict())
        return formatted_nlu_data

    def number_of_unique_intent(self):
        return len(set([example[INTENT] for example in self.nlu_data]))

    def post_process(
        self,
        dataset_type,
        output_directory,
        authtoken: Text = None,
        dataset_id: Text = None,
    ):
        if self.entity_mapping:
            self.nlu_data = map_entities(self.nlu_data, self.entity_mapping)
        if self.auto_tag_entities:
            self.nlu_data = auto_tag_pretrained_entities(
                self.nlu_data, self.language, authtoken=authtoken
            )
            self.nlu_data = auto_tag_lookup(self.nlu_data, self.lookup_data)
            self.nlu_data = auto_tag_regex(self.nlu_data, self.regex_data)
        self.number_of_nlu_examples_before_duplicate_check = self.count(self.nlu_data)
        self.nlu_data = remove_nlu_duplicates(self.nlu_data)
        self.number_of_nlu_examples_after_duplicate_check = self.count(self.nlu_data)
        self.lookup_data = remove_entity_duplicates(
            remove_nlu_duplicates(self.lookup_data)
        )
        self.regex_data = remove_entity_duplicates(
            remove_nlu_duplicates(self.regex_data)
        )
        self.synonym_data = remove_entity_duplicates(
            remove_nlu_duplicates(self.synonym_data)
        )
        self.set_data_type(dataset_type)
        self.save_converted_data(
            output_directory=output_directory,
            nlu_data=self.nlu_data,
            lookup_data=self.lookup_data,
            synonym_data=self.synonym_data,
            regex_data=self.regex_data,
            dataset_id=dataset_id,
        )

    def convert(
        self,
        input_path: List[Path],
        output_directory: Path,
        dataset_type: DatasetType,
        authtoken: Text = None,
        dataset_id: Text = None,
    ):
        from neuralspace.nlu.converters.rasa.shared.importers.utils import (
            training_data_from_paths,
        )

        for single_path in input_path:
            data: TrainingData = training_data_from_paths(
                [str(single_path)], language=self.language
            )
            self.nlu_data += self.__nlu_data_converter(data)
            self.lookup_data += self.__lookup_converter(data.lookup_tables)
            self.regex_data += self.__regex_converter(data.regex_features)
            self.synonym_data += self.__synonym_converter(data.entity_synonyms)

        self.post_process(
            dataset_type=dataset_type,
            output_directory=output_directory,
            authtoken=authtoken,
            dataset_id=dataset_id,
        )

    def component_convert(self, training_data: TrainingData, dataset_type: DatasetType):
        self.nlu_data += self.__nlu_data_converter(training_data)
        self.lookup_data += self.__lookup_converter(training_data.lookup_tables)
        self.regex_data += self.__regex_converter(training_data.regex_features)
        self.synonym_data += self.__synonym_converter(training_data.entity_synonyms)

        if self.entity_mapping:
            self.nlu_data = map_entities(self.nlu_data, self.entity_mapping)

        if self.auto_tag_entities:
            self.nlu_data = auto_tag_pretrained_entities(self.nlu_data, self.language)
            self.nlu_data = auto_tag_lookup(self.nlu_data, self.lookup_data)
            self.nlu_data = auto_tag_regex(self.nlu_data, self.regex_data)

        self.set_data_type(dataset_type)
        self.nlu_data = remove_nlu_duplicates(self.nlu_data)
        self.lookup_data = remove_entity_duplicates(
            remove_nlu_duplicates(self.lookup_data)
        )
        self.regex_data = remove_entity_duplicates(
            remove_nlu_duplicates(self.regex_data)
        )
        self.synonym_data = remove_entity_duplicates(
            remove_nlu_duplicates(self.synonym_data)
        )
