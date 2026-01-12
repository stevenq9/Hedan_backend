from dataclasses import dataclass

from src.common.integration_events.integration_event import IntegrationEvent

@dataclass(frozen=True)
class TestSessionDeletedEvent(IntegrationEvent):
    test_session_id: int
