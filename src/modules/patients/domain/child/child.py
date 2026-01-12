from datetime import date

from src.common.domain.aggregate_root import AggregateRoot
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex
from src.modules.patients.domain.child.scholar_grade import ScholarGrade


class Child(AggregateRoot[int]):

    def __init__(
            self,
            id: int,
            name: str,
            sex: Sex,
            birthdate: date,
            scholar_grade: ScholarGrade,
            psychologist_cedula: Cedula
    ):
        self.__id = id
        self.__name = name
        self.__sex = sex
        self.__birthdate = birthdate
        self.__scholar_grade = scholar_grade
        self.__psychologist_cedula = psychologist_cedula

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def sex(self) -> Sex:
        return self.__sex

    @property
    def psychologist_cedula(self) -> Cedula:
        return self.__psychologist_cedula

    @property
    def birthdate(self) -> date:
        return self.__birthdate

    @property
    def scholar_grade(self) -> ScholarGrade:
        return self.__scholar_grade
