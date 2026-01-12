from injector import Inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel
from src.modules.questionnaires.api.questionnaires.test_session_dto import TestSessionDto
from src.modules.questionnaires.application.interactors.get_test_session_list.get_test_session_list_query import \
    GetTestSessionListQuery
from src.modules.questionnaires.application.interactors.get_test_session_list.get_test_session_list_query_service import \
    TestSessionListQueryService
from src.modules.questionnaires.application.invitation_link.invitation_link_provider import InvitationLinkProvider
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.models.test_session_model import TestSessionModel


class SqlAlchemyTestSessionListQueryService(TestSessionListQueryService):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def execute_async(self, query: GetTestSessionListQuery) -> list[TestSessionDto]:
        async with self.__async_session_factory() as session:
            query = (
                select(TestSessionModel, ChildModel)
                .join(ChildModel, TestSessionModel.child_id == ChildModel.id)
                .where(TestSessionModel.psychologist_cedula == str(query.cedula))
            )

            result = await session.execute(query)
            rows = result.fetchall()

            test_sessions: list[TestSessionDto] = []
            for test_session, child in rows:
                test_sessions.append(TestSessionDto(
                    test_id=test_session.id,
                    child_name=child.name,
                    child_age=test_session.child_age,
                    scholar_grade=test_session.scholar_grade,
                    child_sex=test_session.child_sex,
                    date_time_of_answer=test_session.date_time_of_answer,
                    token=test_session.test_token,
                    isTokenValid=InvitationLinkProvider.validate_token(test_session.test_token)
                )
                )
            return test_sessions
