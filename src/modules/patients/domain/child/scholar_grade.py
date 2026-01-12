from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class ScholarGrade(ValueObject):
    value: int

    def __post_init__(self):
        if self.value < 1 or self.value > 5:
            raise ValueError("Scholar grade must be between 1 and 5")

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value
