from src.common.domain.value_objects.cedula import Cedula
from src.common.integration_events.integration_event import IntegrationEvent


class TestSessionAddedEvent(IntegrationEvent):
    id: int
    child_id: int
    psychologist_cedula: Cedula
    child_age: int
    scholar_grade: int
