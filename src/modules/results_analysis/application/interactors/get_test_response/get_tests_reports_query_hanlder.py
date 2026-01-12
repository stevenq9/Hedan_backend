from injector import Inject

from src.common.application.query_handler import QueryHandler
from src.modules.patients.application.interactors.get_children.get_children_query import GetChildrenQuery
from src.modules.patients.application.interactors.get_children.get_children_query_service import ChildrenQueryService
from src.modules.results_analysis.application.interactors.get_test_response.get_tests_reports_query import \
    GetTestsReportsQuery
from src.modules.results_analysis.application.interactors.get_test_response.get_tests_reports_query_service import \
    GetTestsReportsQueryService


class GetTestsReportsQueryHandler(QueryHandler[GetTestsReportsQuery, str]):
    def __init__(
            self,
            tests_reports_query_service: Inject[GetTestsReportsQueryService]
    ):
        self.__tests_reports_query_service = tests_reports_query_service

    async def handle(self, query: GetTestsReportsQuery) -> str:
        return await self.__tests_reports_query_service.execute_async(query)
