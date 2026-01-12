from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class QuestionId(ValueObject):
    value: int

    def __post_init__(self):
        if self.value < 1 or self.value > 49:
            raise ValueError("Question id must be between 1 and 49")

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __int__(self):
        return self.value
