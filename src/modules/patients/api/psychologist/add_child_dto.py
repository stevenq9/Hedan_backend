from dataclasses import dataclass
from datetime import datetime

from src.common.domain.value_objects.sex import Sex


@dataclass
class AddChildDto:
    name: str
    sex: Sex
    birthdate: datetime
    scholar_grade: int
    test_sender: str
    test_reason: str
