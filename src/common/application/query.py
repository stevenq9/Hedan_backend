from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic

TResponse = TypeVar('TResponse')


@dataclass(frozen=True)
class Query(Generic[TResponse], ABC):
    pass
