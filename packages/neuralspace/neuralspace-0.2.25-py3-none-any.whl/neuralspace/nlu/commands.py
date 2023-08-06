import asyncio
import json
import typing
from contextvars import Context
from inspect import Parameter
from pathlib import Path
from typing import List, Text

import click
import randomname
from rich.console import Console

from neuralspace.apis import get_async_http_session
from neuralspace.constants import (
    ERROR,
    NAME_GENERATOR_CONFIG,
    NER_TYPES,
    ORANGE3_END,
    ORANGE3_START,
    RED_END,
    RED_START,
)
from neuralspace.datamodels import DatasetTypes
from neuralspace.nlu.apis import (
    create_project,
    delete_examples,
    delete_models,
    delete_project,
    deploy,
    get_languages,
    list_examples,
    list_models,
    list_projects,
    parse,
    train_model,
    upload_dataset,
    wait_till_training_completes,
)
from neuralspace.nlu.constants import SUPPORTED_LANGUAGES, TRAINING_PROGRESS
from neuralspace.nlu.utils import print_converted_data_inference
from neuralspace.utils import get_entity_list, print_logo, setup_logger

console = Console()


class MappingClass(click.ParamType):
    name: Text = "mapping_class"

    def convert(
        self,
        value: typing.Any,
        param: typing.Optional["Parameter"],
        ctx: typing.Optional["Context"],
    ) -> typing.Union[typing.Dict[Text, Text], bool]:
        entity_mapping = value.split(",")
        total_entity_mapping = []
        for entities in entity_mapping:
            total_entity_mapping.append(entities.split(":"))
        entity_mapping = dict()
        for entity in total_entity_mapping:
            entity_mapping[entity[0]] = entity[1]
        for entities in total_entity_mapping:
            try:
                assert len(entities) == 2
            except AssertionError:
                console.print(
                    f"{RED_START}Entities mapping is given in the wrong format, Right format is{RED_END} "
                    f"{ORANGE3_START}'your_entity_name:ns_entity_name,your_entity_name...'{ORANGE3_END}"
                )
                return False
        return entity_mapping


@click.group(
    name="nlu", short_help="For short text classification and entity extraction"
)
def nlu():
    pass


