from dataclasses import dataclass
from datetime import datetime, timedelta

from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex
from src.common.integration_events.integration_event import IntegrationEvent


@dataclass(frozen=True)
class TestAnswersSubmittedEvent(IntegrationEvent):
    test_session_id: int
    child_id: int
    psychologist_cedula: Cedula
    child_age: int
    child_scholar_grade: int
    child_sex: Sex
    datetime_submitted: datetime
    social_anxiety_index: int
    physiological_anxiety_index: int
    defensiveness_index: int
    worry_index: int
    total_anxiety_index: int
    inconsistent_answers_index: int
    time_taken: timedelta
