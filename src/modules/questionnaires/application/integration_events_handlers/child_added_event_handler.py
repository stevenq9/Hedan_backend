from datetime import datetime

from injector import Inject

from src.common.application.integration_event_handler import IntegrationEventHandler
from src.modules.patients.integration_events.child_added_event import ChildAddedEvent
from src.modules.questionnaires.domain.test_session.test_session import TestSession
from src.modules.questionnaires.domain.test_session.test_session_repository_async import TestSessionRepositoryAsync


def years_difference(date_string):
    given_date = datetime.strptime(date_string, "%Y-%m-%d")
    current_date = datetime.now()
    difference_in_years = current_date.year - given_date.year
    if (current_date.month, current_date.day) < (given_date.month, given_date.day):
        difference_in_years -= 1
    return difference_in_years


class ChildAddedEventHandler(IntegrationEventHandler[ChildAddedEvent, None]):
    def __init__(self, repository: Inject[TestSessionRepositoryAsync]):
        self.repository = repository

    async def handle(self, event: ChildAddedEvent) -> int:
        # Generate test session id to associate with invitation link
        test_id = await self.repository.add_test_session(
            TestSession(
                id=0,
                child_id=event.child_id,
                psychologist_cedula=event.psychologist_cedula,
                child_age=years_difference(event.birthdate.strftime("%Y-%m-%d")),
                scholar_grade=event.scholar_grade,
                child_sex=event.sex,
                test_sender=event.test_sender,
                test_reason=event.test_reason)
        )
        return test_id

