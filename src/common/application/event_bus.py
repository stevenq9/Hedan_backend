from abc import ABC, abstractmethod
from typing import TypeVar

from src.common.application.event import Event


TEvent = TypeVar('TEvent', bound=Event, contravariant=True)


class EventBus(ABC):

    @abstractmethod
    def publish(self, event: TEvent) -> None:
        pass
