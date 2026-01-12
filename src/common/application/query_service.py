from abc import ABC, abstractmethod
from typing import TypeVar

from src.common.application.query import Query

TQuery = TypeVar('TQuery', bound=Query, contravariant=True)
TResponse = TypeVar('TResponse', covariant=True)


class QueryService(ABC):
    @abstractmethod
    async def execute_async(self, query: TQuery) -> TResponse:
        ...
