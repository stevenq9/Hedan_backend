from abc import ABC, abstractmethod
from typing import TypeVar

from src.common.application.command import Command

TCommand = TypeVar('TCommand', bound=Command, contravariant=True)
TResponse = TypeVar('TResponse', covariant=True)


class WriteService(ABC):
    @abstractmethod
    async def execute_async(self, query: TCommand) -> TResponse:
        ...
