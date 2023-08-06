import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Text

from neuralspace.constants import TYPE
from neuralspace.datamodels import DatasetType


class DataConverter:
    LOOKUP_FILE = "lookup.json"
    REGEX_FILE = "regex.json"
    SYNONYM_FILE = "synonym.json"
    NLU_FILE = "nlu.json"

    @staticmethod
    def __training_data_converter(final_data) -> List[Dict[Text, Any]]:
        NotImplementedError("Training data converter is not implemented")
        pass

    def __regex_converter(self, final_data: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        NotImplementedError("Regex converter is not implemented")

    def __synonym_converter(self, final_data: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        NotImplementedError("synonym converter is not implemented")

    def __lookup_converter(self, final_data: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        NotImplementedError("lookup converter is not implemented")

    def convert(self, input_path: Path, output_path: Path, dataset_type: DatasetType):
        NotImplementedError("lookup converter is not implemented")

    def convert_multiple(
        self, input_path: List[Path], output_path: Path, dataset_type: DatasetType
    ):
        NotImplementedError("lookup converter is not implemented")

    @staticmethod
    def count(dataset):
        return len(dataset)

    @staticmethod
    def get_converted_file_name(filename: Text, prefix: Text) -> Text:
        prefixed_file_name = filename
        if prefix:
            prefixed_file_name = f"{prefix}-{filename}"
        return prefixed_file_name

    @staticmethod
    def save_converted_data(
        output_directory: Path,
        lookup_data: Optional[List[Dict[Text, Any]]] = None,
        regex_data: Optional[List[Dict[Text, Any]]] = None,
        synonym_data: Optional[List[Dict[Text, Any]]] = None,
        nlu_data: Optional[List[Dict[Text, Any]]] = None,
        dataset_id: Optional[Text] = None,
    ):
        output_directory.mkdir(parents=True, exist_ok=True)

        if lookup_data is not None:
            lookup_file_name = DataConverter.get_converted_file_name(
                DataConverter.LOOKUP_FILE, dataset_id
            )
            with open(output_directory / lookup_file_name, "w") as f:
                json.dump(lookup_data, f, indent=4, ensure_ascii=False)
        if regex_data is not None:
            regex_file_name = DataConverter.get_converted_file_name(
                DataConverter.REGEX_FILE, dataset_id
            )
            with open(output_directory / regex_file_name, "w") as f:
                json.dump(regex_data, f, indent=4, ensure_ascii=False)
        if synonym_data is not None:
            synonym_file_name = DataConverter.get_converted_file_name(
                DataConverter.SYNONYM_FILE, dataset_id
            )
            with open(output_directory / synonym_file_name, "w") as f:
                json.dump(synonym_data, f, indent=4, ensure_ascii=False)
        if nlu_data is not None:
            nlu_file_name = DataConverter.get_converted_file_name(
                DataConverter.NLU_FILE, dataset_id
            )
            with open(output_directory / nlu_file_name, "w") as f:
                json.dump(nlu_data, f, indent=4, ensure_ascii=False)

    def set_data_type(self, dataset_type: DatasetType = "train"):
        for example in self.nlu_data:
            example[TYPE] = dataset_type
