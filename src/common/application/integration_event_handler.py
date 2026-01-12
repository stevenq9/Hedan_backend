from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.common.integration_events.integration_event import IntegrationEvent


TIntegrationEvent = TypeVar('TIntegrationEvent', bound=IntegrationEvent, contravariant=True)
TResponse = TypeVar('TResponse', covariant=True)


class IntegrationEventHandler(Generic[TIntegrationEvent, TResponse], ABC):
    @abstractmethod
    async def handle(self, event: TIntegrationEvent) -> TResponse:
        ...
