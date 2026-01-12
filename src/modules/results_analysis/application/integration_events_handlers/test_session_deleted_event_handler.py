from injector import Inject

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.modules.questionnaires.integration_events.test_session_deleted_event import TestSessionDeletedEvent
from src.modules.results_analysis.domain.test_report.test_report_repository_async import TestReportRepositoryAsync


class TestSessionDeletedEventHandler(IntegrationEventHandler[TestSessionDeletedEvent, None]):
    def __init__(self, repository: Inject[TestReportRepositoryAsync]):
        self.repository = repository

    async def handle(self, event: TestSessionDeletedEvent) -> bool:
        # Delete test report associated with test session
        await self.repository.delete_test_report_by_test_session_id(event.test_session_id)
        return True
