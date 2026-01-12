from injector import Inject

from src.common.application.command_handler import CommandHandler, TCommand, TResponse
from src.common.application.event_bus import EventBus
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_command import \
    UpdatePsychologistUserCommand
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_service import \
    UpdatePsychologistUserService
from src.modules.users_management.integration_events.psychologist_updated_event import PsychologistUpdatedEvent


class UpdatePsychologistUserCommandHandler(CommandHandler[UpdatePsychologistUserCommand, None]):
    def __init__(
            self,
            event_bus: Inject[EventBus],
            update_psychologist_user_service: Inject[UpdatePsychologistUserService]
    ):
        self.__update_psychologist_user_service = update_psychologist_user_service
        self.__event_bus = event_bus

    async def handle(self, command: UpdatePsychologistUserCommand) -> None:
        await self.__update_psychologist_user_service.execute_async(command)

        self.__event_bus.publish(
            PsychologistUpdatedEvent(
                cedula=command.cedula,
                name=command.name,
                sex=command.sex,
                email=command.email
            )
        )
