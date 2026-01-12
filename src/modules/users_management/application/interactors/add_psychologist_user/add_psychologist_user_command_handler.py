from injector import Inject

from src.common.application.command_handler import CommandHandler, TCommand, TResponse
from src.common.application.event_bus import EventBus
from src.modules.users_management.application.interactors.add_psychologist_user.add_psychologist_user_command import \
    AddPsychologistUserCommand
from src.modules.users_management.application.interactors.add_psychologist_user.create_psychologist_user_service import \
    CreatePsychologistUserService
from src.modules.users_management.integration_events.psychologist_added_event import PsychologistAddedEvent


class AddPsychologistUserCommandHandler(CommandHandler[AddPsychologistUserCommand, None]):
    def __init__(
            self,
            event_bus: Inject[EventBus],
            create_psychologist_user_service: Inject[CreatePsychologistUserService]
    ):
        self.__create_psychologist_user_service =create_psychologist_user_service
        self.__event_bus = event_bus

    async def handle(self, command: AddPsychologistUserCommand) -> None:
        await self.__create_psychologist_user_service.execute_async(command)

        self.__event_bus.publish(
            PsychologistAddedEvent(
                cedula=command.cedula,
                name=command.name,
                sex=command.sex,
                email=command.email
            )
        )
