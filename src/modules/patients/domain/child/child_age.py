from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class ChildAge(ValueObject):
    value: int

    def __post_init__(self):
        if self.value < 6 or self.value > 8:
            raise ValueError("Child age must be between 6 and 8")

    def __int__(self):
        return self.value
