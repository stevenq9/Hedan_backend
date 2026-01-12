from abc import ABC
from typing import TypeVar, Generic

from src.common.domain.entity import Entity

TId = TypeVar('TId')


class AggregateRoot(Generic[TId], Entity[TId], ABC):
    ...
