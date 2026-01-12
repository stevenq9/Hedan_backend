from injector import Inject

from src.common.application.query_handler import QueryHandler
from src.modules.questionnaires.application.interactors.get_test_session_id.get_test_session_id_query import \
    GetTestSessionIdQuery
from src.modules.questionnaires.application.interactors.get_test_session_id.get_test_session_id_service import \
    TestSessionIdQueryService


class GetTestSessionIdQueryHandler(QueryHandler[GetTestSessionIdQuery, str]):
    def __init__(
            self,
            test_id_query_service: Inject[TestSessionIdQueryService]
    ):
        self.__test_id_query_service = test_id_query_service

    async def handle(self, query: GetTestSessionIdQuery) -> str:
        return await self.__test_id_query_service.execute_async(query)