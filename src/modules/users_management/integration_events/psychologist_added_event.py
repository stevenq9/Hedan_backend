from dataclasses import dataclass

from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.domain.value_objects.sex import Sex
from src.common.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True)
class PsychologistAddedEvent(IntegrationEvent):
    cedula: Cedula
    name: str
    sex: Sex
    email: Email
