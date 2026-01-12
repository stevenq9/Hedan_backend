from datetime import datetime

from injector import Inject

from src.common.application.command_handler import CommandHandler
from src.common.application.event_bus import EventBus
from src.modules.questionnaires.application.interactors.set_test_answers.set_test_answers_command import \
    SetTestAnswersCommand
from src.modules.questionnaires.application.invitation_link.invitation_link_provider import InvitationLinkProvider
from src.modules.questionnaires.domain.test_session.test_session_repository_async import TestSessionRepositoryAsync
from src.modules.questionnaires.integration_events.test_answers_submitted_event import TestAnswersSubmittedEvent


class SetTestAnswersCommandHandler(CommandHandler[SetTestAnswersCommand, None]):
    def __init__(
            self,
            event_bus: Inject[EventBus],
            test_session_repository: Inject[TestSessionRepositoryAsync]
    ):
        self.__event_bus = event_bus
        self.__test_session_repository = test_session_repository

    async def handle(self, command: SetTestAnswersCommand) -> None:
        test_session_id = InvitationLinkProvider.decode_token(command.token)["test_session_id"]
        test_session_updated = await self.__test_session_repository.set_answers_set(test_session_id, command.answers)
        self.__event_bus.publish(TestAnswersSubmittedEvent(
            test_session_id=test_session_updated.id,
            child_id=test_session_updated.child_id,
            psychologist_cedula=test_session_updated.psychologist_cedula,
            child_age=test_session_updated.child_age,
            child_scholar_grade=test_session_updated.scholar_grade,
            child_sex=test_session_updated.child_sex,
            datetime_submitted=test_session_updated.date_time_of_answer,
            social_anxiety_index=test_session_updated.test_results.social_anxiety_index,
            physiological_anxiety_index=test_session_updated.test_results.physiological_anxiety_index,
            defensiveness_index=test_session_updated.test_results.defensiveness_index,
            worry_index=test_session_updated.test_results.worry_index,
            total_anxiety_index=test_session_updated.test_results.total_anxiety_index,
            inconsistent_answers_index=test_session_updated.test_results.inconsistent_answers_index,
            time_taken=test_session_updated.time_taken
        ))
