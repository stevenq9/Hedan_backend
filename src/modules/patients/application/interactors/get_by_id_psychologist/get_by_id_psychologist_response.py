from pydantic.dataclasses import dataclass

from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.domain.value_objects.sex import Sex


@dataclass(frozen=True)
class GetByIdPsychologistResponse:

    cedula: Cedula
    name: str
    sex: Sex
    email: Email

