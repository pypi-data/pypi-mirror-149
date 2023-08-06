from enum import Enum
from typing import NewType

DatasetType = NewType("DatasetType", str)


class DatasetTypes(Enum):
    TRAIN: DatasetType = "train"
    TEST: DatasetType = "test"
