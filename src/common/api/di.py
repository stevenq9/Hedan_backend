from injector import Injector, singleton
from mediatr import Mediator

from src.common.api.handler_factory import handler_factory
from src.common.application.event_bus import EventBus
from src.common.infrastructure.bus.memory.in_memory_event_bus import InMemoryEventBus


def add_mediator(injector: Injector):
    mediator = Mediator()
    mediator.handler_class_manager = handler_factory(injector)
    injector.binder.bind(Mediator, to=mediator, scope=singleton)


def add_event_bus(injector: Injector):
    in_memory_event_bus: InMemoryEventBus = InMemoryEventBus(handler_class_manager=handler_factory(injector))
    injector.binder.bind(EventBus, to=in_memory_event_bus, scope=singleton)
