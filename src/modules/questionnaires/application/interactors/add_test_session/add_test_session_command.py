from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.common.application.command import Command
from src.common.domain.value_objects.cedula import Cedula
from src.modules.questionnaires.domain.test_session.answers_set import AnswerSet
from src.modules.questionnaires.domain.test_session.test_results import TestResults


@dataclass(frozen=True)
class AddTestSessionCommand(Command[int]):
    child_id: int
    psychologist_cedula: Cedula
    child_age: int
    scholar_grade: int
    date_time_of_answer: Optional[datetime]
    answer_set: Optional[AnswerSet]
    test_results: Optional[TestResults]
