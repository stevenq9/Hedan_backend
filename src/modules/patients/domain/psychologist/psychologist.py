from src.common.domain.aggregate_root import AggregateRoot
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.domain.value_objects.sex import Sex


class Psychologist(AggregateRoot[Cedula]):
    def __init__(
            self,
            cedula: Cedula,
            name: str,
            sex: Sex,
            email: Email
    ) -> None:
        self.__cedula = cedula
        self.name = name
        self.sex = sex
        self.email = email

    @property
    def id(self) -> Cedula:
        return self.__cedula
