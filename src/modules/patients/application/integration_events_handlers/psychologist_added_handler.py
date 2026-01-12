from src.common.application.integration_event_handler import IntegrationEventHandler
from src.modules.patients.domain.psychologist.psychologist import Psychologist
from src.modules.patients.domain.psychologist.psychologist_repository_async import PsychologistRepositoryAsync
from src.modules.users_management.integration_events.psychologist_added_event import PsychologistAddedEvent


class PsychologistAddedEventHandler(IntegrationEventHandler[PsychologistAddedEvent, None]):
    def __init__(self, psychologist_repository_async: PsychologistRepositoryAsync):
        self.__psychologist_repository_async=psychologist_repository_async

    async def handle(self, event: PsychologistAddedEvent) -> None:
        psychologist = Psychologist(
            cedula=event.cedula,
            name=event.name,
            sex=event.sex,
            email=event.email
        )

        await self.__psychologist_repository_async.add_psychologist(psychologist)
