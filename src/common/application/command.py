from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

TResponse = TypeVar('TResponse')


@dataclass(frozen=True)
class Command(Generic[TResponse], ABC):
    ...
