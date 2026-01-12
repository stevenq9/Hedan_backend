from injector import Inject

from src.common.application.command_handler import CommandHandler
from src.common.application.event_bus import EventBus
from src.modules.patients.application.interactors.add_child.add_child_command import AddChildCommand
from src.modules.patients.domain.child.child import Child
from src.modules.patients.domain.child.child_repository_async import ChildRepositoryAsync
from src.modules.patients.integration_events.child_added_event import ChildAddedEvent


class AddChildCommandHandler(CommandHandler[AddChildCommand, int]):
    def __init__(
            self,
            event_bus: Inject[EventBus],
            child_repository_async: Inject[ChildRepositoryAsync],
    ):
        self.__event_bus = event_bus
        self.__child_repository_async = child_repository_async

    async def handle(self, command: AddChildCommand) -> int:
        child = Child(
            id=0,
            name=command.name,
            sex=command.sex,
            birthdate=command.birthdate,
            scholar_grade=command.scholar_grade,
            psychologist_cedula=command.psychologist_cedula
        )
        child_id = await self.__child_repository_async.add_child(child)

        self.__event_bus.publish(
            ChildAddedEvent(
                child_id=child_id,
                name=command.name,
                sex=command.sex,
                birthdate=command.birthdate,
                scholar_grade=int(command.scholar_grade),
                test_sender=command.test_sender,
                test_reason=command.test_reason,
                psychologist_cedula=command.psychologist_cedula
            )
        )

        return child_id
