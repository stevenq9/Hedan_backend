from abc import ABC, abstractmethod

from src.modules.patients.domain.child.child import Child


class ChildRepositoryAsync(ABC):
    @abstractmethod
    async def add_child(self, child: Child) -> int:
        ...
