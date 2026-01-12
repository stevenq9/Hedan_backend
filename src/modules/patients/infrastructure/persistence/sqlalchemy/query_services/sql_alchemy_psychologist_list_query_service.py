from typing import List

from injector import Inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.patients.application.interactors.get_psychologists.get_psychologist_list_query import \
    GetPsychologistListQuery
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_query_service import \
    PsychologistListQueryService
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_response import \
    GetPsychologistListResponse
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.psychologist_model import PsychologistModel


class SqlAlchemyPsychologistListQueryService(PsychologistListQueryService):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def execute_async(self, query: GetPsychologistListQuery) -> List[GetPsychologistListResponse]:
        async with (self.__async_session_factory() as session):
            statement = select(
                PsychologistModel.name,
                PsychologistModel.sex,
                PsychologistModel.email,
                PsychologistModel.cedula,
            )
            rows = (await session.execute(statement)).fetchall()
            return [
                GetPsychologistListResponse(
                    name=row.name,
                    sex=row.sex,
                    email=row.email,
                    cedula=row.cedula,
                )
                for row in rows
            ]