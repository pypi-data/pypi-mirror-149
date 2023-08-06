from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Text

import datasets
from datasets import load_dataset, load_dataset_builder

from neuralspace.constants import NLU_FILE, TEST, TRAIN, neuralspace_home
from neuralspace.nlu.converters.csvconverter import CsvConverter


@dataclass
class HuggingfaceDatasetCollection:
    subset: Text
    ner_dict: Dict
    train_dataset: datasets.arrow_dataset.Dataset
    test_dataset: datasets.arrow_dataset.Dataset


class HuggingfaceNerConverter:
    INTERMEDIATE_CSV_FOLDER = neuralspace_home() / "csv_dataset"

    def __init__(self, language: Text, max_entities_in_text: int):
        self.language = language
        self.max_entities_in_text = max_entities_in_text

    def ner_list_to_dict(self, ner_list: List) -> Dict:
        ner_dict = {}
        for index, entity in enumerate(ner_list):
            ner_dict[index] = entity
        return ner_dict

    def __get_label_key(self, features: Dict[Text, Any], tag_pattern: Text) -> Text:
        label_key = None
        for key in features.keys():
            if tag_pattern in key:
                label_key = key
                break
        if label_key is None:
            raise ValueError(
                f"Dataset does not contain '{tag_pattern}' or '{tag_pattern}s' as features. "
                "Please use a dataset which is formatted properly on Huggingface."
            )
        return label_key

    def load_huggingface_dataset(
        self,
        dataset_name: Text,
        subsets: List,
        num_train_examples: int,
        num_test_examples: int,
    ) -> HuggingfaceDatasetCollection:
        hf_dataset = []
        for subset in subsets:
            loaded_dataset = load_dataset_builder(dataset_name, subset)
            ner_label_key = self.__get_label_key(
                loaded_dataset.info.features, "ner_tag"
            )
            subset_ner_tags = loaded_dataset.info.features[ner_label_key].feature.names
            dataset = load_dataset(dataset_name, subset)
            if num_train_examples == -1:
                train_dataset = dataset[TRAIN]
            else:
                train_dataset = dataset[TRAIN][:num_train_examples]

            if TEST in dataset.keys():
                if num_test_examples == -1:
                    test_dataset = dataset[TEST]
                else:
                    test_dataset = dataset[TEST][:num_test_examples]
            else:
                test_dataset = None

            ner_dict = self.ner_list_to_dict(subset_ner_tags)
            hf_dataset.append(
                HuggingfaceDatasetCollection(
                    subset=subset,
                    ner_dict=ner_dict,
                    train_dataset=train_dataset,
                    test_dataset=test_dataset,
                )
            )
        return hf_dataset

    def __convert_tokens_and_ner_tags_to_text(
        self, tokens: List, ner_tags: List, ner_dict: Dict
    ):
        text = ""
        for token, ner_tag in zip(tokens, ner_tags):
            if ner_dict[ner_tag] != "O":
                text += f"[{token}]({ner_dict[ner_tag]})" + " "
            elif token == ".":
                text = text[:-1] + token
            else:
                text += token + " "
        return text

    def convert_huggingface_dataset_to_list(
        self, hf_dataset: HuggingfaceDatasetCollection
    ):
        train_list = []
        test_list = []
        for subset_dataset in hf_dataset:
            ner_dict = subset_dataset.ner_dict
            train_dataset = subset_dataset.train_dataset
            test_dataset = subset_dataset.test_dataset
            token_label_name = self.__get_label_key(train_dataset.to_dict(), "token")
            tags_label_name = self.__get_label_key(train_dataset.to_dict(), "ner_tag")

            train_tokens_list = train_dataset[token_label_name]
            train_ner_tags_list = train_dataset[tags_label_name]

            for tokens, ner_tags in zip(train_tokens_list, train_ner_tags_list):
                text = self.__convert_tokens_and_ner_tags_to_text(
                    tokens, ner_tags, ner_dict
                )
                train_list.append(text)

            if test_dataset is not None:
                test_tokens_list = test_dataset[token_label_name]
                test_ner_tags_list = test_dataset[tags_label_name]
                for tokens, ner_tags in zip(test_tokens_list, test_ner_tags_list):
                    text = self.__convert_tokens_and_ner_tags_to_text(
                        tokens, ner_tags, ner_dict
                    )
                    test_list.append(text)

        train_list = list(set(train_list))
        test_list = list(set(test_list))

        return train_list, test_list

    def __preprocess_text(self, text):
        text = text.replace(" ,", "")
        text = text.replace(",", "")
        text = text.replace('"', "").replace("'", "")
        return text

    def write_list_to_ns_format_csv(self, data: List, output_file_path: Path):
        with open(str(output_file_path), "w") as f:
            f.write(f"label,text\n")  # noqa
            for i, text in enumerate(data):
                text = self.__preprocess_text(text)
                if text.rstrip() != "" and text.count("[") <= self.max_entities_in_text:
                    if i % 2 == 0:
                        f.write(f"intent_1,{text}\n")
                    else:
                        f.write(f"intent_2,{text}\n")

    def convert_csv_to_ns_format(
        self, csv_folder_path: Path, output_folder_path, test_data_present: bool = True
    ):
        converter = CsvConverter(
            language=self.language,
            entity_mapping=False,
            auto_tag_entities=False,
            ignore_missing_examples=False,
            ignore_swapped_columns=False,
        )
        converter.convert(
            input_path=Path(csv_folder_path / TRAIN),
            output_directory=output_folder_path / TRAIN,
            dataset_type=TRAIN,
        )
        if test_data_present:
            converter.convert(
                input_path=Path(csv_folder_path / TEST),
                output_directory=output_folder_path / TEST,
                dataset_type=TEST,
            )

    def convert(
        self,
        hf_dataset_name: Text,
        subsets: Text,
        num_train_examples: int,
        num_test_examples: int,
        output_directory: Path,
    ):
        hf_dataset = self.load_huggingface_dataset(
            hf_dataset_name, subsets, num_train_examples, num_test_examples
        )
        train_list, test_list = self.convert_huggingface_dataset_to_list(hf_dataset)
        tmp_train_dataset_path = HuggingfaceNerConverter.INTERMEDIATE_CSV_FOLDER / TRAIN
        tmp_test_dataset_path = HuggingfaceNerConverter.INTERMEDIATE_CSV_FOLDER / TEST

        Path(tmp_train_dataset_path).mkdir(parents=True, exist_ok=True)
        Path(tmp_test_dataset_path).mkdir(parents=True, exist_ok=True)

        self.write_list_to_ns_format_csv(
            train_list, Path(tmp_train_dataset_path) / NLU_FILE
        )
        self.write_list_to_ns_format_csv(
            test_list, Path(tmp_test_dataset_path) / NLU_FILE
        )
        if test_list == []:
            test_data_present = False
        else:
            test_data_present = True

        self.convert_csv_to_ns_format(
            HuggingfaceNerConverter.INTERMEDIATE_CSV_FOLDER,
            output_directory,
            test_data_present,
        )
