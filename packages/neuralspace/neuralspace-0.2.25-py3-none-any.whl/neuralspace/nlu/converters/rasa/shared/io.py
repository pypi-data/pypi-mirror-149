import errno
import glob
import json
import logging
import os
import re
import warnings
from collections import OrderedDict
from hashlib import md5
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Text, Type, Union

from packaging import version
from packaging.version import LegacyVersion
from pykwalify.errors import SchemaError
from ruamel import yaml as yaml
from ruamel.yaml import RoundTripRepresenter, YAMLError
from ruamel.yaml.constructor import BaseConstructor, DuplicateKeyError, ScalarNode

from neuralspace.nlu.converters.rasa.exceptions import (
    FileIOException,
    FileNotFoundException,
    RasaException,
    SchemaValidationError,
    YamlException,
    YamlSyntaxException,
)
from neuralspace.nlu.converters.rasa.shared.constants import (
    CONFIG_SCHEMA_FILE,
    DEFAULT_LOG_LEVEL,
    DOCS_URL_TRAINING_DATA,
    ENV_LOG_LEVEL,
    LATEST_TRAINING_DATA_FORMAT_VERSION,
    MODEL_CONFIG_SCHEMA_FILE,
    NEXT_MAJOR_VERSION_FOR_DEPRECATIONS,
    PACKAGE_NAME,
    RESPONSES_SCHEMA_FILE,
    SCHEMA_EXTENSIONS_FILE,
)

logger = logging.getLogger(__name__)
KEY_TRAINING_DATA_FORMAT_VERSION = "version"
DEFAULT_ENCODING = "utf-8"
YAML_VERSION = (1, 2)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def wrap_with_color(*args: Any, color: Text) -> Text:
    return color + " ".join(str(s) for s in args) + bcolors.ENDC


def write_text_file(
    content: Text,
    file_path: Union[Text, Path],
    encoding: Text = DEFAULT_ENCODING,
    append: bool = False,
) -> None:
    """Writes text to a file.

    Args:
        content: The content to write.
        file_path: The path to which the content should be written.
        encoding: The encoding which should be used.
        append: Whether to append to the file or to truncate the file.

    """
    mode = "a" if append else "w"
    with open(file_path, mode, encoding=encoding) as file:
        file.write(content)


