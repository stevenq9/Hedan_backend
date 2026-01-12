from abc import ABC, abstractmethod

from src.common.application.write_service import WriteService
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_command import \
    UpdatePsychologistUserCommand


class UpdatePsychologistUserService(WriteService, ABC):
    @abstractmethod
    async def execute_async(self, command: UpdatePsychologistUserCommand) -> None:
        pass
