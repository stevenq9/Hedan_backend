from datetime import datetime, timedelta
from typing import Optional

from src.common.domain.aggregate_root import AggregateRoot
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.sex import Sex
from src.modules.questionnaires.domain.test_session.answer_set_already_set_error import AnswerSetAlreadySetError
from src.modules.questionnaires.domain.test_session.answers_set import AnswerSet
from src.modules.questionnaires.domain.test_session.cmasr2_calculator import calculate_cmasr2_test_results
from src.modules.questionnaires.domain.test_session.test_results import TestResults


class TestSession(AggregateRoot[int]):
    def __init__(
            self,
            id: int,
            child_id: int,
            psychologist_cedula: Cedula,
            child_age: int,
            scholar_grade: int,
            child_sex: Sex,
            test_sender: str,
            test_reason: str
    ):
        self.__id = id
        self.__child_id = child_id
        self.__psychologist_cedula = psychologist_cedula
        self.__child_age = child_age
        self.__scholar_grade = scholar_grade
        self.__child_sex = child_sex
        self.__test_sender = test_sender
        self.__test_reason = test_reason
        self.__date_time_of_answer: Optional[datetime] = None
        self.__answer_set: Optional[AnswerSet] = None
        self.__test_results: Optional[TestResults] = None
        self.__calculate_test_results_time_taken: Optional[timedelta] = None
        self.__test_token: Optional[str] = None

    @property
    def id(self):
        return self.__id

    @property
    def child_id(self):
        return self.__child_id

    @property
    def psychologist_cedula(self):
        return self.__psychologist_cedula

    @property
    def child_age(self):
        return self.__child_age

    @property
    def scholar_grade(self):
        return self.__scholar_grade

    @property
    def child_sex(self):
        return self.__child_sex

    @property
    def test_sender(self):
        return self.__test_sender

    @property
    def test_reason(self):
        return self.__test_reason

    @property
    def test_results(self):
        return self.__test_results

    @property
    def date_time_of_answer(self):
        return self.__date_time_of_answer

    @property
    def answer_set(self):
        return self.__answer_set

    @property
    def test_token(self):
        return self.__test_token

    @property
    def calculate_test_results_time_taken(self):
        return self.__calculate_test_results_time_taken

    @answer_set.setter
    def answer_set(self, answer_set: AnswerSet):
        if self.__answer_set is not None:
            raise AnswerSetAlreadySetError()

        self.__date_time_of_answer = datetime.now()
        self.__answer_set = answer_set
        start_time = datetime.now()
        self.__calculate_test_results()
        end_time = datetime.now()
        execution_time_seconds = (end_time - start_time).total_seconds()
        self.__calculate_test_results_time_taken = int(execution_time_seconds * 1000000)  # microseconds
        print(self.__calculate_test_results_time_taken)

    def __calculate_test_results(self):
        if self.answer_set is None:
            raise ValueError("The answer set is not set")
        else:
            self.__test_results = calculate_cmasr2_test_results(self.answer_set)
            import time
            time.sleep(3)

    @property
    def time_taken(self) -> timedelta:
        return timedelta(
            milliseconds=sum([int(time.time_taken.total_seconds() * 1000) for time in self.__answer_set.answer_list]))
