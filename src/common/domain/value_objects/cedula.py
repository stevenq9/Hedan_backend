from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class Cedula(ValueObject):
    value: str

    def __post_init__(self):
        pass

    def __str__(self):
        return self.value
