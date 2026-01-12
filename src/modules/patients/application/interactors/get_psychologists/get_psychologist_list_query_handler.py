from injector import Inject

from src.common.application.query_handler import QueryHandler
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_list_query import \
    GetPsychologistListQuery
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_query_service import \
    PsychologistListQueryService


class GetPsychologistListQueryHandler(QueryHandler[GetPsychologistListQuery, str]):
    def __init__(
            self,
            psychologist_list_query_service: Inject[PsychologistListQueryService]
    ):
        self.__psychologist_list_query_service = psychologist_list_query_service

    async def handle(self, query: GetPsychologistListQuery) -> None:
        return await self.__psychologist_list_query_service.execute_async(query)
