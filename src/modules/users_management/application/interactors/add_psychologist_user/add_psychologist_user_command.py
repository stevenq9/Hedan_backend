from dataclasses import dataclass

from src.common.application.command import Command
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.domain.value_objects.sex import Sex


@dataclass(frozen=True)
class AddPsychologistUserCommand(Command[None]):
    cedula: Cedula
    name: str
    sex: Sex
    email: Email
    password: str
