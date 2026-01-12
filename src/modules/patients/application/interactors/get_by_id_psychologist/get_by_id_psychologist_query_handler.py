from injector import Inject
from src.common.application.query_handler import QueryHandler

from src.modules.patients.application.interactors.get_by_id_psychologist.get_by_id_psychologist_query import \
    GetByIdPsychologistQuery
from src.modules.patients.application.interactors.get_by_id_psychologist.get_by_id_psychologist_service import \
    GetByIdPsychologistService


class GetByIdPsychologistQueryHandler(QueryHandler[GetByIdPsychologistQuery, str]):
    def __init__(
            self,
            get_by_id_psychologist_user_query_service: Inject[GetByIdPsychologistService]
    ):
        self.__get_by_id_psychologist_user_query_service = get_by_id_psychologist_user_query_service

    async def handle(self, query: GetByIdPsychologistQuery) -> str:
        return await self.__get_by_id_psychologist_user_query_service.execute_async(query)

