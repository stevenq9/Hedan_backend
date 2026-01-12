from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.common.application.query import Query
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex


@dataclass(frozen=True)
class GetPsychologistListResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    cedula: str
    name: str
    sex: Sex
    email: str