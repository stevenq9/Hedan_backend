from abc import ABC
from dataclasses import dataclass

from src.common.application.query import Query
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex


@dataclass(frozen=True)
class GetPsychologistListQuery():
    ...
    #cedula: Cedula
    #name: str
    #sex: Sex
    #email: str