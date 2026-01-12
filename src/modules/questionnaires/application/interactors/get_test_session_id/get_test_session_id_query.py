from dataclasses import dataclass

from src.common.application.query import Query


@dataclass(frozen=True)
class GetTestSessionIdQuery(Query[str]):
    child_id: int
    pyschologist_cedula: str