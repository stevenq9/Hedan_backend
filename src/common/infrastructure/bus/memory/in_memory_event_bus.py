import asyncio
from typing import TypeVar, Dict, Type, List, get_type_hints

from src.common.application.event import Event
from src.common.application.event_bus import EventBus
from src.common.application.integration_event_handler import IntegrationEventHandler
from src.common.integration_events.integration_event import IntegrationEvent

TEvent = TypeVar('TEvent', bound=Event, contravariant=True)


class InMemoryEventBus(EventBus):
    def __init__(self, handler_class_manager):
        self.__handlers: Dict[Type[IntegrationEvent], List[Type[IntegrationEventHandler]]] = {}
        self.__handler_class_manager = handler_class_manager

    def register_handler(self, event_type: Type[IntegrationEvent], handler: Type[IntegrationEventHandler]):
        if event_type not in self.__handlers:
            self.__handlers[event_type] = []
        self.__handlers[event_type].append(handler)

    def publish(self, event: TEvent) -> None:
        if type(event) in self.__handlers:
            handlers = self.__handlers[type(event)]
            [asyncio.create_task(self.__instantiate_handler(handler).handle(event)) for handler in handlers]

    def __manage_dependency(self, dependency_class: Type):
        return self.__handler_class_manager(dependency_class)

    def __instantiate_handler(self, handler_class: Type[IntegrationEventHandler]) -> IntegrationEventHandler:
        init_method = handler_class.__init__
        if init_method is object.__init__:
            return handler_class()

        type_hints = get_type_hints(init_method)
        dependencies = [hint for name, hint in type_hints.items() if name != 'self' and name != 'return']
        instantiated_dependencies = [self.__manage_dependency(dependency) for dependency in dependencies]
        return handler_class(*instantiated_dependencies)
