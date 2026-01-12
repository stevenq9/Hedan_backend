from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.domain.value_objects.sex import Sex


class TestResultsDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    social_anxiety_index: int
    physiological_anxiety_index: int
    defensiveness_index: int
    worry_index: int
    total_anxiety_index: int
    inconsistent_answers_index: int
