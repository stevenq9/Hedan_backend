from dataclasses import dataclass
from datetime import datetime

from src.common.application.command import Command
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex
from src.modules.patients.domain.child.scholar_grade import ScholarGrade


@dataclass(frozen=True)
class AddChildCommand(Command[int]):
    name: str
    sex: Sex
    birthdate: datetime
    scholar_grade: ScholarGrade
    test_sender: str
    test_reason: str
    psychologist_cedula: Cedula
