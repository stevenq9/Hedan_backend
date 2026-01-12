from typing import List, Dict, Type

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.common.integration_events.integration_event import IntegrationEvent
from src.modules.questionnaires.integration_events.test_answers_submitted_event import TestAnswersSubmittedEvent
from src.modules.questionnaires.integration_events.test_session_deleted_event import TestSessionDeletedEvent
from src.modules.results_analysis.application.integration_events_handlers.test_answers_submitted_event_handler import \
    TestAnswersSubmittedEventHandler
from src.modules.results_analysis.application.integration_events_handlers.test_session_deleted_event_handler import \
    TestSessionDeletedEventHandler

game_event_handlers: List[Dict[Type[IntegrationEvent], Type[IntegrationEventHandler]]] = [
    {
        TestAnswersSubmittedEvent: TestAnswersSubmittedEventHandler
    }
]

web_app_event_handlers: List[Dict[Type[IntegrationEvent], Type[IntegrationEventHandler]]] = [
    {
        TestSessionDeletedEvent: TestSessionDeletedEventHandler
    }
]

