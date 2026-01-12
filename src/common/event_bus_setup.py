from typing import Dict, Type, List

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.common.infrastructure.bus.memory.in_memory_event_bus import InMemoryEventBus
from src.common.integration_events.integration_event import IntegrationEvent


def register_event_bus_handlers(
        event_bus: InMemoryEventBus,
        handlers: List[Dict[Type[IntegrationEvent], Type[IntegrationEventHandler]]]
) -> None:
    for handler_dict in handlers:
        [event_bus.register_handler(event, handler_cls) for event, handler_cls in handler_dict.items()]
