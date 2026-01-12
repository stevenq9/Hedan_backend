from typing import List, Dict, Type

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.common.integration_events.integration_event import IntegrationEvent
from src.modules.patients.integration_events.child_added_event import ChildAddedEvent
from src.modules.questionnaires.application.integration_events_handlers.child_added_event_handler import \
    ChildAddedEventHandler

event_handlers: List[Dict[Type[IntegrationEvent], Type[IntegrationEventHandler]]] = [
    {
        ChildAddedEvent: ChildAddedEventHandler
    }
]
