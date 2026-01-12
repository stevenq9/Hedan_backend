from dataclasses import dataclass
from datetime import timedelta

from src.common.domain.value_object import ValueObject
from src.modules.questionnaires.domain.test_session.question_id import QuestionId


@dataclass(frozen=True)
class Answer(ValueObject):
    question_id: QuestionId
    value: bool
    time_taken: timedelta

    def __post_init__(self):
        pass

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def to_dict(self):
        return {
            'question_id': str(self.question_id),
            'value': self.value,
            'time_taken': int(self.time_taken.total_seconds() * 1000)
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question_id=QuestionId(data['question_id']),
            value=data['value'],
            time_taken=timedelta(seconds=data['time_taken'])
        )
