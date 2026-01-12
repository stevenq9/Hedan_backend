from dataclasses import dataclass

from src.common.application.query import Query


@dataclass(frozen=True)
class ValidateQuestionnaireTokenQuery(Query[bool]):
    token: str