def read_file(filename: Union[Text, Path], encoding: Text = DEFAULT_ENCODING) -> Any:
    """Read text from a file."""

    try:
        with open(filename, encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundException(
            f"Failed to read file, " f"'{os.path.abspath(filename)}' does not exist."
        )
    except UnicodeDecodeError:
        raise FileIOException(
            f"Failed to read file '{os.path.abspath(filename)}', "
            f"could not read the file using {encoding} to decode "
            f"it. Please make sure the file is stored with this "
            f"encoding."
        )


def read_json_file(filename: Union[Text, Path]) -> Any:
    """Read json from a file."""
    content = read_file(filename)
    try:
        return json.loads(content)
    except ValueError as e:
        raise FileIOException(
            f"Failed to read json from '{os.path.abspath(filename)}'. Error: {e}"
        )


def list_directory(path: Text) -> List[Text]:
    """Returns all files and folders excluding hidden files.

    If the path points to a file, returns the file. This is a recursive
    implementation returning files in any depth of the path."""

    if not isinstance(path, str):
        raise ValueError(
            f"`resource_name` must be a string type. " f"Got `{type(path)}` instead"
        )

    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        results = []
        for base, dirs, files in os.walk(path, followlinks=True):
            # sort files for same order across runs
            files = sorted(files, key=_filename_without_prefix)
            # add not hidden files
            good_files = filter(lambda x: not x.startswith("."), files)
            results.extend(os.path.join(base, f) for f in good_files)
            # add not hidden directories
            good_directories = filter(lambda x: not x.startswith("."), dirs)
            results.extend(os.path.join(base, f) for f in good_directories)
        return results
    else:
        raise ValueError(f"Could not locate the resource '{os.path.abspath(path)}'.")


def list_files(path: Text) -> List[Text]:
    """Returns all files excluding hidden files.

    If the path points to a file, returns the file."""

    return [fn for fn in list_directory(path) if os.path.isfile(fn)]


def _filename_without_prefix(file: Text) -> Text:
    """Splits of a filenames prefix until after the first ``_``."""
    return "_".join(file.split("_")[1:])


def list_subdirectories(path: Text) -> List[Text]:
    """Returns all folders excluding hidden files.

    If the path points to a file, returns an empty list."""

    return [fn for fn in glob.glob(os.path.join(path, "*")) if os.path.isdir(fn)]


def deep_container_fingerprint(
    obj: Union[List[Any], Dict[Any, Any]], encoding: Text = DEFAULT_ENCODING
) -> Text:
    """Calculate a hash which is stable, independent of a containers key order.

    Works for lists and dictionaries. For keys and values, we recursively call
    `hash(...)` on them. Keep in mind that a list with keys in a different order
    will create the same hash!

    Args:
        obj: dictionary or list to be hashed.
        encoding: encoding used for dumping objects as strings

    Returns:
        hash of the container.
    """
    if isinstance(obj, dict):
        return get_dictionary_fingerprint(obj, encoding)
    if isinstance(obj, list):
        return get_list_fingerprint(obj, encoding)
    else:
        return get_text_hash(str(obj), encoding)


def get_dictionary_fingerprint(
    dictionary: Dict[Any, Any], encoding: Text = DEFAULT_ENCODING
) -> Text:
    """Calculate the fingerprint for a dictionary.

    The dictionary can contain any keys and values which are either a dict,
    a list or a elements which can be dumped as a string.

    Args:
        dictionary: dictionary to be hashed
        encoding: encoding used for dumping objects as strings

    Returns:
        The hash of the dictionary
    """
    stringified = json.dumps(
        {
            deep_container_fingerprint(k, encoding): deep_container_fingerprint(
                v, encoding
            )
            for k, v in dictionary.items()
        },
        sort_keys=True,
    )
    return get_text_hash(stringified, encoding)


def get_list_fingerprint(
    elements: List[Any], encoding: Text = DEFAULT_ENCODING
) -> Text:
    """Calculate a fingerprint for an unordered list.

    Args:
        elements: unordered list
        encoding: encoding used for dumping objects as strings

    Returns:
        the fingerprint of the list
    """
    stringified = json.dumps(
        [deep_container_fingerprint(element, encoding) for element in elements]
    )
    return get_text_hash(stringified, encoding)


def get_text_hash(text: Text, encoding: Text = DEFAULT_ENCODING) -> Text:
    """Calculate the md5 hash for a text."""
    return md5(text.encode(encoding)).hexdigest()  # nosec


def json_to_string(obj: Any, **kwargs: Any) -> Text:
    """Dumps a JSON-serializable object to string.

    Args:
        obj: JSON-serializable object.
        kwargs: serialization options. Defaults to 2 space indentation
                and disable escaping of non-ASCII characters.

    Returns:
        The objects serialized to JSON, as a string.
    """
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


def fix_yaml_loader() -> None:
    """Ensure that any string read by yaml is represented as unicode."""

    def construct_yaml_str(self: BaseConstructor, node: ScalarNode) -> Any:
        # Override the default string handling function
        # to always return unicode objects
        return self.construct_scalar(node)

    yaml.Loader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)
    yaml.SafeLoader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)
    yaml.allow_duplicate_keys = False


def replace_environment_variables() -> None:
    """Enable yaml loader to process the environment variables in the yaml."""
    # eg. ${USER_NAME}, ${PASSWORD}
    env_var_pattern = re.compile(r"^(.*)\$\{(.*)\}(.*)$")
    yaml.Resolver.add_implicit_resolver("!env_var", env_var_pattern, None)

    def env_var_constructor(loader: BaseConstructor, node: ScalarNode) -> Text:
        """Process environment variables found in the YAML."""
        value = loader.construct_scalar(node)
        expanded_vars = os.path.expandvars(value)
        not_expanded = [
            w for w in expanded_vars.split() if w.startswith("$") and w in value
        ]
        if not_expanded:
            raise RasaException(
                f"Error when trying to expand the "
                f"environment variables in '{value}'. "
                f"Please make sure to also set these "
                f"environment variables: '{not_expanded}'."
            )
        return expanded_vars

    yaml.SafeConstructor.add_constructor("!env_var", env_var_constructor)


