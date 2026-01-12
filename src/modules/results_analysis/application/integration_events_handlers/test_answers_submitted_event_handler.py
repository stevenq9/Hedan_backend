from injector import Inject

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.modules.questionnaires.domain.test_session.test_results import TestResults
from src.modules.questionnaires.integration_events.test_answers_submitted_event import TestAnswersSubmittedEvent
from src.modules.results_analysis.domain.test_report.test_report import TestReport
from src.modules.results_analysis.domain.test_report.test_report_repository_async import TestReportRepositoryAsync


class TestAnswersSubmittedEventHandler(IntegrationEventHandler[TestAnswersSubmittedEvent, None]):
    def __init__(
            self,
            test_report_repository: Inject[TestReportRepositoryAsync]
    ):
        self.__test_report_repository = test_report_repository

    async def handle(self, event: TestAnswersSubmittedEvent) -> None:
        await self.__test_report_repository.add_test_report(TestReport(
            id=0,
            child_id=event.child_id,
            test_session_id=event.test_session_id,
            psychologist_cedula=event.psychologist_cedula,
            child_sex=event.child_sex,
            child_age=event.child_age,
            scholar_grade=event.child_scholar_grade,
            date_time_of_answer=event.datetime_submitted,
            test_results=TestResults(
                social_anxiety_index=event.social_anxiety_index,
                physiological_anxiety_index=event.physiological_anxiety_index,
                defensiveness_index=event.defensiveness_index,
                worry_index=event.worry_index,
                total_anxiety_index=event.total_anxiety_index,
                inconsistent_answers_index=event.inconsistent_answers_index
            ),
            time_taken=event.time_taken
        ))
