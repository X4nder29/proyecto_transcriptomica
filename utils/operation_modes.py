from enum import Enum


class OperationModes(Enum):
    SingleEnd = ("Single End", "SE")
    PairedEnd = ("Paired End", "PE")