fix_yaml_loader()
replace_environment_variables()


def _is_ascii(text: Text) -> bool:
    return all(ord(character) < 128 for character in text)


def write_yaml(
    data: Any,
    target: Union[Text, Path, StringIO],
    should_preserve_key_order: bool = False,
) -> None:
    """Writes a yaml to the file or to the stream

    Args:
        data: The data to write.
        target: The path to the file which should be written or a stream object
        should_preserve_key_order: Whether to force preserve key order in `data`.
    """
    _enable_ordered_dict_yaml_dumping()

    if should_preserve_key_order:
        data = convert_to_ordered_dict(data)

    dumper = yaml.YAML()
    # no wrap lines
    dumper.width = YAML_LINE_MAX_WIDTH

    # use `null` to represent `None`
    dumper.representer.add_representer(
        type(None),
        lambda self, _: self.represent_scalar("tag:yaml.org,2002:null", "null"),
    )

    if isinstance(target, StringIO):
        dumper.dump(data, target)
        return

    with Path(target).open("w", encoding=DEFAULT_ENCODING) as outfile:
        dumper.dump(data, outfile)


YAML_LINE_MAX_WIDTH = 4096


def is_key_in_yaml(file_path: Union[Text, Path], *keys: Text) -> bool:
    """Checks if any of the keys is contained in the root object of the yaml file.

    Arguments:
        file_path: path to the yaml file
        keys: keys to look for

    Returns:
          `True` if at least one of the keys is found, `False` otherwise.

    Raises:
        FileNotFoundException: if the file cannot be found.
    """
    try:
        with open(file_path, encoding=DEFAULT_ENCODING) as file:
            return any(
                any(line.lstrip().startswith(f"{key}:") for key in keys)
                for line in file
            )
    except FileNotFoundError:
        raise FileNotFoundException(
            f"Failed to read file, " f"'{os.path.abspath(file_path)}' does not exist."
        )


def convert_to_ordered_dict(obj: Any) -> Any:
    """Convert object to an `OrderedDict`.

    Args:
        obj: Object to convert.

    Returns:
        An `OrderedDict` with all nested dictionaries converted if `obj` is a
        dictionary, otherwise the object itself.
    """
    if isinstance(obj, OrderedDict):
        return obj
    # use recursion on lists
    if isinstance(obj, list):
        return [convert_to_ordered_dict(element) for element in obj]

    if isinstance(obj, dict):
        out = OrderedDict()
        # use recursion on dictionaries
        for k, v in obj.items():
            out[k] = convert_to_ordered_dict(v)

        return out

    # return all other objects
    return obj


def _enable_ordered_dict_yaml_dumping() -> None:
    """Ensure that `OrderedDict`s are dumped so that the order of keys is respected."""
    yaml.add_representer(
        OrderedDict,
        RoundTripRepresenter.represent_dict,
        representer=RoundTripRepresenter,
    )


def is_logging_disabled() -> bool:
    """Returns `True` if log level is set to WARNING or ERROR, `False` otherwise."""
    log_level = os.environ.get(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL)

    return log_level in ("ERROR", "WARNING")


def create_directory_for_file(file_path: Union[Text, Path]) -> None:
    """Creates any missing parent directories of this file path."""

    create_directory(os.path.dirname(file_path))


def dump_obj_as_json_to_file(filename: Union[Text, Path], obj: Any) -> None:
    """Dump an object as a json string to a file."""
    write_text_file(json.dumps(obj, ensure_ascii=False, indent=2), filename)


