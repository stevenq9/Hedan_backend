from injector import Inject

from src.common.application.query_handler import QueryHandler
from src.modules.questionnaires.application.interactors.get_test_session_list.get_test_session_list_query import \
    GetTestSessionListQuery
from src.modules.questionnaires.application.interactors.get_test_session_list.get_test_session_list_query_service import \
    TestSessionListQueryService


class GetTestSessionListQueryHandler(QueryHandler[GetTestSessionListQuery, str]):
    def __init__(
            self,
            test_session_list_query_service: Inject[TestSessionListQueryService]
    ):
        self.__test_session_list_query_service = test_session_list_query_service

    async def handle(self, query: GetTestSessionListQuery) -> str:
        return await self.__test_session_list_query_service.execute_async(query)
