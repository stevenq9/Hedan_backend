from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.common.application.query import Query

TQuery = TypeVar('TQuery', bound=Query, contravariant=True)
TResponse = TypeVar('TResponse', covariant=True)


class QueryHandler(Generic[TQuery, TResponse], ABC):
    @abstractmethod
    async def handle(self, query: TQuery) -> TResponse:
        ...