def dump_obj_as_yaml_to_string(
    obj: Any, should_preserve_key_order: bool = False
) -> Text:
    """Writes data (python dict) to a yaml string.

    Args:
        obj: The object to dump. Has to be serializable.
        should_preserve_key_order: Whether to force preserve key order in `data`.

    Returns:
        The object converted to a YAML string.
    """
    buffer = StringIO()

    write_yaml(obj, buffer, should_preserve_key_order=should_preserve_key_order)

    return buffer.getvalue()


def create_directory(directory_path: Text) -> None:
    """Creates a directory and its super paths.

    Succeeds even if the path already exists."""

    try:
        os.makedirs(directory_path)
    except OSError as e:
        # be happy if someone already created the path
        if e.errno != errno.EEXIST:
            raise


def raise_deprecation_warning(
    message: Text,
    warn_until_version: Text = NEXT_MAJOR_VERSION_FOR_DEPRECATIONS,
    docs: Optional[Text] = None,
    **kwargs: Any,
) -> None:
    """
    Thin wrapper around `raise_warning()` to raise a deprecation warning. It requires
    a version until which we'll warn, and after which the support for the feature will
    be removed.
    """
    if warn_until_version not in message:
        message = f"{message} (will be removed in {warn_until_version})"

    # need the correct stacklevel now
    kwargs.setdefault("stacklevel", 3)
    # we're raising a `FutureWarning` instead of a `DeprecationWarning` because
    # we want these warnings to be visible in the terminal of our users
    # https://docs.python.org/3/library/warnings.html#warning-categories
    raise_warning(message, FutureWarning, docs, **kwargs)


def read_validated_yaml(filename: Union[Text, Path], schema: Text) -> Any:
    """Validates YAML file content and returns parsed content.

    Args:
        filename: The path to the file which should be read.
        schema: The path to the schema file which should be used for validating the
            file content.

    Returns:
        The parsed file content.

    Raises:
        YamlValidationException: In case the model configuration doesn't match the
            expected schema.
    """
    content = read_file(filename)

    validate_yaml_schema(content, schema)
    return read_yaml(content)


def read_config_file(filename: Union[Path, Text]) -> Dict[Text, Any]:
    """Parses a yaml configuration file. Content needs to be a dictionary.

    Args:
        filename: The path to the file which should be read.

    Raises:
        YamlValidationException: In case file content is not a `Dict`.

    Returns:
        Parsed config file.
    """
    return read_validated_yaml(filename, CONFIG_SCHEMA_FILE)


def read_model_configuration(filename: Union[Path, Text]) -> Dict[Text, Any]:
    """Parses a model configuration file.

    Args:
        filename: The path to the file which should be read.

    Raises:
        YamlValidationException: In case the model configuration doesn't match the
            expected schema.

    Returns:
        Parsed config file.
    """
    return read_validated_yaml(filename, MODEL_CONFIG_SCHEMA_FILE)


def is_subdirectory(path: Text, potential_parent_directory: Text) -> bool:
    """Checks if `path` is a subdirectory of `potential_parent_directory`.

    Args:
        path: Path to a file or directory.
        potential_parent_directory: Potential parent directory.

    Returns:
        `True` if `path` is a subdirectory of `potential_parent_directory`.
    """
    if path is None or potential_parent_directory is None:
        return False

    path = os.path.abspath(path)
    potential_parent_directory = os.path.abspath(potential_parent_directory)

    return potential_parent_directory in path


def raise_warning(  # noqa : C901
    message: Text,
    category: Optional[Type[Warning]] = None,
    docs: Optional[Text] = None,
    **kwargs: Any,
) -> None:
    """Emit a `warnings.warn` with sensible defaults and a colored warning msg."""

    original_formatter = warnings.formatwarning

    def should_show_source_line() -> bool:
        if "stacklevel" not in kwargs:
            if category == UserWarning or category is None:
                return False
            if category == FutureWarning:
                return False
        return True

    def formatwarning(
        message: Text,
        category: Optional[Type[Warning]],
        filename: Text,
        lineno: Optional[int],
        line: Optional[Text] = None,
    ) -> Text:
        """Function to format a warning the standard way."""

        if not should_show_source_line():
            if docs:
                line = f"More info at {docs}"
            else:
                line = ""

        formatted_message = original_formatter(
            message, category, filename, lineno, line
        )
        return wrap_with_color(formatted_message, color=bcolors.WARNING)

    if "stacklevel" not in kwargs:
        # try to set useful defaults for the most common warning categories
        if category == DeprecationWarning:
            kwargs["stacklevel"] = 3
        elif category in (UserWarning, FutureWarning):
            kwargs["stacklevel"] = 2

    warnings.formatwarning = formatwarning
    warnings.warn(message, category=category, **kwargs)
    warnings.formatwarning = original_formatter


