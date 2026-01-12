from dataclasses import dataclass

from src.common.application.command import Command
from src.modules.questionnaires.domain.test_session.answers_set import AnswerSet


@dataclass(frozen=True)
class SetTestAnswersCommand(Command[None]):
    token: str
    answers: AnswerSet
