from typing import Optional, List

from injector import Inject
from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload

from src.modules.patients.application.interactors.get_children.get_children_query import GetChildrenQuery
from src.modules.patients.application.interactors.get_children.get_children_query_service import ChildrenQueryService
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.psychologist_model import PsychologistModel
from src.modules.results_analysis.api.test_reports.get_test_reports_dto import TestReportsDto
from src.modules.results_analysis.application.interactors.get_test_response.get_tests_reports_query import \
    GetTestsReportsQuery
from src.modules.results_analysis.infrastructure.persistence.sqlalchemy.models.test_report_model import TestReportModel


class GetTestsReportsQueryService:
    pass


class SqlAlchemyGetTestsReportsQueryService(GetTestsReportsQueryService):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def execute_async(self, query: GetTestsReportsQuery) -> Optional[list[TestReportsDto]]:
        async with self.__async_session_factory() as session:
            query = (
                select(TestReportModel, ChildModel.name)
                .join(ChildModel, TestReportModel.child_id == ChildModel.id)
                .where(TestReportModel.psychologist_cedula == str(query.psychologist_cedula))
            )
            result = await session.execute(query)
            test_reports = []
            for row in result:
                test_report, child_name = row
                test_reports.append({
                    'id': test_report.id,
                    'child_id': test_report.child_id,
                    'child_name': child_name,  # Incluyendo el nombre del niño
                    'psychologist_cedula': test_report.psychologist_cedula,
                    'test_session_id': test_report.test_session_id,
                    'child_age': test_report.child_age,
                    'scholar_grade': test_report.scholar_grade,
                    'child_sex': test_report.child_sex,
                    'date_time_of_answer': test_report.date_time_of_answer,
                    'test_results': test_report.test_results,
                    'time_taken': test_report.time_taken
                })

            return test_reports if test_reports else None