def read_yaml(content: Text, reader_type: Union[Text, List[Text]] = "safe") -> Any:
    """Parses yaml from a text.

    Args:
        content: A text containing yaml content.
        reader_type: Reader type to use. By default "safe" will be used.

    Raises:
        ruamel.yaml.parser.ParserError: If there was an error when parsing the YAML.
    """
    if _is_ascii(content):
        # Required to make sure emojis are correctly parsed
        content = (
            content.encode("utf-8")
            .decode("raw_unicode_escape")
            .encode("utf-16", "surrogatepass")
            .decode("utf-16")
        )

    yaml_parser = yaml.YAML(typ=reader_type)
    yaml_parser.version = YAML_VERSION
    yaml_parser.preserve_quotes = True

    return yaml_parser.load(content) or {}


def read_yaml_file(filename: Union[Text, Path]) -> Union[List[Any], Dict[Text, Any]]:
    """Parses a yaml file.

    Raises an exception if the content of the file can not be parsed as YAML.

    Args:
        filename: The path to the file which should be read.

    Returns:
        Parsed content of the file.
    """
    try:
        return read_yaml(read_file(filename, DEFAULT_ENCODING))
    except (YAMLError, DuplicateKeyError) as e:
        raise YamlSyntaxException(filename, e)


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


class YamlValidationException(YamlException, ValueError):
    """Raised if a yaml file does not correspond to the expected schema."""

    def __init__(
        self,
        message: Text,
        validation_errors: Optional[List[SchemaError.SchemaErrorEntry]] = None,
        filename: Optional[Text] = None,
        content: Any = None,
    ) -> None:
        """Create The Error.

        Args:
            message: error message
            validation_errors: validation errors
            filename: name of the file which was validated
            content: yaml content loaded from the file (used for line information)
        """
        super(YamlValidationException, self).__init__(filename)

        self.message = message
        self.validation_errors = validation_errors
        self.content = content

    def __str__(self) -> Text:
        msg = ""
        if self.filename:
            msg += f"Failed to validate '{self.filename}'. "
        else:
            msg += "Failed to validate YAML. "
        msg += self.message
        if self.validation_errors:
            unique_errors = {}
            for error in self.validation_errors:
                line_number = self._line_number_for_path(self.content, error.path)

                if line_number and self.filename:
                    error_representation = f"  in {self.filename}:{line_number}:\n"
                elif line_number:
                    error_representation = f"  in Line {line_number}:\n"
                else:
                    error_representation = ""

                error_representation += f"      {error}"
                unique_errors[str(error)] = error_representation
            error_msg = "\n".join(unique_errors.values())
            msg += f":\n{error_msg}"
        return msg

    def _line_number_for_path(self, current: Any, path: Text) -> Optional[int]:
        """Get line number for a yaml path in the current content.

        Implemented using recursion: algorithm goes down the path navigating to the
        leaf in the YAML tree. Unfortunately, not all nodes returned from the
        ruamel yaml parser have line numbers attached (arrays have them, dicts have
        them), e.g. strings don't have attached line numbers.
        If we arrive at a node that has no line number attached, we'll return the
        line number of the parent - that is as close as it gets.

        Args:
            current: current content
            path: path to traverse within the content

        Returns:
            the line number of the path in the content.
        """
        if not current:
            return None

        this_line = current.lc.line + 1 if hasattr(current, "lc") else None

        if not path:
            return this_line

        if "/" in path:
            head, tail = path.split("/", 1)
        else:
            head, tail = path, ""

        if head:
            if isinstance(current, dict) and head in current:
                return self._line_number_for_path(current[head], tail) or this_line
            elif isinstance(current, list) and head.isdigit():
                return self._line_number_for_path(current[int(head)], tail) or this_line
            else:
                return this_line
        return self._line_number_for_path(current, tail) or this_line


