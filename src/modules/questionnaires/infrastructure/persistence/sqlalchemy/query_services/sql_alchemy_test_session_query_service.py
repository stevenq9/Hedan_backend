from injector import Inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.questionnaires.application.interactors.get_test_session_id.get_test_session_id_query import \
    GetTestSessionIdQuery
from src.modules.questionnaires.application.interactors.get_test_session_id.get_test_session_id_service import \
    TestSessionIdQueryService
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.models.test_session_model import TestSessionModel


class SqlAlchemyTestSessionQueryService(TestSessionIdQueryService):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def execute_async(self, query: GetTestSessionIdQuery) -> int:
        async with self.__async_session_factory() as session:
            result = select(TestSessionModel.id).where(TestSessionModel.child_id == query.child_id
                                                       and TestSessionModel.psychologist_cedula
                                                       == query.pyschologist_cedula).fetch(1)
            return (await session.execute(result)).scalar()
