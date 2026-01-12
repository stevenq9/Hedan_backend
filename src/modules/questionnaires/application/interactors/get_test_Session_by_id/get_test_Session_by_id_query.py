from dataclasses import dataclass

from src.common.application.query import Query


@dataclass(frozen=True)
class GetTestSessionByIdQuery(Query[str]):
    test_id: int