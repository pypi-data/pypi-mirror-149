from typing import Iterable, Text

from neuralspace.nlu.converters.rasa.training_data.training_data import TrainingData


def training_data_from_paths(paths: Iterable[Text], language: Text) -> TrainingData:
    from neuralspace.nlu.converters.rasa.loading import load_data

    training_data_sets = [load_data(nlu_file, language) for nlu_file in paths]
    return TrainingData().merge(*training_data_sets)
