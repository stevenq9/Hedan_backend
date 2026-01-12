from fastapi import HTTPException
from injector import Inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload

from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel
from src.modules.questionnaires.api.questionnaires.test_session_result_dto import ResultTestSessionDto
from src.modules.questionnaires.application.interactors.get_test_Session_by_id.get_test_Session_by_id_query import \
    GetTestSessionByIdQuery
from src.modules.questionnaires.application.interactors.get_test_Session_by_id.get_test_Session_by_id_query_service import \
    TestSessionByIdQueryService
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.models.test_session_model import TestSessionModel


class SqlAlchemyTestSessionByIdQueryService(TestSessionByIdQueryService):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def execute_async(self, query: GetTestSessionByIdQuery) -> ResultTestSessionDto:
        async with self.__async_session_factory() as session:
            query = (
                select(
                    TestSessionModel.id,
                    TestSessionModel.child_id,
                    TestSessionModel.psychologist_cedula,
                    TestSessionModel.child_age,
                    TestSessionModel.scholar_grade,
                    TestSessionModel.child_sex,
                    TestSessionModel.test_sender,
                    TestSessionModel.test_reason,
                    TestSessionModel.date_time_of_answer,
                    TestSessionModel.answers,
                    TestSessionModel.test_results,
                    TestSessionModel.calculate_test_results_time_taken,
                    ChildModel.name.label('child_name')
                )
                .join(ChildModel,
                      TestSessionModel.child_id == ChildModel.id)
                .where(TestSessionModel.id == query.test_id)
            )

            result = await session.execute(query)
            test_session = result.fetchone()

            if test_session is None:
                raise HTTPException(status_code=404, detail="Test session not found")

            return ResultTestSessionDto(
                test_id=test_session.id,
                child_id=test_session.child_id,
                child_name=test_session.child_name,
                psychologist_cedula=test_session.psychologist_cedula,
                child_age=test_session.child_age,
                scholar_grade=test_session.scholar_grade,
                child_sex=test_session.child_sex,
                test_sender=test_session.test_sender,
                test_reason=test_session.test_reason,
                date_time_of_answer=test_session.date_time_of_answer,
                answers_set=test_session.answers,
                test_results=test_session.test_results
            )


