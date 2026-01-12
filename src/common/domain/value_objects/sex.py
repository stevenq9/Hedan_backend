from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Sex(str, Enum):
    MALE = "m"
    FEMALE = "f"

    def __str__(self):
        return str(self.value)
