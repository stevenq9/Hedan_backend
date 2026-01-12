from injector import Inject

from src.common.application.command_handler import CommandHandler
from src.common.application.event_bus import EventBus
from src.modules.questionnaires.application.interactors.add_test_session.add_test_session_command import \
    AddTestSessionCommand
from src.modules.questionnaires.domain.test_session.test_session import TestSession
from src.modules.questionnaires.domain.test_session.test_session_repository_async import TestSessionRepositoryAsync
from src.modules.questionnaires.integration_events.test_session_adedd_event import TestSessionAddedEvent


class AddTestSessionCommandHandler(CommandHandler[AddTestSessionCommand, int]):
    def __init__(
            self,
            event_bus: Inject[EventBus],
            test_session_repository_async: Inject[TestSessionRepositoryAsync],
    ):
        self.__event_bus = event_bus
        self.__test_session_repository_async = test_session_repository_async

    async def handle(self, command: AddTestSessionCommand) -> int:
        test_session = TestSession(
            id=0,
            child_id=command.child_id,
            psychologist_cedula=command.psychologist_cedula,
            child_age=command.child_age,
            scholar_grade=command.scholar_grade
        )
        test_id = await self.__test_session_repository_async.add_test_session(test_session)

        # self.__event_bus.publish(
        #    TestSessionAddedEvent(
        #        id=test_id,
        #        child_id=command.child_id,
        #        psychologist_cedula=command.psychologist_cedula,
        #        child_age=command.child_age,
        #        scholar_grade=command.scholar_grade
        #    )
        # )

        return test_id
