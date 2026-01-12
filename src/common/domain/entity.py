from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TId = TypeVar('TId')


class Entity(Generic[TId], ABC):
    @property
    @abstractmethod
    def id(self) -> TId:
        pass

    def __eq__(self, other):
        return self.id == other.child_id
