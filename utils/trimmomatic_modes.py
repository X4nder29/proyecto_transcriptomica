from enum import Enum


class TrimmomaticModes(Enum):
    SingleEnd = ("Single End", "SE")
    PairedEnd = ("Paired End", "PE")