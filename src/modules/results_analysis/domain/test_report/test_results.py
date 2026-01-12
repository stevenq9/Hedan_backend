from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class TestResults(ValueObject):
    social_anxiety_index: int
    physiological_anxiety_index: int
    defensiveness_index: int
    worry_index: int
    total_anxiety_index: int
    inconsistent_answers_index: int

    def to_dict(self):
        return {
            'social_anxiety_index': self.social_anxiety_index,
            'physiological_anxiety_index': self.physiological_anxiety_index,
            'defensiveness_index': self.defensiveness_index,
            'worry_index': self.worry_index,
            'total_anxiety_index': self.total_anxiety_index,
            'inconsistent_answers_index': self.inconsistent_answers_index,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            social_anxiety_index=data['social_anxiety_index'],
            physiological_anxiety_index=data['physiological_anxiety_index'],
            defensiveness_index=data['defensiveness_index'],
            worry_index=data['worry_index'],
            total_anxiety_index=data['total_anxiety_index'],
            inconsistent_answers_index=data['inconsistent_answers_index']
        )
