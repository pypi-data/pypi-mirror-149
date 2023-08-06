import json
from pathlib import Path
from typing import Any, Dict, List, Text

from neuralspace.constants import (
    COMMON_EXAMPLES,
    ELEMENTS,
    ENTITY,
    ENTITY_SYNONYMS,
    ENTITY_TYPE,
    EXAMPLES,
    LANGUAGE,
    LOOKUP,
    LOOKUP_TABLES,
    NAME,
    PATTERN,
    REGEX,
    REGEX_FEATURES,
    SYNONYM,
    SYNONYMS,
    VALUE,
)
from neuralspace.nlu.converters.rasaconverter import RasaConverter


class DialogflowConverter(RasaConverter):
    INTERMEDIATE_FILE = "dialogflow_to_rasa.json"
    KEY_RASA_NLU_DATA = "rasa_nlu_data"

    @staticmethod
    def __nlu_data_converter(dataset: List[Dict[Text, Any]]) -> List[Dict[Text, Any]]:
        list_of_examples = []
        for value in dataset[COMMON_EXAMPLES]:
            list_of_examples.append(value)
        return list_of_examples

    def __regex_converter(
        self, entities: List[Dict[Text, Any]]
    ) -> List[Dict[Text, Any]]:
        all_regexes = {}
        for value in entities[REGEX_FEATURES]:
            if value[NAME] not in all_regexes:
                all_regexes[value[NAME]] = {
                    ENTITY: value[NAME],
                    EXAMPLES: [],
                    LANGUAGE: self.language,
                    ENTITY_TYPE: REGEX,
                }
            all_regexes[value[NAME]][EXAMPLES].append(value[PATTERN])
        return list(all_regexes.values())

    def __lookup_converter(self, final_data) -> List[Dict[Text, Any]]:
        lookups = []
        for value in final_data[LOOKUP_TABLES]:
            value[ENTITY] = value.pop(NAME)
            value[EXAMPLES] = value.pop(ELEMENTS)
            value[LANGUAGE] = self.language
            value[ENTITY_TYPE] = LOOKUP
            lookups.append(value)
        return lookups

    def __synonym_converter(self, final_data) -> List[Dict[Text, Any]]:
        """
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_synonyms = []
        for value in final_data[ENTITY_SYNONYMS]:
            value[ENTITY] = value.pop(VALUE)
            value[EXAMPLES] = value.pop(SYNONYMS)
            value[LANGUAGE] = self.language
            value[ENTITY_TYPE] = SYNONYM
            list_of_synonyms.append(value)
        return list_of_synonyms

    def convert(
        self, input_path: List[Path], output_directory: Path, dataset_type: List[Text]
    ):
        from rasa.nlu.convert import convert_training_data

        for single_path in input_path:
            output_directory.mkdir(parents=True, exist_ok=True)
            convert_training_data(
                str(single_path),
                str(output_directory / DialogflowConverter.INTERMEDIATE_FILE),
                "json",
                language=self.language,
            )

            with open(output_directory / DialogflowConverter.INTERMEDIATE_FILE) as f:
                data = json.load(f)[DialogflowConverter.KEY_RASA_NLU_DATA]
            (output_directory / DialogflowConverter.INTERMEDIATE_FILE).unlink()
            self.lookup_data += self.__lookup_converter(data)
            self.regex_data += self.__regex_converter(data)
            self.synonym_data += self.__synonym_converter(data)
            self.nlu_data += self.__nlu_data_converter(data)

        self.post_process(dataset_type=dataset_type, output_directory=output_directory)
