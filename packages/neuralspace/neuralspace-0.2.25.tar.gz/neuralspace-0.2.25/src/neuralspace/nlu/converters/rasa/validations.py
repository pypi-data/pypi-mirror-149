from typing import Text

from ruamel.yaml.constructor import DuplicateKeyError

from neuralspace.nlu.converters.rasa.exceptions import YamlSyntaxException
from neuralspace.nlu.converters.rasa.shared.constants import (
    PACKAGE_NAME,
    RESPONSES_SCHEMA_FILE,
    SCHEMA_EXTENSIONS_FILE,
)
from neuralspace.nlu.converters.rasa.shared.io import (
    YamlValidationException,
    read_yaml,
    read_yaml_file,
)


def validate_yaml_schema(yaml_file_content: Text, schema_path: Text) -> None:
    """
    Validate yaml content.

    Args:
        yaml_file_content: the content of the yaml file to be validated
        schema_path: the schema of the yaml file
    """
    from pykwalify.core import Core
    from pykwalify.errors import SchemaError
    from ruamel.yaml import YAMLError
    import pkg_resources
    import logging

    log = logging.getLogger("pykwalify")
    log.setLevel(logging.CRITICAL)

    try:
        # we need "rt" since
        # it will add meta information to the parsed output. this meta information
        # will include e.g. at which line an object was parsed. this is very
        # helpful when we validate files later on and want to point the user to the
        # right line
        source_data = read_yaml(yaml_file_content, reader_type=["safe", "rt"])
    except (YAMLError, DuplicateKeyError) as e:
        raise YamlSyntaxException(underlying_yaml_exception=e)

    schema_file = pkg_resources.resource_filename(PACKAGE_NAME, schema_path)
    schema_utils_file = pkg_resources.resource_filename(
        PACKAGE_NAME, RESPONSES_SCHEMA_FILE
    )
    schema_extensions = pkg_resources.resource_filename(
        PACKAGE_NAME, SCHEMA_EXTENSIONS_FILE
    )

    # Load schema content using our YAML loader as `pykwalify` uses a global instance
    # which can fail when used concurrently
    schema_content = read_yaml_file(schema_file)
    schema_utils_content = read_yaml_file(schema_utils_file)
    schema_content = dict(schema_content, **schema_utils_content)

    c = Core(
        source_data=source_data,
        schema_data=schema_content,
        extensions=[schema_extensions],
    )

    try:
        c.validate(raise_exception=True)
    except SchemaError:
        raise YamlValidationException(
            "Please make sure the file is correct and all "
            "mandatory parameters are specified. Here are the errors "
            "found during validation",
            c.errors,
            content=source_data,
        )
