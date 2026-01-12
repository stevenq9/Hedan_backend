from typing import List, Dict, Type

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.common.integration_events.integration_event import IntegrationEvent
from src.modules.patients.application.integration_events_handlers.psychologist_added_handler import \
    PsychologistAddedEventHandler
from src.modules.patients.application.integration_events_handlers.psychologist_updated_handler import \
    PsychologistUpdatedEventHandler
from src.modules.users_management.integration_events.psychologist_added_event import PsychologistAddedEvent
from src.modules.users_management.integration_events.psychologist_updated_event import PsychologistUpdatedEvent

event_handlers: List[Dict[Type[IntegrationEvent], Type[IntegrationEventHandler]]] = [
    {
        PsychologistAddedEvent: PsychologistAddedEventHandler,
        PsychologistUpdatedEvent: PsychologistUpdatedEventHandler
    }
]
