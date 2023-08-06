from pathlib import Path
from typing import Any, Dict, List, Optional, Text, Tuple

import pandas as pd

from neuralspace.constants import (
    ENTITIES,
    ENTITY,
    ENTITY_TYPE,
    EXAMPLES,
    INTENT,
    LANGUAGE,
    LOOKUP_FILE,
    NLU_FILE,
    REGEX,
    REGEX_FILE,
    SYNONYM,
    SYNONYMS_FILE,
    TEXT,
)
from neuralspace.datamodels import DatasetType
from neuralspace.nlu.converters.rasaconverter import RasaConverter


class NLUValidationError(Exception):
    pass


class EntityValidationError(Exception):
    pass


class CsvConverter(RasaConverter):
    def __init__(
        self,
        entity_mapping: Optional[Dict[Text, Text]],
        auto_tag_entities: bool,
        language: Text,
        ignore_missing_examples: bool,
        ignore_swapped_columns: bool,
        nlu_file_name: Text = None,
        lookup_file_name: Text = None,
        regex_file_name: Text = None,
        synonym_file_name: Text = None,
    ):
        self.ignore_missing_examples = ignore_missing_examples
        self.ignore_swapped_columns = ignore_swapped_columns

        self.nlu_file_name: Text = nlu_file_name if nlu_file_name else NLU_FILE
        self.lookup_file_name: Text = lookup_file_name if nlu_file_name else LOOKUP_FILE
        self.regex_file_name: Text = regex_file_name if nlu_file_name else REGEX_FILE
        self.synonym_file_name: Text = (
            synonym_file_name if nlu_file_name else SYNONYMS_FILE
        )

        super(CsvConverter, self).__init__(
            language=language,
            entity_mapping=entity_mapping,
            auto_tag_entities=auto_tag_entities,
        )

    def __validate_nlu_file(self, dataset: pd.DataFrame):
        if not len(dataset.columns) == 2:
            raise NLUValidationError(
                "Two Columns(label, text) are required to convert the dataset. "
                "Download the sample file to understand the right file format"
            )
        else:
            if not self.ignore_swapped_columns:
                if len(dataset[dataset.columns[0]].unique()) >= len(dataset):
                    raise NLUValidationError(
                        "Check if you have given the labels in first column and texts in second column. "
                        "Download the sample file to understand the right file format"
                    )
        if (
            not self.ignore_missing_examples
            and dataset[dataset.columns[1]].isna().any().any()
        ):
            raise NLUValidationError("Found missing Text in your csv data")
        if (
            not self.ignore_missing_examples
            and dataset[dataset.columns[0]].isna().any().any()
        ):
            raise NLUValidationError("Found missing label data in your csv")

    @staticmethod
    def __validate_entity_file(entities: pd.DataFrame):
        for entity_label, examples in entities.items():
            if len(examples.dropna().to_list()) < 1:
                raise EntityValidationError(
                    f"There is no examples present for entity: {entity_label}"
                )

    def nlu_data_converter(self, dataset: pd.DataFrame) -> List[Dict[Text, Any]]:
        from neuralspace.nlu.converters.rasa.training_data import entities_parser

        """

        +--------+------+
        | Label  | Text |
        +--------+------+
        |A_label | sdf  |
        +---------------+

        :return: training data in the Neuralspace format
        """
        nlu_data = []
        if self.ignore_missing_examples:
            dataset.dropna(inplace=True)
        self.__validate_nlu_file(dataset)
        labels = dataset[dataset.columns[0]]
        texts = dataset[dataset.columns[1]]
        for label, text in zip(labels, texts):
            nlu_data.append(
                {
                    TEXT: entities_parser.replace_entities(text),
                    INTENT: label,
                    ENTITIES: entities_parser.find_entities_in_training_example(text),
                }
            )
        return nlu_data

    def synonym_converter(self, synonyms: pd.DataFrame) -> List[Dict[Text, Any]]:
        self.__validate_entity_file(synonyms)
        synonym_data = []
        for synonym_label, examples in synonyms.items():
            synonym_data.append(
                {
                    ENTITY: synonym_label,
                    EXAMPLES: examples.dropna().to_list(),
                    ENTITY_TYPE: SYNONYM,
                    LANGUAGE: self.language,
                }
            )
        return synonym_data

    def regex_converter(self, entities: pd.DataFrame) -> List[Dict[Text, Any]]:
        self.__validate_entity_file(entities)
        regex_data = []
        for regex_label, examples in entities.items():
            regex_data.append(
                {
                    ENTITY: regex_label,
                    EXAMPLES: examples.dropna().to_list(),
                    ENTITY_TYPE: REGEX,
                    LANGUAGE: self.language,
                }
            )
        return regex_data

    def lookup_converter(self, entities: pd.DataFrame) -> List[Dict[Text, Any]]:
        self.__validate_entity_file(entities)
        lookup_data = []
        for lookup_label, examples in entities.items():
            lookup_data.append(
                {
                    ENTITY: lookup_label,
                    EXAMPLES: examples.dropna().to_list(),
                    ENTITY_TYPE: SYNONYM,
                    LANGUAGE: self.language,
                }
            )
        return lookup_data

    def get_data_files(
        self,
        directory_path: Path,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        return (
            pd.read_csv(directory_path / self.nlu_file_name)
            if (directory_path / self.nlu_file_name).exists()
            else pd.DataFrame(),
            pd.read_csv(directory_path / self.synonym_file_name)
            if (directory_path / self.synonym_file_name).exists()
            else pd.DataFrame(),
            pd.read_csv(directory_path / self.regex_file_name)
            if (directory_path / self.regex_file_name).exists()
            else pd.DataFrame(),
            pd.read_csv(directory_path / self.lookup_file_name)
            if (directory_path / self.lookup_file_name).exists()
            else pd.DataFrame(),
        )

    def convert(
        self,
        input_path: Path,
        output_directory: Path,
        dataset_type: DatasetType,
        authtoken: Text = None,
        dataset_id: Text = None,
    ):
        nlu_data, synonym_data, regex_data, lookup_data = self.get_data_files(
            input_path
        )
        if nlu_data.columns.to_list():
            self.nlu_data = self.nlu_data_converter(nlu_data)
        if synonym_data.columns.to_list():
            self.synonym_data = self.synonym_converter(synonym_data)
        if lookup_data.columns.to_list():
            self.lookup_data = self.lookup_converter(lookup_data)
        if regex_data.columns.to_list():
            self.regex_data = self.regex_converter(regex_data)
        self.post_process(
            dataset_type=dataset_type,
            output_directory=output_directory,
            authtoken=authtoken,
            dataset_id=dataset_id,
        )
