from dataclasses import dataclass
from typing import List

from src.common.domain.value_object import ValueObject
from src.modules.questionnaires.domain.test_session.answer import Answer


@dataclass(frozen=True)
class AnswerSet(ValueObject):
    answer_list: List[Answer]

    def __post_init__(self):
        if len(self.answer_list) != 49:
            raise ValueError("The answer set should have 49 answers")

        question_ids = [int(answer.question_id) for answer in self.answer_list]
        if len(set(question_ids)) != 49:
            raise ValueError("The answer set should have 49 unique questions")
