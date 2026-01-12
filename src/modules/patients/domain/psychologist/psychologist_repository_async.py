from abc import ABC, abstractmethod

from src.common.domain.value_objects.cedula import Cedula
from src.modules.patients.domain.psychologist.psychologist import Psychologist


class PsychologistRepositoryAsync(ABC):
    @abstractmethod
    async def add_psychologist(self, psychologist: Psychologist) -> Cedula:
        ...

    @abstractmethod
    async def get_by_cedula(self, cedula: Cedula) -> Psychologist:
        pass

    @abstractmethod
    async def update_psychologist(self, psychologist: Psychologist) -> None:
        pass