@nlu.command(name="get-languages")
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_get_languages(log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_languages())
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(
    name="convert-dataset",
    help="To know more about the format and structure kindly refer to"
    "https://docs.neuralspace.ai/natural-language-understanding/concepts/dataset-format-and-converters",
)
@click.option(
    "-F",
    "--from-platform",
    type=click.Choice(["dialogflow", "rasa", "csv", "luis"], case_sensitive=False),
    required=True,
    help="Where to convert data from [dialogflow, rasa, csv, luis]",
)
@click.option(
    "-at",
    "--auto-tag-entities",
    is_flag=True,
    default=False,
    help="If the names of your entities are the same as our pretrained entities "
    "then tag them automatically as pre-trained",
)
@click.option(
    "-L",
    "--language",
    type=click.STRING,
    required=True,
    help="Language in which the dataset is. "
    "Use the following to get a list of supported languages: neuralspace nlu get-languages",
)
@click.option(
    "-em",
    "--entity-mapping",
    type=MappingClass(),
    required=False,
    help="If your entity names don't match with our pre-trained entity names then you can give a mapping like this:"
    "'your_entity_name:ns_entity_name,...' and we will convert them to our format. "
    "This argument works best with the --auto-tag-entities argument as it can happen in a "
    "lot of cases that your entity names don't match our pre-trained entity names, "
    "or even regex and lookup entities. This helps you make make the best out of the platform.",
)
@click.option(
    "-t",
    "--data-type",
    type=click.Choice(["train", "test"], case_sensitive=True),
    default="train",
    help="you can decide whether you want it as test or train data. Defaults to train.",
)
@click.option(
    "-d",
    "--input-path",
    required=True,
    multiple=True,
    help="Name of the folder in which the dataset files are stored. "
    "You can read more about dataset formats here https://docs.neuralspace.ai/natural-language-understanding/concepts/dataset-format-and-converters#dataset-format "  # noqa
    "You can look at sample datasets here: https://github.com/Neural-Space/neuralspace-examples/tree/format_examples/datasets/nlu/Sample%20formats",  # noqa
)
@click.option(
    "-o",
    "--output-path",
    required=True,
    help="Path to the folder in which the converted dataset files will be stored",
)
@click.option(
    "-ime",
    "--ignore-missing-examples",
    is_flag=True,
    default=False,
    help="Will ignore if there are any missing examples in your data (works with CSV format only)",
)
@click.option(
    "-iswp",
    "--ignore-swapped-columns",
    is_flag=True,
    default=False,
    help="Will ignore if you have swapped columns in your nlu examples data (works with csv files only)",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def converter(
    from_platform: Text,
    auto_tag_entities: bool,
    language: Text,
    entity_mapping: typing.Dict[Text, Text],
    input_path: List[Text],
    data_type: Text,
    output_path: Text,
    ignore_missing_examples: bool,
    ignore_swapped_columns: bool,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    if entity_mapping is not False:
        if from_platform == "rasa":
            from neuralspace.nlu.converters.rasaconverter import RasaConverter

            converter = RasaConverter(
                language=language,
                entity_mapping=entity_mapping,
                auto_tag_entities=auto_tag_entities,
            )
            converter.convert(
                input_path=[Path(path) for path in input_path],
                output_directory=Path(output_path),
                dataset_type=DatasetTypes(data_type).value,
            )
        elif from_platform == "dialogflow":
            from neuralspace.nlu.converters.dialogflowconverter import (
                DialogflowConverter,
            )

            converter = DialogflowConverter(
                language=language,
                entity_mapping=entity_mapping,
                auto_tag_entities=auto_tag_entities,
            )
            converter.convert(
                input_path=[Path(path) for path in input_path],
                output_directory=Path(output_path),
                dataset_type=DatasetTypes(data_type).value,
            )
        elif from_platform == "luis":
            from neuralspace.nlu.converters.luisconverter import (
                LuisConverter,
            )

            converter = LuisConverter(
                language=language,
                entity_mapping=entity_mapping,
                auto_tag_entities=auto_tag_entities,
            )
            converter.convert(
                input_path=[Path(path) for path in input_path],
                output_directory=Path(output_path),
                dataset_type=DatasetTypes(data_type).value,
            )
        else:
            from neuralspace.nlu.converters.csvconverter import CsvConverter

            converter = CsvConverter(
                language=language,
                entity_mapping=entity_mapping,
                auto_tag_entities=auto_tag_entities,
                ignore_missing_examples=ignore_missing_examples,
                ignore_swapped_columns=ignore_swapped_columns,
            )
            converter.convert(
                input_path=Path(input_path[0]),
                output_directory=Path(output_path),
                dataset_type=DatasetTypes(data_type).value,
            )
        print_converted_data_inference(from_platform, Path(output_path), converter)
    else:
        console.print(
            f"{ERROR} There is some error in the entity mapping you have given"
        )


@nlu.command(
    name="convert-huggingface-ner-dataset",
)
@click.option(
    "-hf",
    "--huggingface-dataset",
    required=True,
    type=click.STRING,
    help="Exact name of the NER dataset from huggingface dataset hub",
)
@click.option(
    "-s",
    "--subset",
    required=True,
    type=click.STRING,
    multiple=True,
    help="Go to the dataset page on huggingface and pass all the subsets you want as shown in the dataset preview."
    "For multiple subsets, pass them in one string seperated by space",
)
@click.option(
    "-L",
    "--language",
    type=click.STRING,
    required=True,
    help="Language in which the dataset is. "
    "Use the following to get a list of supported languages: neuralspace nlu get-languages"
    "For datasets having more than one language, select 'multilingual'",
)
@click.option(
    "-tr",
    "--num-train-examples",
    type=click.INT,
    required=False,
    default=-1,
    help="Pass the number of examples you want in your converted training dataset for each subset"
    "Dont set this parameter if you want to select all the examples available in the dataset",
)
@click.option(
    "-te",
    "--num-test-examples",
    type=click.INT,
    required=False,
    default=-1,
    help="Pass the number of examples you want in your converted test dataset for each subset"
    "Dont set this parameter if you want to select all the examples available in the dataset",
)
@click.option(
    "-o",
    "--output-path",
    required=True,
    type=click.STRING,
    help="Path to the folder in which the converted dataset files will be stored",
)
@click.option(
    "-me",
    "--max-entities",
    required=False,
    default=30,
    type=click.INT,
    help="Only keeps sentences having number of entities less than selected value."
    "Sentences having more entities are discarded.",
)
def huggingface_converter(
    huggingface_dataset: Text,
    subset: List,
    language: Text,
    num_train_examples: int,
    num_test_examples: int,
    output_path: Text,
    max_entities: int,
):
    from neuralspace.nlu.converters.huggingface_nerconverter import (
        HuggingfaceNerConverter,
    )

    converter = HuggingfaceNerConverter(
        language=language, max_entities_in_text=max_entities
    )
    converter.convert(
        hf_dataset_name=huggingface_dataset,
        subsets=list(subset),
        num_train_examples=num_train_examples,
        num_test_examples=num_test_examples,
        output_directory=Path(output_path),
    )


@nlu.command(name="create-project")
@click.option(
    "-p",
    "--project-name",
    type=click.STRING,
    required=False,
    help="Project Name",
)
@click.option(
    "-L",
    "--languages",
    type=click.STRING,
    multiple=True,
    required=True,
    help="Language code that you want to select for this project. To get the list of supported languages try:"
    " neuralspace nlu get-languages",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_create_project(project_name: Text, languages: List[Text], log_level: Text):
    setup_logger(log_level=log_level)
    languages = list(languages)
    if project_name is None:
        project_name = randomname.get_name(**NAME_GENERATOR_CONFIG)
    if not languages:
        ValueError(f"Languages is mandatory. You can select from {SUPPORTED_LANGUAGES}")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(create_project(project_name, languages))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="delete-project")
@click.option(
    "-p",
    "--project-id",
    type=click.STRING,
    required=True,
    help="id of the project you want to delete",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_delete_project(project_id: Text, log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(delete_project(project_id))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="list-projects")
@click.option(
    "-S",
    "--search",
    type=click.STRING,
    required=False,
    default="",
    help="Substring search keyword",
)
@click.option(
    "-p",
    "--page-number",
    type=click.INT,
    required=False,
    default=1,
    help="Which page number to fetch",
)
@click.option(
    "-s",
    "--page-size",
    type=click.INT,
    required=False,
    default=20,
    help="items per page to fetch",
)
@click.option(
    "-L",
    "--language",
    type=click.STRING,
    multiple=True,
    default=[],
    help="List of languages. E.g., -L en -L de; You can add multiple languages",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose results",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_list_projects(
    search: Text,
    page_number: int,
    page_size: int,
    language: List[Text],
    verbose: bool,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    languages = list(language)
    if not languages:
        ValueError(f"Languages is mandatory. You can select from {SUPPORTED_LANGUAGES}")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        list_projects(search, page_size, page_number, languages, verbose)
    )
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="upload-dataset")
@click.option(
    "-d",
    "--dataset-file",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="An nlu dataset file in NeuralSpace format. "
    "To convert from other platforms like Rasa, Dialogflow, etc. try: ",
)
@click.option(
    "-p",
    "--project-id",
    type=click.STRING,
    required=True,
    help="NLU project id",
)
@click.option(
    "-L",
    "--language",
    type=click.Choice(SUPPORTED_LANGUAGES),
    required=True,
    help="Language",
)
@click.option(
    "-s",
    "--skip-first",
    type=click.INT,
    required=False,
    default=0,
    help="Skip this many example from the beginning. "
    "Use this in case you have to interrupt upload or if some error occurred while uploading.",
)
@click.option(
    "-e",
    "--ignore-errors",
    type=click.BOOL,
    required=False,
    default=False,
    help="To ignore errors and go to the next example",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_upload_dataset(
    dataset_file: Path,
    project_id: Text,
    language: Text,
    skip_first: int,
    ignore_errors: bool,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    dataset = json.loads(Path(dataset_file).read_text())
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        upload_dataset(
            dataset,
            project_id=project_id,
            language=language,
            skip_first=skip_first,
            ignore_errors=ignore_errors,
        )
    )
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="list-examples")
@click.option(
    "-p",
    "--project-id",
    type=click.STRING,
    required=True,
    help="Project ID",
)
@click.option(
    "-L",
    "--language",
    type=click.STRING,
    required=True,
    help="Language",
)
@click.option(
    "-P",
    "--prepared",
    type=click.Choice(["true", "false"]),
    required=False,
    default="true",
    help="Flag to filter only prepared examples",
)
@click.option(
    "-t",
    "--type",
    type=click.Choice(["train", "test"]),
    required=False,
    default="train",
    help="Flag to filter only train or test examples",
)
@click.option(
    "-i",
    "--intent",
    type=click.STRING,
    required=False,
    help="Flag to filter examples only for this intent",
)
@click.option(
    "-n",
    "--page-number",
    type=click.INT,
    required=False,
    default=1,
    help="Which page number to fetch",
)
@click.option(
    "-s",
    "--page-size",
    type=click.INT,
    required=False,
    default=20,
    help="items per page to fetch",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose results",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_list_examples(
    project_id: Text,
    language: Text,
    prepared: Text,
    type: Text,
    intent: Text,
    page_number: int,
    page_size: int,
    verbose: bool,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    prepared_flag = False
    if prepared == "true":
        prepared_flag = True
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        list_examples(
            project_id,
            language,
            prepared_flag,
            type,
            intent,
            page_number,
            page_size,
            verbose,
        )
    )
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="delete-example")
@click.option(
    "-e",
    "--example-id",
    type=click.STRING,
    required=True,
    multiple=True,
    help="Example ID",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_delete_example(example_id: List[Text], log_level: Text):
    setup_logger(log_level=log_level)
    example_ids = list(example_id)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(delete_examples(example_ids))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="train")
@click.option(
    "-p",
    "--project-id",
    type=click.STRING,
    required=True,
    help="Project ID",
)
@click.option(
    "-L",
    "--language",
    type=click.STRING,
    required=True,
    help="Language",
)
@click.option(
    "-m",
    "--model-name",
    type=click.STRING,
    required=False,
    help="Name of the model",
)
@click.option(
    "-n",
    "--training-jobs",
    type=click.INT,
    required=False,
    default=1,
    help="No of training jobs to be queued",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_train_model(
    project_id: Text,
    language: Text,
    model_name: Text,
    log_level: Text,
    training_jobs: int,
):
    setup_logger(log_level=log_level)
    print_logo()
    if model_name is None:
        model_name = randomname.get_name(**NAME_GENERATOR_CONFIG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        train_model(project_id, language, model_name, training_jobs)
    )
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="model-status")
@click.option(
    "-m",
    "--model-id",
    type=click.STRING,
    required=True,
    help="Model ID",
)
@click.option(
    "-w",
    "--wait",
    is_flag=True,
    default=True,
    help="Wait for training to complete",
)
@click.option(
    "-i",
    "--wait-interval",
    type=click.INT,
    required=False,
    default=1,
    help="Time to wait between consecutive status-check pools.",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_check_model_status(
    model_id: Text, wait: bool, wait_interval: int, log_level: Text
):
    setup_logger(log_level=log_level)
    print_logo()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(wait_till_training_completes(model_id, wait, wait_interval))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="list-models")
@click.option(
    "-p",
    "--project-id",
    type=click.STRING,
    required=True,
    help="Project ID",
)
@click.option(
    "-L",
    "--language",
    type=click.STRING,
    required=True,
    help="Language",
)
@click.option(
    "-s",
    "--training-status",
    type=click.STRING,
    required=False,
    help=f"Flag to filter models with the given training status. "
    f"These are some valid values: {', '.join(TRAINING_PROGRESS)}",
)
@click.option(
    "-n",
    "--page-number",
    type=click.INT,
    required=False,
    default=1,
    help="Which page number to fetch",
)
@click.option(
    "-s",
    "--page-size",
    type=click.INT,
    required=False,
    default=20,
    help="items per page to fetch",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose results",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_list_models(
    project_id: Text,
    language: Text,
    training_status: List[Text],
    page_number: int,
    page_size: int,
    verbose: bool,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    if training_status:
        training_status = list(training_status)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        list_models(
            project_id, language, training_status, page_number, page_size, verbose
        )
    )
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="delete-model")
@click.option(
    "-m",
    "--model-id",
    type=click.STRING,
    required=True,
    help="Model ID",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_delete_model(model_id: Text, log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(delete_models(model_id))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="deploy")
@click.option(
    "-m",
    "--model-id",
    type=click.STRING,
    required=True,
    help="Model ID",
)
@click.option(
    "-n",
    "--n-replicas",
    type=click.INT,
    required=False,
    default=1,
    help="Number of replicas to deploy for this model. One Replica gives you 5-8 requests per second throughput.",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_deploy(model_id: Text, n_replicas: int, log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(deploy(model_id, n_replicas))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="parse")
@click.option(
    "-m",
    "--model-id",
    type=click.STRING,
    required=True,
    help="Model ID",
)
@click.option(
    "-i",
    "--input-text",
    type=click.STRING,
    required=True,
    help="Text to parse",
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def nlu_parse(model_id: Text, input_text: Text, log_level: Text):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(parse(model_id, input_text))
    loop.run_until_complete(get_async_http_session().close())


@nlu.command(name="get-pretrained-entities")
@click.option("-L", "--language", type=click.STRING, required=True)
@click.option("-s", "--search", type=click.STRING, default="")
@click.option("-p", "--page-number", type=click.INT, default=1)
@click.option("-P", "--page-size", type=click.INT, default=5)
@click.option(
    "-T", "--entity-type", type=click.Choice(NER_TYPES), default="pre-trained"
)
@click.option(
    "-l", "--log-level", type=click.Choice(["INFO", "DEBUG", "ERROR"]), default="INFO"
)
def get_pretrained_entities(
    language: Text,
    search: Text,
    page_number: int,
    page_size: int,
    entity_type: Text,
    log_level: Text,
):
    setup_logger(log_level=log_level)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        get_entity_list(language, search, page_number, page_size, entity_type)
    )
    loop.run_until_complete(get_async_http_session().close())
