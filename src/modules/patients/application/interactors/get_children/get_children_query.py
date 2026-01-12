from dataclasses import dataclass

from src.common.application.query import Query
from src.common.domain.value_objects.cedula import Cedula


@dataclass(frozen=True)
class GetChildrenQuery(Query[str]):
    cedula: Cedula
