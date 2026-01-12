from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from src.common.application.command import Command

TCommand = TypeVar('TCommand', bound=Command, contravariant=True)
TResponse = TypeVar('TResponse', covariant=True)


class CommandHandler(Generic[TCommand, TResponse], ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> TResponse:
        ...
