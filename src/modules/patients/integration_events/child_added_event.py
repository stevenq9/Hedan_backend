from dataclasses import dataclass
from datetime import datetime

from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex
from src.common.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True)
class ChildAddedEvent(IntegrationEvent):
    child_id: int
    name: str
    sex: Sex
    birthdate: datetime
    scholar_grade: int
    test_sender: str
    test_reason: str
    psychologist_cedula: Cedula
