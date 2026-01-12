from datetime import datetime

from injector import Inject

from src.common.application.command_handler import CommandHandler
from src.common.application.event_bus import EventBus
from src.modules.questionnaires.application.interactors.set_test_token.set_test_token_command import SetTestTokenCommand
from src.modules.questionnaires.domain.test_session.test_session_repository_async import TestSessionRepositoryAsync


class SetTestTokenCommandHandler(CommandHandler[SetTestTokenCommand, None]):
    def __init__(
            self,
            event_bus: Inject[EventBus],
            test_session_repository: Inject[TestSessionRepositoryAsync]
    ):
        self.__event_bus = event_bus
        self.__test_session_repository = test_session_repository

    async def handle(self, command: SetTestTokenCommand) -> None:
        await self.__test_session_repository.set_token(
            test_session_id=command.test_session_id,
            token=command.token
        )