def validate_training_data(json_data: Dict[Text, Any], schema: Dict[Text, Any]) -> None:
    """Validate rasa training data format to ensure proper training.

    Args:
        json_data: the data to validate
        schema: the schema

    Raises:
        SchemaValidationError if validation fails.
    """
    from jsonschema import validate
    from jsonschema import ValidationError

    try:
        validate(json_data, schema)
    except ValidationError as e:
        e.message += (
            f". Failed to validate data, make sure your data "
            f"is valid. For more information about the format visit "
            f"{DOCS_URL_TRAINING_DATA}."
        )
        raise SchemaValidationError.create_from(e) from e


def validate_training_data_format_version(
    yaml_file_content: Dict[Text, Any], filename: Optional[Text]
) -> bool:
    """Validates version on the training data content using `version` field
       and warns users if the file is not compatible with the current version of
       Rasa Open Source.

    Args:
        yaml_file_content: Raw content of training data file as a dictionary.
        filename: Name of the validated file.

    Returns:
        `True` if the file can be processed by current version of Rasa Open Source,
        `False` otherwise.
    """

    if filename:
        filename = os.path.abspath(filename)

    if not isinstance(yaml_file_content, dict):
        raise YamlValidationException(
            "YAML content in is not a mapping, can not validate training "
            "data schema version.",
            filename=filename,
        )

    version_value = yaml_file_content.get(KEY_TRAINING_DATA_FORMAT_VERSION)

    if not version_value:
        # not raising here since it's not critical
        logger.info(
            f"The '{KEY_TRAINING_DATA_FORMAT_VERSION}' key is missing in "
            f"the training data file {filename}. "
            f"Rasa Open Source will read the file as a "
            f"version '{LATEST_TRAINING_DATA_FORMAT_VERSION}' file. "
            f"See {DOCS_URL_TRAINING_DATA}."
        )
        return True

    try:
        if isinstance(version_value, str):
            version_value = version_value.strip("\"'")
        parsed_version = version.parse(version_value)
        latest_version = version.parse(LATEST_TRAINING_DATA_FORMAT_VERSION)

        if isinstance(parsed_version, LegacyVersion):
            raise TypeError

        if parsed_version < latest_version:
            raise_warning(
                f"Training data file {filename} has a lower "
                f"format version than your Rasa Open Source installation: "
                f"{version_value} < {LATEST_TRAINING_DATA_FORMAT_VERSION}. "
                f"Rasa Open Source will read the file as a version "
                f"{LATEST_TRAINING_DATA_FORMAT_VERSION} file. "
                f"Please update your version key to "
                f"{LATEST_TRAINING_DATA_FORMAT_VERSION}. "
                f"See {DOCS_URL_TRAINING_DATA}."
            )

        if latest_version >= parsed_version:

            return True

    except TypeError:
        raise_warning(
            f"Training data file {filename} must specify "
            f"'{KEY_TRAINING_DATA_FORMAT_VERSION}' as string, for example:\n"
            f"{KEY_TRAINING_DATA_FORMAT_VERSION}: "
            f"'{LATEST_TRAINING_DATA_FORMAT_VERSION}'\n"
            f"Rasa Open Source will read the file as a "
            f"version '{LATEST_TRAINING_DATA_FORMAT_VERSION}' file.",
            docs=DOCS_URL_TRAINING_DATA,
        )
        return True

    raise_warning(
        f"Training data file {filename} has a greater "
        f"format version than your Rasa Open Source installation: "
        f"{version_value} > {LATEST_TRAINING_DATA_FORMAT_VERSION}. "
        f"Please consider updating to the latest version of Rasa Open Source."
        f"This file will be skipped.",
        docs=DOCS_URL_TRAINING_DATA,
    )
    return False
