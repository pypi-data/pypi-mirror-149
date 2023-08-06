import logging
from collections import defaultdict
from typing import Any, Dict, Text

import neuralspace.nlu.converters.rasa.shared.io
from neuralspace.nlu.converters.rasa.constants import ENTITIES
from neuralspace.nlu.converters.rasa.formats.markdown import INTENT
from neuralspace.nlu.converters.rasa.formats.readerwriter import (
    JsonTrainingDataReader,
    TrainingDataWriter,
)
from neuralspace.nlu.converters.rasa.message import Message
from neuralspace.nlu.converters.rasa.shared.io import json_to_string
from neuralspace.nlu.converters.rasa.shared.nlu.constants import TEXT
from neuralspace.nlu.converters.rasa.training_data.training_data import TrainingData
from neuralspace.nlu.converters.rasa.util import transform_entity_synonyms

logger = logging.getLogger(__name__)


class RasaReader(JsonTrainingDataReader):
    def read_from_json(self, js: Dict[Text, Any], **_: Any) -> "TrainingData":
        """Loads training data stored in the rasa NLU data format."""
        from neuralspace.nlu.converters.rasa.training_data.schemas.data_schema import (
            rasa_nlu_data_schema,
        )

        neuralspace.nlu.converters.rasa.shared.io.validate_training_data(
            js, rasa_nlu_data_schema()
        )

        data = js["rasa_nlu_data"]
        common_examples = data.get("common_examples", [])
        entity_synonyms = data.get("entity_synonyms", [])
        regex_features = data.get("regex_features", [])
        lookup_tables = data.get("lookup_tables", [])

        entity_synonyms = transform_entity_synonyms(entity_synonyms)

        training_examples = []
        for ex in common_examples:
            # taking care of custom entries
            msg = Message.build(
                text=ex.pop(TEXT, ""),
                intent=ex.pop(INTENT, None),
                entities=ex.pop(ENTITIES, None),
                **ex,
            )
            training_examples.append(msg)

        return TrainingData(
            training_examples, entity_synonyms, regex_features, lookup_tables
        )


class RasaWriter(TrainingDataWriter):
    def dumps(self, training_data: "TrainingData", **kwargs: Any) -> Text:
        """Writes Training Data to a string in json format."""

        js_entity_synonyms = defaultdict(list)
        for k, v in training_data.entity_synonyms.items():
            if k != v:
                js_entity_synonyms[v].append(k)

        formatted_synonyms = [
            {"value": value, "synonyms": syns}
            for value, syns in js_entity_synonyms.items()
        ]

        formatted_examples = [
            example.as_dict_nlu() for example in training_data.training_examples
        ]

        return json_to_string(
            {
                "rasa_nlu_data": {
                    "common_examples": formatted_examples,
                    "regex_features": training_data.regex_features,
                    "lookup_tables": training_data.lookup_tables,
                    "entity_synonyms": formatted_synonyms,
                }
            },
            **kwargs,
        )
